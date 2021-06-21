import asyncio
import json
import uuid
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

from app.Agent import Agent

app = FastAPI()
origins = [
    '*',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'HEAD', 'OPTIONS'],
    allow_headers=['*'],
)

running_agents: Dict[uuid.UUID, Agent] = {}


class GetAgent(BaseModel):
    room: str
    chat_server_host: str


@app.get('/')
def home():
    return {
        'hello': 'world'
    }


@app.post('/agents/init')
async def init_agent(r_data: GetAgent):
    room = r_data.room
    host = r_data.chat_server_host
    uid = generate_uuid()
    agent = Agent(host, uid, room, 'bot')
    task = asyncio.create_task(agent.connect_agent())
    await task
    running_agents[uid] = agent
    print('running agents : ', running_agents)
    return agent.to_dict()


def generate_uuid():
    uid = uuid.uuid4()
    while uid in running_agents.keys():
        uid = uuid.uuid4()
    return uid

