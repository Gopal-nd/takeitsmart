# agents/backend_dev.py

from .base_agent import BaseAgent

class BackendDevAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Backend Developer",
            system_prompt="""
            Generate clean FastAPI backend code.
            Include routes, models, and logic.
            """
        )