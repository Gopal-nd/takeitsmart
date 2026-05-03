# agents/code_reviewer.py

from .base_agent import BaseAgent

class CodeReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Senior Code Reviewer",
            system_prompt="""
            Review code:
            - Suggest improvements
            - Fix bugs
            - Improve performance
            """
        )