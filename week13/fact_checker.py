from .base_agent import BaseAgent

class FactCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__("FactChecker")

    def process(self, text, context=None):
        summary = context.get("summary", "") if context else text
        return f"Checked summary: '{summary[:75]}...' — Verdict: Mostly Accurate (placeholder)"