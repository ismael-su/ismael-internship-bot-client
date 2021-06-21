# Bot client
## Install deps and run

```shell
git clone git@github.com:ismael-su/ismael-internship-bot-client.git
cd ismael-internship-bot-client
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/install-poetry.py | python
conda create -n rumble-bot-client-py381 python=3.8.1
conda activate rumble-bot-client-py381
poetry install
poetry run uvicorn app.main:app --reload
```

### Make an Agent join a chat

send an HTTP post request to this server at the endpoint ``agents/init``
the request body structure : 
````json
{
  "room": "chat_room_name",
  "chat_server_host":  "addresse of the chat server[http://X.X.X.X:8000]",
}
````

example of a server response 
````json
{
    "uid": "80a44343-6b30-40ef-8833-938000fb9bf0",
    "username": "bot",
    "chat_server_host": "http://localhost:8001",
    "channel_id": "myAmazingChat",
    "is_connected": true
}
````

The uid will be used later to send commands to the bot client such as making it leave the chat

## Test
In order to locally test the clients, you can create 2 Agents and make them talk to each other.
Check the test file for more details
