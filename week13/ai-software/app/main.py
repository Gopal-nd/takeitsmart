import os
import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import init_db, get_db, Project, ProjectStep
from app.orchestrator import SoftwareTeamOrchestrator
from app.export_utils import create_project_zip

# Initialize DB on startup
init_db()

app = FastAPI(title="AI Software Development Team API")

# Enable CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = SoftwareTeamOrchestrator()

# --- Pydantic Schemas ---
class ProjectCreate(BaseModel):
    name: str
    idea: str
    model_id: str = "meta.llama3-8b-instruct-v1:0"
    temperature: float = 0.2

class RequestModel(BaseModel):
    idea: str

class StepUpdate(BaseModel):
    content: str

# --- SSE Helper ---
def make_sse_generator(generator):
    try:
        for chunk in generator:
            yield f"data: {json.dumps({'token': chunk})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

# --- REST Endpoints ---

@app.get("/api/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [{
        "id": p.id,
        "name": p.name,
        "idea": p.idea,
        "model_id": p.model_id,
        "temperature": p.temperature,
        "status": p.status,
        "created_at": p.created_at.isoformat() if p.created_at else None
    } for p in projects]

@app.post("/api/projects")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(
        name=payload.name,
        idea=payload.idea,
        model_id=payload.model_id,
        temperature=payload.temperature,
        status="created"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@app.get("/api/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    steps = db.query(ProjectStep).filter_by(project_id=project_id).all()
    return {
        "id": project.id,
        "name": project.name,
        "idea": project.idea,
        "model_id": project.model_id,
        "temperature": project.temperature,
        "status": project.status,
        "created_at": project.created_at.isoformat() if project.created_at else None,
        "steps": {s.step_name: s.content for s in steps}
    }

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

@app.put("/api/projects/{project_id}/step/{step_name}")
def update_project_step(project_id: int, step_name: str, payload: StepUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    orchestrator.save_step_content(db, project_id, step_name, payload.content)
    return {"message": f"Step {step_name} updated successfully"}

# --- SSE Streaming Endpoints ---

@app.get("/api/projects/{project_id}/stream/requirements")
def stream_requirements_endpoint(project_id: int, db: Session = Depends(get_db)):
    return StreamingResponse(
        make_sse_generator(orchestrator.stream_requirements(db, project_id)),
        media_type="text/event-stream"
    )

@app.get("/api/projects/{project_id}/stream/architecture")
def stream_architecture_endpoint(project_id: int, db: Session = Depends(get_db)):
    return StreamingResponse(
        make_sse_generator(orchestrator.stream_architecture(db, project_id)),
        media_type="text/event-stream"
    )

@app.get("/api/projects/{project_id}/stream/backend_code")
def stream_backend_endpoint(project_id: int, db: Session = Depends(get_db)):
    return StreamingResponse(
        make_sse_generator(orchestrator.stream_backend_code(db, project_id)),
        media_type="text/event-stream"
    )

@app.get("/api/projects/{project_id}/stream/review")
def stream_review_endpoint(project_id: int, db: Session = Depends(get_db)):
    return StreamingResponse(
        make_sse_generator(orchestrator.stream_review(db, project_id)),
        media_type="text/event-stream"
    )

@app.get("/api/projects/{project_id}/stream/frontend_code")
def stream_frontend_endpoint(project_id: int, db: Session = Depends(get_db)):
    return StreamingResponse(
        make_sse_generator(orchestrator.stream_frontend_code(db, project_id)),
        media_type="text/event-stream"
    )

@app.get("/api/projects/{project_id}/stream/tests")
@app.get("/api/projects/{project_id}/stream/qa")
def stream_qa_endpoint(project_id: int, db: Session = Depends(get_db)):
    return StreamingResponse(
        make_sse_generator(orchestrator.stream_qa(db, project_id)),
        media_type="text/event-stream"
    )

@app.get("/api/projects/{project_id}/stream/deployment")
@app.get("/api/projects/{project_id}/stream/devops")
def stream_devops_endpoint(project_id: int, db: Session = Depends(get_db)):
    return StreamingResponse(
        make_sse_generator(orchestrator.stream_devops(db, project_id)),
        media_type="text/event-stream"
    )

# --- Sandbox running endpoints ---
import subprocess
import signal
import sys
import time

active_sandboxes = {}

@app.post("/api/projects/{project_id}/run")
def run_sandbox(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get backend code step
    step = db.query(ProjectStep).filter_by(project_id=project_id, step_name="backend_code").first()
    if not step or not step.content:
        raise HTTPException(status_code=400, detail="Backend code must be generated first")
    
    # Clean code blocks
    from app.export_utils import clean_code_block
    clean_code = clean_code_block(step.content)
    
    # Filter out redundant/hallucinated database imports that conflict with the sandbox setup
    lines = clean_code.split('\n')
    filtered_lines = [
        line for line in lines 
        if not (line.strip().startswith("from database import") or line.strip().startswith("import database"))
    ]
    clean_code = '\n'.join(filtered_lines)
    
    # Ensure app directory exists
    os.makedirs("app", exist_ok=True)
    sandbox_file = "app/sandbox_app.py"
    with open(sandbox_file, "w", encoding="utf-8") as f:
        f.write(clean_code)
        
    # Stop ALL existing sandboxes running on port 8080 to prevent conflicts
    for pid_proj_id, proc in list(active_sandboxes.items()):
        try:
            if sys.platform != "win32":
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            else:
                proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            pass
    active_sandboxes.clear()
            
    # Force kill any process lingering on port 8080 to ensure it is completely free
    if sys.platform != "win32":
        try:
            subprocess.run(["fuser", "-k", "8080/tcp"], capture_output=True, timeout=2)
        except Exception:
            pass
            
    # Launch uvicorn on port 8080 in background, writing logs directly to app/sandbox.log
    log_file = open("app/sandbox.log", "w", encoding="utf-8")
    cmd = [sys.executable, "-m", "uvicorn", "app.sandbox_app:app", "--host", "0.0.0.0", "--port", "8080"]
    try:
        if sys.platform != "win32":
            proc = subprocess.Popen(
                cmd,
                preexec_fn=os.setsid,
                stdout=log_file,
                stderr=log_file
            )
        else:
            proc = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=log_file
            )
        active_sandboxes[project_id] = proc
        
        # Wait for uvicorn to bind to port
        time.sleep(2.0)
        return {
            "status": "running",
            "url": "http://localhost:8080",
            "docs_url": "http://localhost:8080/docs"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start sandbox: {str(e)}")

@app.post("/api/projects/{project_id}/stop")
def stop_sandbox(project_id: int):
    if project_id in active_sandboxes:
        try:
            proc = active_sandboxes[project_id]
            if sys.platform != "win32":
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            else:
                proc.terminate()
            proc.wait(timeout=2)
            del active_sandboxes[project_id]
            return {"status": "stopped"}
        except Exception as e:
            return {"status": "stopped", "detail": str(e)}
    return {"status": "not_running"}

# --- HTML Preview Endpoint ---

@app.get("/api/projects/{project_id}/preview")
def preview_project(project_id: int, db: Session = Depends(get_db)):
    from fastapi.responses import HTMLResponse
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    step = db.query(ProjectStep).filter_by(project_id=project_id, step_name="frontend_code").first()
    if not step or not step.content:
        return HTMLResponse("<html><body style='background:#0f172a;color:#64748b;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;'><div style='text-align:center;'><h3>No frontend code generated yet.</h3><p style='font-size:12px;color:#475569;'>Complete the Frontend Developer agent step to enable preview.</p></div></body></html>")
    
    from app.export_utils import generate_html_wrapper
    html_content = generate_html_wrapper(project.name, step.content)
    # Rewrite ports from 8000 -> 8080 since sandbox API runs on 8080!
    html_content = html_content.replace("http://localhost:8000", "http://localhost:8080")
    html_content = html_content.replace("http://127.0.0.1:8000", "http://localhost:8080")
    return HTMLResponse(content=html_content)

# --- ZIP Export Endpoint ---

@app.get("/api/projects/{project_id}/export")
def export_project(project_id: int, db: Session = Depends(get_db)):
    zip_buffer = create_project_zip(db, project_id)
    if not zip_buffer:
        raise HTTPException(status_code=404, detail="Project or steps not found")
    
    project = db.query(Project).filter_by(id=project_id).first()
    filename = f"{project.name.lower().replace(' ', '_')}_workspace.zip"
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

# --- Legacy Fallback for backwards compatibility ---
@app.post("/build")
def build_app(request: RequestModel):
    # Sequential fallback
    import requests
    # Run the stream handlers sequentially inside a simple dict response
    db = next(get_db())
    # Create a temporary project
    project = Project(name="Legacy Project", idea=request.idea, model_id="meta.llama3-8b-instruct-v1:0")
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Run steps synchronously
    req_chunks = list(orchestrator.stream_requirements(db, project.id))
    arch_chunks = list(orchestrator.stream_architecture(db, project.id))
    back_chunks = list(orchestrator.stream_backend_code(db, project.id))
    rev_chunks = list(orchestrator.stream_review(db, project.id))
    front_chunks = list(orchestrator.stream_frontend_code(db, project.id))
    qa_chunks = list(orchestrator.stream_qa(db, project.id))
    devops_chunks = list(orchestrator.stream_devops(db, project.id))
    
    return {
        "requirements": "".join(req_chunks),
        "architecture": "".join(arch_chunks),
        "backend_code": "".join(back_chunks),
        "review": "".join(rev_chunks),
        "frontend_code": "".join(front_chunks),
        "tests": "".join(qa_chunks),
        "deployment": "".join(devops_chunks)
    }