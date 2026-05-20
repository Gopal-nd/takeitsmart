# VISVESVARAYA TECHNOLOGICAL UNIVERSITY
### Belagavi-590018, Karnataka

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                     INTERNSHIP REPORT                        │
│                             ON                               │
│          “MULTI-AGENT AI SOFTWARE DEVELOPMENT PLATFORM”      │
│                                                              │
└──────────────────────────────────────────────────────────────┘

**Submitted in partial fulfillment of the requirements for the award of degree**
### BACHELORS OF ENGINEERING 
### IN
### ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING

---

**Submitted by:**  
**KAVYASHREE N (1SB22AI031)**

**Under the Guidance of:**

*   **Internal Guide:**  
    **Mr. S. Vanarasan**  
    Assistant Professor, Department of AIML  
    Sri Sairam College of Engineering, Anekal, Bengaluru  

*   **External Guide:**  
    **Mr. Mallikarjun Kumbar**  
    Director, Take It Smart, Bangalore  

---

### DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING 
### SRI SAIRAM COLLEGE OF ENGINEERING
##### ANEKAL, BENGALURU - 562106
##### ACADEMIC YEAR: 2025-2026

---
\pagebreak

## SRI SAIRAM COLLEGE OF ENGINEERING
##### ANEKAL, BENGALURU - 562106
### DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING

---

### CERTIFICATE

This is to certify that **KAVYASHREE N** bearing the USN **1SB22AI031** has carried out the **INDUSTRY INTERNSHIP – BINT803B** work entitled **“MULTI-AGENT AI SOFTWARE DEVELOPMENT PLATFORM”** in **TAKE IT SMART (OPC) PVT. LTD.**, Bengaluru for the partial fulfillment for the award of Bachelor of Engineering in Department of Artificial Intelligence and Machine Learning in Sri Sairam College of Engineering, Bengaluru under Visvesvaraya Technological University, Belagavi during the year 2025-2026.

---

<br><br><br>

______________________________________               ______________________________________
**Signature of the Head of Department**             **Signature of the Principal**  
**Dr. Sivaprakash C**                               **Dr. B Shadaksharappa**  
Head of the Department, AIML                         Principal  
Sri Sairam College of Engineering                    Sri Sairam College of Engineering  

<br><br>

**Name of Examiners:**  
1.  __________________________________  
2.  __________________________________  

**Signature with Date:**  
1.  __________________________________  
2.  __________________________________  

---
\pagebreak

## DECLARATION

I, **KAVYASHREE N**, hereby declare that I have successfully completed my internship titled **“Multi-Agent AI Software Development Platform”** at **Take It Smart (OPC) Pvt. Ltd.** during the VIII semester of the B.E. (AIML) degree at Sri Sairam College of Engineering, Anekal, Bangalore, under the esteemed guidance of **Mr. Mallikarjun Kumbar**, Director, Take It Smart (OPC) Pvt. Ltd. and **Mr. S. Vanarasan**, Assistant Professor, Department of Artificial Intelligence and Machine Learning in Sri Sairam College of Engineering, affiliated with Visvesvaraya Technological University. 

The work carried out during this internship is original and has not been submitted, either in part or in full, for any other degree or award in any university.

<br><br><br>

**Date:** 14/05/2026  
**Place:** Bengaluru  

<br><br>

**KAVYASHREE N (1SB22AI031)**

---
\pagebreak

## ACKNOWLEDGEMENT

I hereby thank the management of **Sri Sairam College of Engineering** for providing an opportunity to study in their esteemed institution and supporting this internship program.

I extend my sincere gratitude to **TAKE IT SMART (OPC) PVT. LTD.** and their dedicated engineering team for providing an insightful, challenging, and enriching experience in the field of **Artificial Intelligence, Multi-Agent Systems, and Full-Stack Engineering**. The training and hands-on exposure not only broadened my understanding of Large Language Models (LLMs) but also equipped me with production-grade software development skills aligned with current industry standards.

I am deeply grateful to our beloved Founder Chairman, **MJF. Lion Leo Muthu**, our esteemed CEO, **Dr. Sai Prakash Leo Muthu**, and our respected Chief Operating Officer, **Dr. R. Arunkumar**, for their unwavering support and kind encouragement.

