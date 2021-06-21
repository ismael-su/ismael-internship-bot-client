import uuid

from app.Agent import Agent
agent1 = Agent("http://localhost:8000", uuid.uuid4(), 'test')
agent2 = Agent("http://localhost:8000", uuid.uuid4(), 'test')
print('Agent1: What is your name ?')
answer = agent2.talk('What is your name ?')
counter = 0
while counter < 5:
    print('Agent2: ', answer)
    answer = agent1.talk(answer)
    print('Agent1: ', answer)
    answer = agent2.talk(answer)
    counter = counter + 1
