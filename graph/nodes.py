from agents.moderator import ModeratorAgent
from agents.opponent import OpponentAgent

moderator = ModeratorAgent()
opponent = OpponentAgent()


def moderator_node(state):
    print("Moderator node reached")
    return moderator.run(state)


def opponent_node(state):
    print("Opponent node reached")
    return opponent.run(state)