I sincerely thank **Dr. B. Shadaksharappa**, Principal, Sri Sairam College of Engineering, Bengaluru, for his constant encouragement and support in nurturing a positive attitude among students.

I express my heartfelt gratitude and sincere thanks to **Dr. Sivaprakash C**, Professor and Head of the Department of AIML, Sri Sairam College of Engineering, Bengaluru, for his valuable guidance and support in facilitating the successful completion of my internship.

I take this opportunity to express my sincere thanks to my internal guide **Mr. S. Vanarasan**, Assistant Professor, Department of AIML, Sri Sairam College of Engineering, and my external guide **Mr. Mallikarjun Kumbar**, Director, Take It Smart (OPC) Pvt. Ltd., Bangalore, for guiding, mentoring, and encouraging me throughout my internship tenure.

I would also like to mention my special thanks to all the faculty members of the Department of Artificial Intelligence and Machine Learning, Sri Sairam College of Engineering, Bengaluru, for their valuable support and guidance.

Finally, I thank my family and friends who have been encouraging me constantly and inspiring me throughout my studies, without whom this internship would not have been possible.

---
\pagebreak

## ABSTRACT

This report presents a comprehensive summary of the professional internship completed at **Take It Smart (OPC) Pvt. Ltd.**, focusing on the research, system design, and complete implementation of a **Multi-Agent AI Software Development Platform**. 

The platform represents a state-of-the-art collaborative AI system that automates the entire software engineering lifecycle—from initial abstract requirement definition to complete architecture specification, backend API generation, frontend UI styling, code safety review, automated QA test script creation, background execution, and production packaging.

The system orchestrates seven specialized role-playing agents—Product Manager, System Architect, Backend Developer, Frontend Developer, Code Reviewer, QA Engineer, and DevOps Agent—interfacing through **Amazon Bedrock (Llama-3 models)**. 

Major technical innovations implemented in this project include:
1.  **Double-Layer Purity Engine:** Combines LLM prompt engineering with orchestrator-level parser tools (`clean_code_block`) that strip markdown backticks and conversational prose to ensure all saved code is 100% syntactically pure and compilable.
2.  **Auto-Deduplication Algorithm:** A stream cleaning utility that intercepts tokens and filters duplicate import statements on-the-fly, preventing LLM repetition loop corruption.
3.  **Surgical Dynamic JSX Parser:** Safely extracts the default component name export format (handling functions, classes, and variables) and rewrites port endpoints from port 8000 to 8080, enabling seamless client-server sandbox bindings.
4.  **Dual-Sandbox Execution Layer:** Executes isolated background backend Uvicorn processes alongside in-browser Babel dynamic transpile wrappers.
5.  **Dual-Tab Launcher Dashboard:** A sleek, glassmorphic React dashboard featuring a unified log stream, file manager, Monaco code workspace editor, and dual sandbox buttons allowing developers to test the live frontend or inspect the Swagger API Docs.

Overall, the internship successfully demonstrated the practical application of Artificial Intelligence, Multi-Agent Systems, Database Management, and Full-Stack Web Development in solving real-world educational and industrial software automation challenges.

---
\pagebreak

## TABLE OF CONTENTS

*   **Certificate**
*   **Declaration**
*   **Acknowledgement**
*   **Abstract**
*   **List of Figures**
*   **Chapter 1: Introduction**
    *   1.1 Overview of AI in Software Engineering
    *   1.2 Problem Statement & Limitations of Single-Agent LLMs
    *   1.3 Project Goal & Key Objectives
*   **Chapter 2: About the Company**
    *   2.1 Brief History of Take It Smart
    *   2.2 Core Product Sectors & Services
    *   2.3 Internship Program Objectives
*   **Chapter 3: Tasks Performed**
    *   3.1 Full-Stack Development Tasks
    *   3.2 Database & Database Modeling Tasks
    *   3.3 Multi-Agent Systems & Bedrock Orchestration
*   **Chapter 4: Methodology**
    *   4.1 Core System Architecture & Design
    *   4.2 Multi-Agent Orchestrator Pipeline
    *   4.3 Database Schema & ORM Model Definition
    *   4.4 Double-Layer Purity & Auto-Deduplication Logic
    *   4.5 Dynamic Client-Side Compiler Iframe Flow
