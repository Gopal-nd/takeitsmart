import io
import re
import zipfile
from sqlalchemy.orm import Session
from app.database import Project, ProjectStep

def clean_code_block(text: str) -> str:
    cleaned = text
    if "```" in text:
        parts = text.split("```")
        code_blocks = []
        for i, part in enumerate(parts):
            if i % 2 == 1:
                lines = part.split("\n")
                if lines and (lines[0].strip().lower() in ["python", "javascript", "js", "html", "css", "bash", "sh", "yaml", "yml", "json", "jsx"]):
                    code_blocks.append("\n".join(lines[1:]))
                else:
                    code_blocks.append(part)
        if code_blocks:
            cleaned = "\n\n".join(code_blocks).strip()
    else:
        cleaned = text.strip()

    # Deduplicate repeated imports to prevent LLM infinite repetition bugs from corrupting code
    lines = cleaned.split("\n")
    seen_imports = set()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            norm = " ".join(stripped.split())
            if norm in seen_imports:
                continue
            seen_imports.add(norm)
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

def generate_html_wrapper(project_name: str, react_code: str) -> str:
    # Extract component name safely
    func_match = re.search(r'export\s+default\s+function\s+(\w+)', react_code)
    if func_match:
        component_name = func_match.group(1)
    else:
        class_match = re.search(r'export\s+default\s+class\s+(\w+)', react_code)
        if class_match:
            component_name = class_match.group(1)
        else:
            var_match = re.search(r'export\s+default\s+(\w+)', react_code)
            if var_match and var_match.group(1) not in ['function', 'class']:
                component_name = var_match.group(1)
            else:
                component_name = 'App'
    
    cleaned_code = clean_code_block(react_code)
    cleaned_code = re.sub(r"import\s+[\s\S]*?from\s+['\"].*?['\"];?", "", cleaned_code)
    cleaned_code = re.sub(r"import\s+['\"].*?['\"];?", "", cleaned_code)
    cleaned_code = re.sub(r"export\s+default\s+", "", cleaned_code)
    cleaned_code = re.sub(r"\bexport\s+", "", cleaned_code)
    
    # In a real deployed Docker environment, the client browser connects to port 8000 on localhost
    cleaned_code = cleaned_code.replace("http://localhost:8000", "http://localhost:8000")
    cleaned_code = cleaned_code.replace("http://127.0.0.1:8000", "http://localhost:8000")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name} - Live Portal</title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body {{
      background-color: #0f172a;
      color: #f8fafc;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}
  </style>
</head>
<body class="p-6">
  <div id="root"></div>

  <script type="text/babel">
    const {{ useState, useEffect, useRef }} = React;
    
    {cleaned_code}

    try {{
      const root = ReactDOM.createRoot(document.getElementById('root'));
      if (typeof {component_name} !== 'undefined') {{
        root.render(<{component_name} />);
      }} else if (typeof App !== 'undefined') {{
        root.render(<App />);
      }} else {{
        document.getElementById('root').innerHTML = '<div style="text-align:center;padding:50px;color:#f43f5e;"><h3>Could not locate App component</h3></div>';
      }}
    }} catch(e) {{
      console.error(e);
      document.getElementById('root').innerHTML = '<div style="text-align:center;padding:50px;color:#f43f5e;"><h3>Compilation Error</h3><pre style="text-align:left;background:#1e293b;padding:15px;border-radius:10px;font-size:11px;overflow-x:auto;color:#f8fafc;">' + e.message + '</pre></div>';
    }}
  </script>
</body>
</html>"""

def create_project_zip(db: Session, project_id: int) -> io.BytesIO:
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        return None
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # Add basic project documentation and Docker guide
        readme_content = f"""# {project.name}

Generated dynamically by the AI Software Team Agent Platform.

## 🚀 How to Run (Using Docker Stack)

Ensure you have Docker and Docker Compose installed, then spin up the entire multi-container application stack with a single command:

```bash
docker compose up --build
```

Once running:
- 🖥️ **Stunning Interactive Frontend:** Open [http://localhost:8080](http://localhost:8080)
- ⚙️ **FastAPI REST API Docs:** Open [http://localhost:8000/docs](http://localhost:8000/docs)

## 📁 Directory Structure
- `backend/`: FastAPI Python server with autogenerated CRUD endpoints
- `frontend/`: Standalone React + Tailwind CSS client portal served via Nginx
- `docker-compose.yml`: Multi-container architecture configuration
"""
        zip_file.writestr("README.md", readme_content)
        
        # Add root docker-compose.yml
        compose_content = """version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./sql_app.db

  frontend:
    build: ./frontend
    ports:
      - "8080:80"
    depends_on:
      - backend
"""
        zip_file.writestr("docker-compose.yml", compose_content)
        
        steps = db.query(ProjectStep).filter_by(project_id=project_id).all()
        frontend_src = ""
        backend_src = ""
        
        for step in steps:
            content = step.content
            if step.step_name == "requirements":
                zip_file.writestr("docs/requirements.md", content)
            elif step.step_name == "architecture":
                zip_file.writestr("docs/architecture.md", content)
            elif step.step_name == "backend_code":
                backend_src = clean_code_block(content)
                zip_file.writestr("backend/main.py", backend_src)
            elif step.step_name == "frontend_code":
                frontend_src = content
                code = clean_code_block(content)
                zip_file.writestr("frontend/App.jsx", code)
            elif step.step_name == "tests":
                code = clean_code_block(content)
                zip_file.writestr("tests/test_main.py", code)
            elif step.step_name == "deployment":
                zip_file.writestr("deployment/deploy.md", content)
        
        # Write backend container files
        backend_dockerfile = """FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        backend_reqs = """fastapi
uvicorn
sqlalchemy
pydantic
requests
"""
        zip_file.writestr("backend/Dockerfile", backend_dockerfile)
        zip_file.writestr("backend/requirements.txt", backend_reqs)
        
        # Write frontend container files using Nginx + stunning React HTML wrapper
        if frontend_src:
            wrapped_html = generate_html_wrapper(project.name, frontend_src)
            zip_file.writestr("frontend/index.html", wrapped_html)
        else:
            dummy_html = "<html><body><h3>Application UI is being generated...</h3></body></html>"
            zip_file.writestr("frontend/index.html", dummy_html)
            
        frontend_dockerfile = """FROM nginx:alpine
COPY index.html /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
        zip_file.writestr("frontend/Dockerfile", frontend_dockerfile)
                
    zip_buffer.seek(0)
    return zip_buffer
