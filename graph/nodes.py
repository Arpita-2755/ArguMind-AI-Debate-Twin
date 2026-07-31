from agents.moderator import ModeratorAgent

moderator = ModeratorAgent()

def moderator_node(state):
    print("Moderator node reached")
    return moderator.run(state)