*   **Chapter 5: Implementation**
    *   5.1 Stage-by-Stage Implementation Steps
        *   5.1.1 Stage 1: Idea Submission & Requirements Logging (PM)
        *   5.1.2 Stage 2: Technical Specifications & Data Schemas (Architect)
        *   5.1.3 Stage 3: Python FastAPI Backend Generation & Import Filtering (Backend Dev)
        *   5.1.4 Stage 4: React JSX Frontend Design & Import Stripping (Frontend Dev)
        *   5.1.5 Stage 5: Code Review, CORS, & Security Validation (Reviewer)
        *   5.1.6 Stage 6: QA Integration Testing & Automated Test Cases (QA)
        *   5.1.7 Stage 7: Subprocess Sandboxing & Live Port Bindings (8080)
        *   5.1.8 Stage 8: Dynamic Iframe Rendering & Error Handling
        *   5.1.9 Stage 9: Zip Workspace Packaging & Dockerization
    *   5.2 System Requirements
        *   5.2.1 Hardware Requirements
        *   5.2.2 Software Requirements
        *   5.2.3 Libraries and Packages Used
*   **Chapter 6: Screenshots & Live Demonstration**
*   **Chapter 7: Reflection Notes**
    *   7.1 Technical Learnings
    *   7.2 Professional & Non-Technical Outcomes
*   **Chapter 8: Conclusion**

---
\pagebreak

## LIST OF FIGURES

| Figure No. | Title | Page No. |
| :--- | :--- | :--- |
| **Figure 1** | Conceptual Multi-Agent Orchestrator Pipeline | 14 |
| **Figure 2** | Platform System Design & Subprocess Architecture | 15 |
| **Figure 3** | Database Schema Entity Relationship Diagram | 17 |
| **Figure 4** | Double-Layer Code Cleaning & Deduplication Pipeline | 19 |
| **Figure 5** | Dynamic Client-Side Iframe Compiler Flowchart | 21 |
| **Figure 6** | Platform Workspace Dashboard & Monaco Code Editor | 29 |
| **Figure 7** | Multi-Agent Terminal Logs & Streaming SSE Output | 30 |
| **Figure 8** | Interactive Sandboxed Frontend Application Preview | 31 |
| **Figure 9** | FastAPI Interactive OpenAPI/Swagger API Docs Portal | 32 |
| **Figure 10** | Dynamic Error Boundary Runtime Exception Overlay | 33 |

---
\pagebreak

## CHAPTER 1: INTRODUCTION

### 1.1 Overview of AI in Software Engineering
The integration of Artificial Intelligence into software engineering has evolved rapidly from simple autocomplete utilities to complex generative systems capable of producing entire code blocks. Large Language Models (LLMs) trained on vast repositories of open-source code show remarkable proficiency in understanding natural language and translating it into syntactically valid programming structures in Python, JavaScript, SQL, HTML, and CSS. 

However, writing individual code snippets represents only a small portion of the software development lifecycle. Building real-world, production-ready applications requires coordinated requirements gathering, architectural planning, interface design, security reviews, unit testing, and deployment orchestration.

### 1.2 Problem Statement & Limitations of Single-Agent LLMs
While modern LLMs can generate high-quality code, utilizing a single LLM agent to construct complete full-stack applications suffers from severe operational limitations:
1.  **Context Length Constraints:** A single chat context quickly becomes bloated when storing backend routers, frontend screens, database classes, and testing suites. This leads to context decay, where the model forgets core system boundaries, leading to broken imports, database schema mismatches, and syntax errors.
2.  **Lack of Specialized Logic:** A single general prompt forces the LLM to behave simultaneously as a designer, backend programmer, tester, and reviewer, which dilutes output quality.
3.  **Code Truncation:** Large code files often hit the LLM generation length limit, resulting in half-written functions, unclosed brackets, and broken files.
4.  **Markdown/Conversational Noise:** LLMs naturally wrap their outputs in explanatory paragraphs, introductions, and remarks. Directly saving this output into code files breaks the compiler or parser.

