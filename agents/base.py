from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the agent and return a JSON-serialisable dict."""
