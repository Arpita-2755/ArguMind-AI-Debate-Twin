from agents.moderator import ModeratorAgent
from agents.opponent import OpponentAgent
from agents.judge import JudgeAgent
from agents.reflection import ReflectionAgent
from agents.reasoning_analyzer import ReasoningAnalyzerAgent
from agents.memory_agent import MemoryAgent
from agents.memory_update_agent import MemoryUpdateAgent


moderator = ModeratorAgent()
opponent = OpponentAgent()
judge = JudgeAgent()
reflection = ReflectionAgent()
reasoning_analyzer = ReasoningAnalyzerAgent()
memory = MemoryAgent()
memory_update = MemoryUpdateAgent()


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


def reasoning_analyzer_node(state):
    print("Reasoning Analyzer node reached")
    return reasoning_analyzer.run(state)


def memory_node(state):
    print("Memory node reached")
    return memory.run(state)


def memory_update_node(state):
    print("Memory update node reached")
    return memory_update.run(state)