### 1.3 Project Goal & Key Objectives
The primary goal of this project is to develop the **Multi-Agent AI Software Development Platform**—a collaborative platform that partitions software engineering responsibilities among a cooperative team of intelligent, specialized AI agents. The key objectives are:
*   Divide requirements gathering, database schema definition, API writing, interface layout, code review, unit testing, and packaging among seven distinct, cooperative agents.
*   Enforce a **Double-Layer Purity Engine** to automatically extract and save raw, executable code by stripping markdown blocks, conversational noise, and repetitive imports.
*   Configure a **Dynamic Client-Side React Compiler** that transpiles JSX dynamically in the browser using Babel CDN, linking it seamlessly with a sandboxed FastAPI backend.
*   Incorporate a **Dual-Sandbox runtime environment** running FastAPI backends on port 8080 and compiled frontends in a dual-tab viewer (Frontend Preview vs. Swagger API Docs).
*   Provide complete workspace packaging (comprising backends, frontends, unit tests, and Docker containers) for immediate execution.

---
\pagebreak

## CHAPTER 2: ABOUT THE COMPANY

### 2.1 Brief History of Take It Smart
**Take It Smart (OPC) Pvt. Ltd.** was established in the year 2018 in Bangalore, Karnataka, as a specialized engineering and software development consulting organization. It was officially registered as a private organization in the year 2021. The firm operates as a dual-channel developer: building in-house smart software products in data science and computer vision, and providing software services, mobile applications, and cloud-native solutions to industrial clients.

### 2.2 Core Product Sectors & Services
Take It Smart specializes in:
*   **Artificial Intelligence Solutions:** Developing intelligent face recognition portals, predictive data analytics pipelines, and natural language interfaces.
*   **Web & Mobile Engineering:** Building responsive full-stack applications, interactive data dashboards, and mobile utility applications.
*   **Industrial IoT & Embedded Systems:** Constructing smart monitoring systems, automated camera controllers, and sensor network interfaces.
*   **Research & Mentorship:** Mentoring undergraduate and graduate interns in engineering projects, cloud technologies, database modeling, and state-of-the-art deep learning architectures.

### 2.3 Internship Program Objectives
The AIML internship program at Take It Smart is designed to bridge the gap between academic theory and industry engineering practices. The objectives are to:
*   Gain deep hands-on exposure to full-stack engineering frameworks like FastAPI, SQLAlchemy, SQLite, React, and Tailwind CSS.
*   Understand advanced AI system orchestration using Bedrock SDK, prompt engineering, and FAISS vector databases.
*   Implement production-grade practices like background subprocess tracking, dynamic error boundaries, CORS security configurations, and containerized deployment pipelines.

---
\pagebreak

## CHAPTER 3: TASKS PERFORMED

During the internship at Take It Smart, I successfully completed the following engineering and implementation tasks:

1.  **FastAPI REST Architecture Engineering:** Wrote the core application routing, SSE streaming generator helpers, dynamic sandbox runners, and export controllers.
2.  **SQLite Database Modeling:** Designed the SQLite schema and configured SQLAlchemy ORM tables to manage projects and steps with cascade deletion logic.
3.  **Monaco Code Editor Configuration:** Integrated `@monaco-editor/react` inside the React client workspace, configuring active tab tracking, dark themes, automatic layouts, and local save callbacks.
4.  **Babel Iframe Compiler Construction:** Wrote the dynamic iframe wrapper that loads React 18, Babel Standalone, Axios, and Tailwind CSS, transpiling raw JSX inside the client browser.
5.  **Multi-Agent Orchestrator Core:** Built the multi-agent orchestrator (`SoftwareTeamOrchestrator`) that drives step-by-step agent triggers and memory recall searches using FAISS.
6.  **Purity Engine & Deduplicator Implementation:** Developed the code cleaning and import deduplication logic to sanitize LLM code outputs.
7.  **Process Sandboxing & Subprocess Control:** Managed background Uvicorn servers using `subprocess.Popen` and implemented clean process killing via `os.killpg`.

---
\pagebreak

## CHAPTER 4: METHODOLOGY

