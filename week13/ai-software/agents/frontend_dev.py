# agents/frontend_dev.py

from .base_agent import BaseAgent

class FrontendDevAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Frontend Developer",
            system_prompt="""
            Generate modern UI using React or Streamlit.
            Clean and minimal design.
            """
        )