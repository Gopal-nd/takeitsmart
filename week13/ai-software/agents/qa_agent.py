# agents/qa_agent.py

from .base_agent import BaseAgent

class QAAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="QA Engineer",
            system_prompt="""
            Generate:
            - Unit tests
            - Edge cases
            - Integration tests
            """
        )