### 4.1 Core System Architecture & Design
The Multi-Agent AI Software Development Platform is designed as a modular, decoupled full-stack platform. The architecture comprises a **React Client Dashboard**, a **FastAPI Core Orchestrator API**, a **Local SQLite Transactional Database**, and a **Sandboxed Application Runtime (Port 8080)**.

┌────────────────────────────────────────────────────────┐
│                                                        │
│       [PLACEHOLDER: Figure 2 - Subprocess Architecture]│
│                                                        │
└────────────────────────────────────────────────────────┘

The system coordinates the user interface, backend server, database, and sandbox environment as follows:
*   The **React Client** communicates with the FastAPI main server using standard REST calls and Server-Sent Events (SSE) for streaming text.
*   The **FastAPI main server** manages data schemas via SQLAlchemy and stores project data in the SQLite database.
*   The **Bedrock Runtime** is invoked dynamically at each stage, loading specific agent system prompts and querying the local FAISS vector store memory.
*   When sandbox execution is triggered, the main server launches a child process using `subprocess.Popen`, running a background Uvicorn instance on port 8080.
*   The React client renders an `<iframe>` targeting port 8080, mounting the compiled frontend dynamically.

### 4.2 Multi-Agent Orchestrator Pipeline
The software development process is divided into a structured pipeline driven by specialized AI agents:

┌────────────────────────────────────────────────────────┐
│                                                        │
│      [PLACEHOLDER: Figure 1 - Multi-Agent Pipeline]    │
│                                                        │
└────────────────────────────────────────────────────────┘

1.  **Product Manager Agent:** Accepts abstract user prompts (e.g., "Build a fitness tracker dashboard") and drafts detailed product requirements (PRD).
2.  **System Architect Agent:** Processes the PRD and compiles a complete system architecture specification, defining relational data models and API paths.
3.  **Backend Developer Agent:** Reads the architecture specifications and outputs pure FastAPI Python code, complete with CORS middlewares and in-memory mock data.
4.  **Frontend Developer Agent:** Builds a fully responsive, Tailwind CSS-styled React single-page application based on the architecture specs.
5.  **Code Reviewer Agent:** Audits the backend and frontend code for import accuracy, secure CORS parameters, and exception handling.
6.  **QA Engineer Agent:** Writes a robust unit testing suite using `pytest` to validate all API endpoints.
7.  **DevOps Agent:** Formulates the final packaging assets, creating Dockerfiles, dependency lists (`requirements.txt`), and automated start scripts.

### 4.3 Database Schema & ORM Model Definition
The platform uses SQLite as its metadata and state management storage engine. The data models are designed to enable transactional safety and support clean cascade deletions:

┌────────────────────────────────────────────────────────┐
│                                                        │
│     [PLACEHOLDER: Figure 3 - Entity Relationship Diagram]│
│                                                        │
└────────────────────────────────────────────────────────┘

The relational tables are configured as follows:
1.  **`projects` table:** Tracks project metadata and lifecycle state:
    *   `id` (Integer, Primary Key, autoincrement)
    *   `name` (String, Non-Nullable)
    *   `idea` (Text, Non-Nullable)
    *   `model_id` (String, Nullable)
    *   `temperature` (Float, Default: 0.2)
    *   `status` (String, Default: "created") - represents the active phase: `created`, `requirements`, `architecture`, `code_backend`, `code_frontend`, `qa`, or `completed`.
    *   `created_at` (DateTime, Default: UTC Now)
2.  **`project_steps` table:** Stores step-specific outputs with foreign key links and cascade deletion:
    *   `id` (Integer, Primary Key, autoincrement)
    *   `project_id` (Integer, Foreign Key linking to `projects.id`, cascade delete-orphan enabled)
    *   `step_name` (String, Non-Nullable) - `requirements`, `architecture`, `backend_code`, `frontend_code`, `review`, `tests`, `deployment`
    *   `content` (Text, Non-Nullable)
    *   `updated_at` (DateTime, Default: UTC Now, onupdate: UTC Now)

### 4.4 Double-Layer Purity & Auto-Deduplication Logic
To prevent LLM conversational noise, markdown blocks, and import repetition loops from corrupting files, the platform implements a robust two-layer purity and auto-deduplication system:

┌────────────────────────────────────────────────────────┐
│                                                        │
│     [PLACEHOLDER: Figure 4 - Double-Layer Code Clean]  │
│                                                        │
└────────────────────────────────────────────────────────┘

