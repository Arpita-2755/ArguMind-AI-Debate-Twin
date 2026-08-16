from agents.moderator import ModeratorAgent
from agents.opponent import OpponentAgent
from agents.judge import JudgeAgent
moderator = ModeratorAgent()
opponent = OpponentAgent()
judge = JudgeAgent()

def moderator_node(state):
    print("Moderator node reached")
    return moderator.run(state)


def opponent_node(state):
    print("Opponent node reached")
    return opponent.run(state)

def judge_node(state):
    print("Judge node reached")
    return judge.run(state)