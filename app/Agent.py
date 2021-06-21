from typing import Any, Dict, List
from uuid import UUID

from transformers import BlenderbotForConditionalGeneration, BlenderbotTokenizer
import torch
import asyncio

import socketio

# model_name = 'facebook/blenderbot-3B'
model_name = 'facebook/blenderbot-400M-distill'
# model_name = 'facebook/blenderbot-1B-distill'
blender_tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

blender_model = BlenderbotForConditionalGeneration.from_pretrained(model_name)


class Agent:
    """
    Agent let us have multiple AI chatter running at the same time
    and based on the same model, we can even make two agent talk to each other. check
    the test script for more details
    """
    chat_server_host: str
    step: int
    username = ''
    uid: UUID
    chat = ''
    chat_history_ids: Any
    bot_input_ids: Any
    human_readable_chat_history: List[Dict[str, str]] = []
    tokenizer: BlenderbotTokenizer
    model: Any

    def __init__(self, chat_server_host, uid, chat, username=''):
        self.step = 0
        self.uid = uid
        self.chat = chat
        self.username = username
        self.chat_server_host = chat_server_host
        self.tokenizer = blender_tokenizer
        self.model = blender_model
        self.sio = socketio.AsyncClient()
        # self.sio = socketio.AsyncClient(logger=True, engineio_logger=True)
        self.init_handlers()

    async def connect(self):
        await self.sio.connect(self.chat_server_host, socketio_path="ws/socket.io", wait_timeout=60000)
        print("my sid is", self.sio.sid)

    async def join_chat(self):
        await self.sio.emit('join_chat', self.to_dict())

    async def connect_agent(self):
        await self.connect()
        await self.join_chat()
        await self.send_message('Hi, i am Rumble Studio Assistant, How can i help you ?')

    def talk(self, msg: str):
        new_user_input_ids = self.tokenizer.encode(
            msg + self.tokenizer.eos_token,
            return_tensors='pt').to(device)

        # append the new user input tokens to the chat history
        self.bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids],
                                       dim=-1) if self.step > 0 else new_user_input_ids

        # Make model use GPU if available
        self.model.to(device)

        # generated a response while limiting the total chat history to 1000 tokens,
        self.chat_history_ids = self.model.generate(
            self.bot_input_ids, max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id)

        self.step = self.step + 1
        # pretty print last output tokens from bot
        answer = self.tokenizer.decode(self.chat_history_ids[0], skip_special_tokens=True)

        self.human_readable_chat_history.append(
            {
                "input": msg,
                "output": answer
            }
        )
        return answer

    async def on_connect(self):
        print(3 * "\n")
        print("[EVENT.connect]")
        print("connected to server, my sid is", self.sio.sid)
        print(1 * "\n")

    @staticmethod
    async def on_disconnect():
        print(3 * "\n")
        print("[EVENT.disconnect]")
        print("disconnected from server")
        print(1 * "\n")

    async def on_message(self, data):
        print(3 * "\n")
        print("[EVENT.message]")
        print("New message", data)
        print(1 * "\n")
        if data['sender'] == 'server_alert':
            return
        answer = self.talk(data['message'])
        await self.send_message(answer)

    @staticmethod
    def on_server_reply(data):
        print(3 * "\n")
        print("[EVENT.server_reply]")
        print(data)
        print(1 * "\n")

    @staticmethod
    def on_connect_error(data):
        print(3 * "\n")
        print("[EVENT.connect_error]")
        print("The connection failed!")
        print(data)
        print(1 * "\n")

    async def send_message(self,  message_to_send):
        print(3 * "\n")
        print("[EVENT.send_message]")
        print(message_to_send)
        print(1 * "\n")
        await self.sio.emit(
            "send_message",
            {"channel_id": self.chat, "username": self.username, "message": message_to_send},
        )

    async def test(self):
        await self.connect()
        await self.join_chat()
        print(3 * "\n")
        await self.send_message("Hi everyone")
        await self.sio.wait()

    async def test_passive(self):
        await self.connect()
        await self.join_chat()
        print(3 * "\n")

    def init_handlers(self):
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)
        self.sio.on('server_reply', self.on_server_reply)
        self.sio.on('connect_error', self.on_connect_error)

    def to_dict(self):
        return {
            'uid': self.uid.__str__(),
            'username': self.username,
            'chat_server_host': self.chat_server_host,
            'channel_id': self.chat,
            'is_connected': self.sio.connected
        }

