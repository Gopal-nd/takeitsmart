# agents/architect.py

from .base_agent import BaseAgent

class ArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Software Architect",
            system_prompt="""
            Design system architecture:
            - Tech stack
            - APIs
            - DB schema
            - High-level diagram (text)
            """
        )