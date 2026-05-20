from sqlalchemy.orm import Session
from app.database import Project, ProjectStep
from agents.product_manager import ProductManagerAgent
from agents.architect import ArchitectAgent
from agents.backend_dev import BackendDevAgent
from agents.frontend_dev import FrontendDevAgent
from agents.code_reviewer import CodeReviewerAgent
from agents.qa_agent import QAAgent
from agents.devops_agent import DevOpsAgent
from tools.vector_store import VectorStore

class SoftwareTeamOrchestrator:

    def __init__(self):
        self.pm = ProductManagerAgent()
        self.architect = ArchitectAgent()
        self.backend = BackendDevAgent()
        self.frontend = FrontendDevAgent()
        self.reviewer = CodeReviewerAgent()
        self.qa = QAAgent()
        self.devops = DevOpsAgent()
        self.memory = VectorStore()

    def get_step_content(self, db: Session, project_id: int, step_name: str) -> str:
        step = db.query(ProjectStep).filter_by(project_id=project_id, step_name=step_name).first()
        return step.content if step else ""

    def save_step_content(self, db: Session, project_id: int, step_name: str, content: str):
        if step_name in ["backend_code", "frontend_code", "tests"]:
            from app.export_utils import clean_code_block
            content = clean_code_block(content)
            
        step = db.query(ProjectStep).filter_by(project_id=project_id, step_name=step_name).first()
        if step:
            step.content = content
        else:
            step = ProjectStep(project_id=project_id, step_name=step_name, content=content)
            db.add(step)
        db.commit()
        # Add to FAISS memory
        try:
            self.memory.add_text(f"[{step_name.upper()}]: {content}")
        except Exception:
            pass

    def stream_requirements(self, db: Session, project_id: int):
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            yield "Error: Project not found"
            return
        
        buffered = []
        for chunk in self.pm.run_stream(project.idea):
            buffered.append(chunk)
            yield chunk
        
        full_text = "".join(buffered).strip()
        if full_text and not full_text.startswith("Error"):
            self.save_step_content(db, project_id, "requirements", full_text)
            project.status = "requirements"
            db.commit()

    def stream_architecture(self, db: Session, project_id: int):
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            yield "Error: Project not found"
            return
        
        requirements = self.get_step_content(db, project_id, "requirements")
        past_context = ""
        try:
            past_results = self.memory.search("software requirements")
            past_context = "\n".join([doc.page_content for doc in past_results])
        except Exception:
            pass

        prompt = f"""
        Use these requirements:
        {requirements}

        Relevant past knowledge:
        {past_context}

        Do NOT change domain.
        """

        buffered = []
        for chunk in self.architect.run_stream(prompt):
            buffered.append(chunk)
            yield chunk
        
        full_text = "".join(buffered).strip()
        if full_text and not full_text.startswith("Error"):
            self.save_step_content(db, project_id, "architecture", full_text)
            project.status = "architecture"
            db.commit()

    def stream_backend_code(self, db: Session, project_id: int):
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            yield "Error: Project not found"
            return
        
        architecture = self.get_step_content(db, project_id, "architecture")
        past_context = ""
        try:
            past_results = self.memory.search("software architecture")
            past_context = "\n".join([doc.page_content for doc in past_results])
        except Exception:
            pass

        prompt = f"""
        Use this architecture strictly:
        {architecture}

        Relevant past knowledge:
        {past_context}

        RULES:
        - Use FastAPI only
        - Keep consistency
        """

        buffered = []
        for chunk in self.backend.run_stream(prompt):
            buffered.append(chunk)
            yield chunk
        
        full_text = "".join(buffered).strip()
        if full_text and not full_text.startswith("Error"):
            self.save_step_content(db, project_id, "backend_code", full_text)
            project.status = "code_backend"
            db.commit()

    def stream_review(self, db: Session, project_id: int):
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            yield "Error: Project not found"
            return
        
        backend_code = self.get_step_content(db, project_id, "backend_code")
        buffered = []
        for chunk in self.reviewer.run_stream(backend_code):
            buffered.append(chunk)
            yield chunk
        
        full_text = "".join(buffered).strip()
        if full_text and not full_text.startswith("Error"):
            self.save_step_content(db, project_id, "review", full_text)
            db.commit()

    def stream_frontend_code(self, db: Session, project_id: int):
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            yield "Error: Project not found"
            return
        
        backend_code = self.get_step_content(db, project_id, "backend_code")
        architecture = self.get_step_content(db, project_id, "architecture")
        
        prompt = f"""
        Project Idea: {project.idea}
        
        ARCHITECTURE:
        {architecture}
        
        BACKEND IMPLEMENTATION DETAILS:
        {backend_code}
        
        INSTRUCTIONS:
        1. Design a fully featured, state-of-the-art interactive client UI in React to manage the data models defined in the backend API above.
        2. Ensure the UI looks absolutely STUNNING and PREMIUM:
           - Use rich dark-mode HSL gradients (e.g. from slate-900 to indigo-950/20).
           - Design beautifully styled layout blocks: a header title bar, a main workspace card, and styled table/list grids.
           - Ensure all buttons, forms, and toggles have gorgeous colors, rounded corners (rounded-xl/rounded-2xl), hover effects, and glowing active states.
           - Use Tailwind typography classes (text-slate-200, font-bold, tracking-wide, etc.) to convey premium polish.
        3. Make sure all backend endpoints (e.g. GET, POST, PUT, DELETE) are linked to frontend state. Any CRUD modifications should update the task/item state reactively in React.
        4. Integrate beautiful select dropdowns, search inputs, sorting options, and action buttons cleanly.
        """

        buffered = []
        for chunk in self.frontend.run_stream(prompt):
            buffered.append(chunk)
            yield chunk
        
        full_text = "".join(buffered).strip()
        if full_text and not full_text.startswith("Error"):
            self.save_step_content(db, project_id, "frontend_code", full_text)
            project.status = "code"
            db.commit()

    def stream_qa(self, db: Session, project_id: int):
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            yield "Error: Project not found"
            return
        
        backend_code = self.get_step_content(db, project_id, "backend_code")
        buffered = []
        for chunk in self.qa.run_stream(backend_code):
            buffered.append(chunk)
            yield chunk
        
        full_text = "".join(buffered).strip()
        if full_text and not full_text.startswith("Error"):
            self.save_step_content(db, project_id, "tests", full_text)
            project.status = "qa"
            db.commit()

    def stream_devops(self, db: Session, project_id: int):
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            yield "Error: Project not found"
            return
        
        architecture = self.get_step_content(db, project_id, "architecture")
        backend_code = self.get_step_content(db, project_id, "backend_code")
        prompt = f"""
        Deploy system:

        ARCHITECTURE:
        {architecture}

        BACKEND:
        {backend_code}
        """

        buffered = []
        for chunk in self.devops.run_stream(prompt):
            buffered.append(chunk)
            yield chunk
        
        full_text = "".join(buffered).strip()
        if full_text and not full_text.startswith("Error"):
            self.save_step_content(db, project_id, "deployment", full_text)
            project.status = "completed"
            db.commit()