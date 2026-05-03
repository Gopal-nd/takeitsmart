from agents.product_manager import ProductManagerAgent
from agents.architect import ArchitectAgent
from agents.backend_dev import BackendDevAgent
from agents.frontend_dev import FrontendDevAgent
from agents.code_reviewer import CodeReviewerAgent
from agents.qa_agent import QAAgent
from agents.devops_agent import DevOpsAgent

from tools.vector_store import VectorStore  # ✅ ADD THIS


def safe_run(agent, input_text):
    try:
        result = agent.run(input_text)
        if not result or len(result.strip()) < 20:
            return "⚠️ Agent failed to generate valid output"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


class SoftwareTeamOrchestrator:

    def __init__(self):
        self.pm = ProductManagerAgent()
        self.architect = ArchitectAgent()
        self.backend = BackendDevAgent()
        self.frontend = FrontendDevAgent()
        self.reviewer = CodeReviewerAgent()
        self.qa = QAAgent()
        self.devops = DevOpsAgent()

        self.memory = VectorStore()  # ✅ INIT MEMORY

    def run_pipeline(self, idea):

        context = {
            "idea": idea
        }

        # 📌 Step 1: Requirements
        context["requirements"] = safe_run(self.pm, context["idea"])
        self.memory.add_text(context["requirements"])  # ✅ STORE

        # 🔍 Retrieve memory (optional but powerful)
        past_context = self.memory.search("software requirements")

        # 🏗 Step 2: Architecture
        context["architecture"] = safe_run(
            self.architect,
            f"""
            Use these requirements:
            {context["requirements"]}

            Relevant past knowledge:
            {past_context}

            Do NOT change domain.
            """
        )

        self.memory.add_text(context["architecture"])  # ✅ STORE

        # ⚙ Step 3: Backend
        backend_input = f"""
        Use this architecture strictly:
        {context["architecture"]}

        Relevant past knowledge:
        {past_context}

        RULES:
        - Use FastAPI only
        - Keep consistency
        """

        context["backend_code"] = safe_run(self.backend, backend_input)
        self.memory.add_text(context["backend_code"])  # ✅ STORE

        # 🔁 Step 4: Reviewer Loop
        for _ in range(2):
            review = safe_run(self.reviewer, context["backend_code"])

            if "no issues" in review.lower():
                break

            fix_prompt = f"""
            Fix the code based on review.

            CODE:
            {context["backend_code"]}

            REVIEW:
            {review}
            """

            context["backend_code"] = safe_run(self.backend, fix_prompt)

        context["review"] = review

        # 🎨 Step 5: Frontend
        context["frontend_code"] = safe_run(
            self.frontend,
            f"""
            Build UI based on backend:
            {context["backend_code"]}
            """
        )

        # 🧪 Step 6: QA
        context["tests"] = safe_run(self.qa, context["backend_code"])

        # 🚀 Step 7: DevOps
        context["deployment"] = safe_run(
            self.devops,
            f"""
            Deploy system:

            ARCHITECTURE:
            {context["architecture"]}

            BACKEND:
            {context["backend_code"]}
            """
        )

        return context