#### Layer 1: Prompt Constraint
All agent prompts are appended with a strict instruction:
> *CRITICAL OUTPUT RULE: Your response must consist EXCLUSIVELY of the code inside the code block. Do NOT write any introductory explanations, conversational prefaces, or concluding descriptions before or after the code block. It must start directly with the markdown code block and end directly with the closing backticks.*

#### Layer 2: Orchestrator Purity & Import Deduplication
When the stream finishes, `save_step_content` automatically passes the text to `clean_code_block()`. It splits away any external text, extracts the raw content inside the markdown backticks, and performs an O(N) deduplication sweep:
```python
def clean_code_block(text: str) -> str:
    cleaned = text
    if "```" in text:
        parts = text.split("```")
        code_blocks = []
        for i, part in enumerate(parts):
            if i % 2 == 1:
                lines = part.split("\n")
                if lines and (lines[0].strip().lower() in ["python", "javascript", "js", "html", "css", "jsx"]):
                    code_blocks.append("\n".join(lines[1:]))
                else:
                    code_blocks.append(part)
        if code_blocks:
            cleaned = "\n\n".join(code_blocks).strip()
    else:
        cleaned = text.strip()

    # Deduplicate repeated imports to prevent LLM loops from corrupting code
    lines = cleaned.split("\n")
    seen_imports = set()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            norm = " ".join(stripped.split())
            if norm in seen_imports:
                continue # Skip duplicate imports
            seen_imports.add(norm)
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()
```

### 4.5 Dynamic Client-Side Compiler Iframe Flow
To compile and preview React components inside the browser without requiring external build pipelines (Vite/webpack), the system uses an in-browser compilation workflow inside the client-side dashboard:

┌────────────────────────────────────────────────────────┐
│                                                        │
│     [PLACEHOLDER: Figure 5 - Dynamic Iframe Compiler]  │
│                                                        │
└────────────────────────────────────────────────────────┘

1.  **Read Step:** The client reads the `frontend_code` from the selected project steps.
2.  **Surgical Component Name Matching:** The dynamic compiler extracts the React component name from `export default` statements, resolving functions, classes, and variables safely:
    ```javascript
    let componentName = 'App';
    const funcMatch = rawCode.match(/export\s+default\s+function\s+(\w+)/);
    if (funcMatch) {
      componentName = funcMatch[1];
    } else {
      const classMatch = rawCode.match(/export\s+default\s+class\s+(\w+)/);
      if (classMatch) {
        componentName = classMatch[1];
      } else {
        const varMatch = rawCode.match(/export\s+default\s+(\w+)/);
        if (varMatch && varMatch[1] !== 'function' && varMatch[1] !== 'class') {
          componentName = varMatch[1];
        }
      }
    }
    ```
3.  **Strip Exports & Imports:** Removes ES6 block imports and `export default` statements to prevent browser errors.
4.  **Rewrite Port Endpoints:** Dynamically replaces all instances of `http://localhost:8000` or `127.0.0.1:8000` with `http://localhost:8080` to route backend API requests to the active sandbox backend.
5.  **Compile with Babel:** Mounts React 18, Babel Standalone, Axios, and Tailwind CSS. Babel transpiles the JSX in real-time, wraps the component inside an `<ErrorBoundary />`, and mounts it to `document.getElementById('root')`.

---
\pagebreak

## CHAPTER 5: IMPLEMENTATION

### 5.1 Stage-by-Stage Implementation Steps

#### 5.1.1 Stage 1: Idea Submission & Requirements Logging (PM)
The user enters a project concept into the platform. The main FastAPI backend logs this entry in the SQLite `projects` database. The `SoftwareTeamOrchestrator` triggers `stream_requirements`, creating a streaming SSE thread powered by the **Product Manager Agent**. The PM agent translates the idea into a comprehensive PRD, which is stored in the `project_steps` table.

#### 5.1.2 Stage 2: Technical Specifications & Data Schemas (Architect)
Once requirements are logged, `stream_architecture` is triggered. The **System Architect Agent** processes the PRD and defines the technical layout, listing out schemas, entity relationships, and REST API paths.

