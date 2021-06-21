from typing import Dict

from docker.client import DockerClient
from docker.errors import NotFound

CONTAINER_NAME = "ismael-chat-bot-client-test"


def remove_previous_container(client: DockerClient) -> None:
    try:
        previous = client.containers.get(CONTAINER_NAME)
        previous.stop()
        previous.remove()
    except NotFound:
        return None


def get_logs(container: DockerClient) -> str:
    logs = container.logs()
    return logs.decode("utf-8")


def get_response_home() -> Dict:
    return {
        'hello': 'world'
    }
