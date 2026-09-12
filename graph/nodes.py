from agents.moderator import ModeratorAgent
from agents.opponent import OpponentAgent
from agents.judge import JudgeAgent
from agents.reflection import ReflectionAgent
moderator = ModeratorAgent()
opponent = OpponentAgent()
judge = JudgeAgent()
reflection = ReflectionAgent()

def moderator_node(state):
    print("Moderator node reached")
    return moderator.run(state)


def opponent_node(state):
    print("Opponent node reached")
    return opponent.run(state)

def judge_node(state):
    print("Judge node reached")
    return judge.run(state)

def reflection_node(state):
    print("Reflection node reached")
    return reflection.run(state)