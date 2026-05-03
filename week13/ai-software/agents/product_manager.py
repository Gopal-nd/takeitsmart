# agents/product_manager.py

from .base_agent import BaseAgent

class ProductManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Product Manager",
            system_prompt="""
            Create:
            - Features
            - User stories
            - Functional requirements
            - Non-functional requirements
            """
        )