#### 5.1.3 Stage 3: Python FastAPI Backend Generation & Import Filtering (Backend Dev)
With the architecture specification complete, the **Backend Developer Agent** runs to generate the backend code. The orchestrator streams the code block, sanitizes it using the Double-Layer Purity Engine, and applies the auto-deduplicator to filter out duplicate imports. The pure code is written to the database.

#### 5.1.4 Stage 4: React JSX Frontend Design & Import Stripping (Frontend Dev)
The **Frontend Developer Agent** reads the architecture specification and builds a React single-page application complete with interactive state hooks, forms, graphs, and Tailwind-styled panels.

#### 5.1.5 Stage 5: Code Review, CORS, & Security Validation (Reviewer)
The **Code Reviewer Agent** audits the backend and frontend code. It verifies that CORS is configured with `allow_origins=["*"]`, all backend endpoints are wrapped in robust try-except error handlers, and frontend components use proper state initializations.

#### 5.1.6 Stage 6: QA Integration Testing & Automated Test Cases (QA)
The **QA Engineer Agent** generates a robust Python test file `test_main.py` using `pytest`. The test file contains unit and integration tests covering every endpoint designed in the architecture to validate response schemas, query validation parameters, and error status codes.

#### 5.1.7 Stage 7: Subprocess Sandboxing & Live Port Bindings
When the developer clicks **⚡ Run Sandbox App**, the FastAPI main server writes the backend code to `app/sandbox_app.py` and spawns a child process:
```python
cmd = [sys.executable, "-m", "uvicorn", "app.sandbox_app:app", "--host", "0.0.0.0", "--port", "8080"]
proc = subprocess.Popen(cmd, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```
The Uvicorn backend starts dynamically on port 8080, loading database records or mock data.

#### 5.1.8 Stage 8: Dynamic Iframe Rendering & Error Handling
The React application loads the Dynamic Iframe. The dynamic code runs, transpiling JSX on-the-fly. If any Javascript runtime error occurs, the `<ErrorBoundary />` intercepts the exception and displays an overlay detailing the exception name and debugging tips.

#### 5.1.9 Stage 9: Zip Workspace Packaging & Dockerization
When the developer clicks **📥 Export**, the backend creates an in-memory ZIP archive including:
*   `backend/main.py`: The auto-deduplicated FastAPI code.
*   `frontend/App.jsx`: The clean React JSX component.
*   `tests/test_main.py`: The pytest suite.
*   `backend/Dockerfile` and `backend/requirements.txt`: For containerization.
*   `docker-compose.yml`: For instant multi-container deployment.
*   `start.sh`: A shell script to boot the full Docker stack.

### 5.2 System Requirements

#### 5.2.1 Hardware Requirements
*   **Processor:** Intel Core i5 / AMD Ryzen 5 or higher.
*   **RAM:** 8 GB minimum (16 GB recommended).
*   **Storage:** 5 GB free SSD space.
*   **Network:** High-speed internet connection for Bedrock API calls and loading dynamic CDNs inside the sandboxed iframe.

#### 5.2.2 Software Requirements
*   **Operating System:** Linux (Ubuntu 20.04+ / Debian 11+), macOS, or Windows 10/11 with WSL2.
*   **Runtime Environments:** Python 3.10+ and Node.js 18+.
*   **Package Managers:** Poetry (for backend Python environments) and npm (for React dev servers).
*   **Database:** SQLite3.

#### 5.2.3 Libraries and Packages Used
*   **FastAPI & Uvicorn:** Drives the core orchestrator server and the sandboxed background runtimes.
*   **SQLAlchemy ORM:** Maps Python objects to SQLite tables with relational integrity.
*   **Boto3 SDK:** Connects to Amazon Bedrock to invoke Llama-3 models.
*   **FAISS & Sentence Transformers:** Powers vector storage and semantic search memory recall.
*   **Monaco Editor:** A high-fidelity code editor integrated inside the workspace page.
*   **Babel Standalone:** Transpiles React JSX in the browser dynamically.
*   **Axios:** Executes REST API calls between the compiled client React UI and the sandbox backend.

---
\pagebreak

## CHAPTER 6: SCREENSHOTS & LIVE DEMONSTRATION

