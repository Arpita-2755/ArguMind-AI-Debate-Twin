from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, state):
        """
        Executes the agent.
        Must be implemented by child classes.
        """
        pass