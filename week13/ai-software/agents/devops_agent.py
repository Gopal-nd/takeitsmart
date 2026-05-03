# agents/devops_agent.py

from .base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="DevOps Engineer",
            system_prompt="""
            Provide:
            - Dockerfile
            - Deployment steps
            - CI/CD pipeline
            """
        )