This section contains placeholders for the visual screens and runtime execution interfaces of the Multi-Agent AI Software Development Platform:

┌────────────────────────────────────────────────────────┐
│                                                        │
│    [PLACEHOLDER: Figure 6 - Platform Workspace UI]     │
│                                                        │
└────────────────────────────────────────────────────────┘
*Figure 6: The main platform dashboard displaying the Monaco Code Editor on the right, the project selector sidebar on the left, and the workspace action panels.*

┌────────────────────────────────────────────────────────┐
│                                                        │
│    [PLACEHOLDER: Figure 7 - Streaming SSE Logs]        │
│                                                        │
└────────────────────────────────────────────────────────┘
*Figure 7: Server-Sent Events (SSE) log console output, streaming token-by-token reasoning steps from the Product Manager and Architect agents.*

┌────────────────────────────────────────────────────────┐
│                                                        │
│    [PLACEHOLDER: Figure 8 - Sandboxed Frontend App]    │
│                                                        │
└────────────────────────────────────────────────────────┘
*Figure 8: Interactive compiled React UI displaying a generated application preview. All form inputs and buttons connect to the sandbox Uvicorn backend on port 8080.*

┌────────────────────────────────────────────────────────┐
│                                                        │
│    [PLACEHOLDER: Figure 9 - Swagger OpenAPI Portal]    │
│                                                        │
└────────────────────────────────────────────────────────┘
*Figure 9: The interactive FastAPI Swagger OpenAPI interface running on `http://localhost:8080/docs`, allowing live testing of the generated backend APIs.*

┌────────────────────────────────────────────────────────┐
│                                                        │
│    [PLACEHOLDER: Figure 10 - Runtime Error Boundary]   │
│                                                        │
└────────────────────────────────────────────────────────┘
*Figure 10: The sleek, glassmorphic Error Boundary overlay, capturing a JavaScript runtime exception and displaying debugging tips.*

---
\pagebreak

## CHAPTER 7: REFLECTION NOTES

### 7.1 Technical Learnings
During this internship, I gained valuable practical knowledge in:
1.  **Multi-Agent Collaborative Design:** Designing modular agent structures where each agent has specialized instructions and system prompts, which significantly improves code generation quality compared to general single-agent models.
2.  **Robust Code Cleaning Pipelines:** Implementing double-layered code sanitation filters (`clean_code_block`) inside the orchestrator is critical when developing code generation tools, as it prevents conversational noise and formatting anomalies from breaking compilation.
3.  **Isolated Background Process Management:** Spawning, tracking, and cleanly terminating independent background processes via Python's `subprocess.Popen` and `os.killpg` prevents process leaks and port conflicts in multi-project sandboxed environments.
4.  **Babel dynamic transpilation:** Configuring in-browser JSX transpilation using Babel Standalone allows developers to test React UIs dynamically without complex web build chains.
5.  **Secure CORS Configurations:** Configuring robust CORS settings in backend and review steps is essential to enable secure cross-origin communication between the dynamic frontend and the sandboxed APIs.

### 7.2 Professional & Non-Technical Outcomes
Apart from core engineering competencies, the internship contributed to:
*   **Analytical Thinking:** Investigating blank iframe screens in a sandboxed runtime requires checking console errors, Babel compiler states, CORS setups, and regex matches systematically.
*   **Time Management & Prioritization:** Completing complex, multi-stage engineering tasks within strict project deadlines highlighted the importance of project planning and step-by-step progress tracking.
*   **Technical Documentation & Presentation:** Presenting system designs, data models, and workflow diagrams during code reviews significantly improved my technical writing and verbal communication skills.

---
\pagebreak

## CHAPTER 8: CONCLUSION

The **Multi-Agent AI Software Development Platform** successfully demonstrates the power of collaborative AI engineering. By combining specialized role-playing agents, robust code cleaning pipelines, real-time background sandboxing, and dynamic in-browser React compilation, the platform bridges the gap between abstract user ideas and fully working full-stack applications.

The successful implementation of this platform proves that multi-agent systems are highly capable of automating complex, multi-stage software engineering lifecycles. It represents a significant step forward in automated prototyping, educational sandboxing, and intelligent full-stack software development workflows.
