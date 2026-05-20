import os
import math
from PIL import Image, ImageDraw, ImageFont

# Ensure screenshots directory exists
os.makedirs("screenshots", exist_ok=True)

# Select modern, clean sans-serif font
font_path = "/usr/share/fonts/Adwaita/AdwaitaSans-Regular.ttf"
if not os.path.exists(font_path):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not os.path.exists(font_path):
    font_path = None  # Fallback to default

def get_fonts(font_file, font_size):
    if font_file:
        try:
            return (
                ImageFont.truetype(font_file, font_size),
                ImageFont.truetype(font_file, max(12, int(font_size * 0.8))),
                ImageFont.truetype(font_file, max(14, int(font_size * 1.2)))
            )
        except Exception:
            pass
    return ImageFont.load_default(), ImageFont.load_default(), ImageFont.load_default()

def draw_arrow(draw, start, end, color=(100, 116, 139), width=2):
    # Draw line
    draw.line([start, end], fill=color, width=width)
    
    # Draw arrowhead
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    angle = math.atan2(dy, dx)
    
    arrow_length = 12
    arrow_angle = math.pi / 6 # 30 degrees
    
    p1 = (x1 - arrow_length * math.cos(angle - arrow_angle), y1 - arrow_length * math.sin(angle - arrow_angle))
    p2 = (x1 - arrow_length * math.cos(angle + arrow_angle), y1 - arrow_length * math.sin(angle + arrow_angle))
    
    draw.polygon([end, p1, p2], fill=color)

def draw_card(draw, size, title, bg_color=(248, 250, 252)):
    # Clean card outline and background
    w, h = size
    draw.rounded_rectangle([10, 10, w - 10, h - 10], radius=15, fill=bg_color, outline=(226, 232, 240), width=2)

def draw_flat_node(draw, center, radius, color, step_num, title, lines):
    # Soft background circle
    x, y = center
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
    
    # White icon circle inside
    draw.ellipse([x - radius + 15, y - radius + 15, x + radius - 15, y + radius - 15], fill=(255, 255, 255))
    
    # Step Number Text inside circle
    num_font = get_fonts(font_path, 20)[2]
    draw.text((x - 8, y - 12), str(step_num), fill=color, font=num_font)
    
    # Node Title (Bold text below)
    font, sub_font, _ = get_fonts(font_path, 14)
    draw.text((x - 90, y + radius + 12), title, fill=(15, 23, 42), font=font)
    
    # Subtitle details below
    curr_y = y + radius + 32
    for line in lines:
        draw.text((x - 90, curr_y), line, fill=(100, 116, 139), font=sub_font)
        curr_y += 18

# ==========================================
# FIGURE 1: Conceptual Agent Pipeline
# ==========================================
def make_fig1():
    w, h = 1200, 700
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_card(draw, (w, h), "Figure 1: Conceptual Multi-Agent Orchestrator Pipeline")
    
    # Coordinates of 8 snake-like stages
    nodes = [
        {"num": 1, "center": (150, 180), "color": (59, 130, 246), "title": "1. User Idea Input", "desc": ["Abstract project description", "Admin triggers execution"]},
        {"num": 2, "center": (420, 180), "color": (16, 185, 129), "title": "2. Product Manager", "desc": ["Requirements Gathering", "Drafts detailed PRD & stories"]},
        {"num": 3, "center": (700, 180), "color": (245, 158, 11), "title": "3. System Architect", "desc": ["API Specifications", "Designs SQL database models"]},
        {"num": 4, "center": (980, 180), "color": (139, 92, 246), "title": "4. Backend Developer", "desc": ["FastAPI Routing Engine", "Extracts pure Python code"]},
        
        {"num": 5, "center": (980, 480), "color": (236, 72, 153), "title": "5. Frontend Developer", "desc": ["Tailwind CSS React SPA", "Builds UI views & inputs"]},
        {"num": 6, "center": (700, 480), "color": (6, 182, 212), "title": "6. Code Reviewer", "desc": ["Security Validation", "Audits CORS, errors & imports"]},
        {"num": 7, "center": (420, 480), "color": (239, 68, 68), "title": "7. QA Engineer", "desc": ["Automated pytest", "Validates response structures"]},
        {"num": 8, "center": (150, 480), "color": (100, 116, 139), "title": "8. Sandbox Runtime", "desc": ["Live Uvicorn Server", "Binds dynamically to port 8080"]}
    ]
    
    # Draw Nodes
    for n in nodes:
        draw_flat_node(draw, n["center"], 45, n["color"], n["num"], n["title"], n["desc"])
        
    # Draw Connecting Arrows
    draw_arrow(draw, (205, 180), (365, 180)) # 1 -> 2
    draw_arrow(draw, (475, 180), (645, 180)) # 2 -> 3
    draw_arrow(draw, (755, 180), (925, 180)) # 3 -> 4
    
    draw_arrow(draw, (980, 245), (980, 415)) # 4 -> 5 (down)
    
    draw_arrow(draw, (925, 480), (755, 480)) # 5 -> 6 (left)
    draw_arrow(draw, (645, 480), (475, 480)) # 6 -> 7 (left)
    draw_arrow(draw, (365, 480), (205, 480)) # 7 -> 8 (left)
    
    img.save("screenshots/fig1_agent_pipeline.png")

# ==========================================
# FIGURE 2: System Design & Subprocess
# ==========================================
def make_fig2():
    w, h = 1000, 700
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_card(draw, (w, h), "Figure 2: Platform System Design & Subprocess Architecture")
    
    font, sub_font, title_font = get_fonts(font_path, 13)
    
    # Component Blocks
    # 1. React SPA Front (Left Top)
    draw.rounded_rectangle([50, 100, 350, 220], radius=10, fill=(239, 246, 255), outline=(59, 130, 246), width=2)
    draw.text((70, 120), "Client React Dashboard (Port 5173)", fill=(15, 23, 42), font=title_font)
    draw.text((70, 150), "- Monaco Workspace Editor", fill=(100, 116, 139), font=font)
    draw.text((70, 175), "- Unified Agent Logs Console", fill=(100, 116, 139), font=font)
    draw.text((70, 195), "- Iframe Preview Component", fill=(100, 116, 139), font=font)
    
    # 2. Main API Server (Left Bottom)
    draw.rounded_rectangle([50, 320, 350, 480], radius=10, fill=(240, 253, 250), outline=(16, 185, 129), width=2)
    draw.text((70, 340), "FastAPI Orchestrator (Port 8000)", fill=(15, 23, 42), font=title_font)
    draw.text((70, 370), "- Project & Steps SQLite Manager", fill=(100, 116, 139), font=font)
    draw.text((70, 395), "- SSE Real-Time Streaming Server", fill=(100, 116, 139), font=font)
    draw.text((70, 420), "- Double-Layer Purity Engine", fill=(100, 116, 139), font=font)
    draw.text((70, 445), "- Subprocess Group Manager", fill=(100, 116, 139), font=font)
    
    # 3. Amazon Bedrock Gateway
    draw.rounded_rectangle([50, 530, 350, 630], radius=10, fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.text((70, 550), "Amazon Bedrock SDK Gateway", fill=(15, 23, 42), font=title_font)
    draw.text((70, 580), "- Invokes Llama-3-8B model", fill=(100, 116, 139), font=font)
    draw.text((70, 600), "- Direct stream token callbacks", fill=(100, 116, 139), font=font)
    
    # 4. Sandboxed Uvicorn Runner (Right)
    draw.rounded_rectangle([550, 100, 950, 480], radius=10, fill=(255, 241, 242), outline=(239, 68, 68), width=2)
    draw.text((570, 120), "Sandboxed Subprocesses", fill=(15, 23, 42), font=title_font)
    
    # Inner block inside Sandbox
    draw.rounded_rectangle([580, 160, 920, 300], radius=5, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((600, 180), "Live FastAPI App Subprocess (Port 8080)", fill=(15, 23, 42), font=font)
    draw.text((600, 210), "Runs custom generated main.py logic", fill=(100, 116, 139), font=sub_font)
    draw.text((600, 235), "Mock DB tables auto-configured in SQLite", fill=(100, 116, 139), font=sub_font)
    draw.text((600, 260), "Process ID tracked inside main project map", fill=(100, 116, 139), font=sub_font)
    
    draw.rounded_rectangle([580, 340, 920, 450], radius=5, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((600, 360), "Babel CDN Dynamic compiler iframe", fill=(15, 23, 42), font=font)
    draw.text((600, 390), "Renders Tailwind CSS & React modules", fill=(100, 116, 139), font=sub_font)
    draw.text((600, 415), "Links dynamic clients directly to port 8080", fill=(100, 116, 139), font=sub_font)
    
    # Connecting Arrows
    draw_arrow(draw, (200, 225), (200, 315)) # Client -> API (down)
    draw_arrow(draw, (180, 315), (180, 225)) # API -> Client (up)
    
    draw_arrow(draw, (200, 485), (200, 525)) # API -> Bedrock (down)
    
    draw_arrow(draw, (355, 380), (545, 220)) # Main API -> Sandbox (launch)
    draw_arrow(draw, (550, 400), (355, 200)) # Sandbox -> Client iframe preview
    
    img.save("screenshots/fig2_system_architecture.png")

# ==========================================
# FIGURE 3: Database Schema ER
# ==========================================
def make_fig3():
    w, h = 900, 500
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_card(draw, (w, h), "Figure 3: Database Schema Entity Relationship Diagram")
    
    font, sub_font, title_font = get_fonts(font_path, 13)
    
    # 1. Projects Table Card
    draw.rounded_rectangle([100, 120, 380, 380], radius=10, fill=(248, 250, 252), outline=(100, 116, 139), width=2)
    # Table header
    draw.rounded_rectangle([100, 120, 380, 160], radius=10, fill=(100, 116, 139))
    draw.text((120, 130), "projects (Table)", fill=(255, 255, 255), font=title_font)
    
    # Column details
    cols_1 = [
        "PK | id: INTEGER (Autoincrement)",
        "     | name: VARCHAR(255)",
        "     | idea: TEXT",
        "     | model_id: VARCHAR(100)",
        "     | temperature: FLOAT (0.2)",
        "     | status: VARCHAR(50) (created)",
        "     | created_at: DATETIME (UTC Now)"
    ]
    curr_y = 180
    for c in cols_1:
        draw.text((120, curr_y), c, fill=(15, 23, 42) if "|" in c else (100, 116, 139), font=font)
        curr_y += 28
        
    # 2. Project Steps Table Card
    draw.rounded_rectangle([520, 120, 800, 350], radius=10, fill=(248, 250, 252), outline=(139, 92, 246), width=2)
    # Table header
    draw.rounded_rectangle([520, 120, 800, 160], radius=10, fill=(139, 92, 246))
    draw.text((540, 130), "project_steps (Table)", fill=(255, 255, 255), font=title_font)
    
    # Column details
    cols_2 = [
        "PK | id: INTEGER (Autoincrement)",
        "FK | project_id: INTEGER (projects.id)",
        "     | step_name: VARCHAR(100)",
        "     | content: TEXT",
        "     | updated_at: DATETIME (UTC Now)"
    ]
    curr_y = 180
    for c in cols_2:
        draw.text((540, curr_y), c, fill=(15, 23, 42) if "|" in c else (100, 116, 139), font=font)
        curr_y += 28
        
    # 3. Connection Relational Line (One-To-Many)
    # Draw horizontal connector line
    draw.line([(385, 215), (515, 215)], fill=(139, 92, 246), width=2)
    
    # Crowsfoot one-to-many fork indicator
    draw.line([(385, 205), (385, 225)], fill=(139, 92, 246), width=2) # One mark
    draw.line([(500, 205), (515, 215)], fill=(139, 92, 246), width=2) # Crow fork 1
    draw.line([(500, 225), (515, 215)], fill=(139, 92, 246), width=2) # Crow fork 2
    
    draw.text((410, 185), "1 : N (Cascade)", fill=(139, 92, 246), font=sub_font)
    
    img.save("screenshots/fig3_database_schema.png")

# ==========================================
# FIGURE 4: Double-Layer Code Clean (Two-Layer Stacked Layout)
# ==========================================
def make_fig4():
    w, h = 1100, 500
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_card(draw, (w, h), "Figure 4: Double-Layer Code Cleaning & Deduplication Pipeline")
    
    font, sub_font, title_font = get_fonts(font_path, 13)
    _, _, main_title_font = get_fonts(font_path, 16)
    
    # 1. LAYER 1: Prompt Constraint Panel (Top half)
    draw.rounded_rectangle([40, 50, 1060, 220], radius=10, fill=(239, 246, 255), outline=(59, 130, 246), width=2)
    draw.rounded_rectangle([40, 50, 1060, 90], radius=10, fill=(59, 130, 246))
    draw.text((60, 60), "LAYER 1: BEDROCK SYSTEM PROMPT CONSTRAINT", fill=(255, 255, 255), font=main_title_font)
    
    prompt_lines = [
        "Enforces strict LLM behavior during raw generation phase:",
        "\"CRITICAL OUTPUT RULE: Your response must consist EXCLUSIVELY of the code inside the code block. Do NOT write any",
        "introductory explanations, conversational prefaces, or concluding descriptions before or after the code block.\""
    ]
    curr_y = 110
    for line in prompt_lines:
        draw.text((60, curr_y), line, fill=(15, 23, 42) if line.startswith("\"") else (71, 85, 105), font=font)
        curr_y += 28
        
    # 2. LAYER 2: Orchestrator Clean & Deduplicate Panel (Bottom half)
    draw.rounded_rectangle([40, 260, 1060, 470], radius=10, fill=(240, 253, 250), outline=(16, 185, 129), width=2)
    draw.rounded_rectangle([40, 260, 1060, 300], radius=10, fill=(16, 185, 129))
    draw.text((60, 270), "LAYER 2: ORCHESTRATOR PARSING & DEDUPLICATION PIPELINE", fill=(255, 255, 255), font=main_title_font)
    
    # Inner horizontal process boxes
    box_width = 200
    box_height = 80
    box_y = 350
    
    boxes = [
        {"x": 70, "title": "Stream Tokens", "line": "Reads Bedrock output"},
        {"x": 320, "title": "clean_code_block()", "line": "Strips MD backticks"},
        {"x": 570, "title": "Import Scanner", "line": "Parses package lines"},
        {"x": 820, "title": "O(N) Deduplicator", "line": "Removes repeat imports"}
    ]
    
    for b in boxes:
        draw.rounded_rectangle([b["x"], box_y, b["x"] + box_width, box_y + box_height], radius=8, fill=(255, 255, 255), outline=(16, 185, 129), width=1)
        draw.text((b["x"] + 20, box_y + 15), b["title"], fill=(15, 23, 42), font=title_font)
        draw.text((b["x"] + 20, box_y + 45), b["line"], fill=(100, 116, 139), font=sub_font)
        
    # Connections between boxes
    draw_arrow(draw, (275, box_y + box_height//2), (315, box_y + box_height//2), color=(16, 185, 129))
    draw_arrow(draw, (525, box_y + box_height//2), (565, box_y + box_height//2), color=(16, 185, 129))
    draw_arrow(draw, (775, box_y + box_height//2), (815, box_y + box_height//2), color=(16, 185, 129))
    
    img.save("screenshots/fig4_code_cleaning.png")

# ==========================================
# FIGURE 5: Dynamic Client-Side Iframe Compiler (Clockwise Loop Flowchart)
# ==========================================
def make_fig5():
    w, h = 1100, 500
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_card(draw, (w, h), "Figure 5: Dynamic Client-Side React Iframe Compiler Flowchart")
    
    font, sub_font, title_font = get_fonts(font_path, 13)
    
    # 2 rows, 3 columns loop grid
    # Row 1 (flows left-to-right)
    # Row 2 (flows right-to-left)
    
    box_w = 260
    box_h = 100
    
    nodes = [
        # Row 1
        {"id": 1, "x": 100, "y": 100, "title": "1. Read JSX Code", "lines": ["Retrieves React component", "logic from database"]},
        {"id": 2, "x": 420, "y": 100, "title": "2. Component Match", "lines": ["Extracts name from default", "export statement"]},
        {"id": 3, "x": 740, "y": 100, "title": "3. Strip Imports", "lines": ["Removes ES6 block imports", "and default exports"]},
        
        # Row 2
        {"id": 4, "x": 740, "y": 320, "title": "4. Port Redirect", "lines": ["Rewrites backend API URLs", "from port 8000 to 8080"]},
        {"id": 5, "x": 420, "y": 320, "title": "5. Babel Transpile", "lines": ["Dynamic transpile of JSX", "using browser Babel CDN"]},
        {"id": 6, "x": 100, "y": 320, "title": "6. Mount to Iframe", "lines": ["Injects compiled React UI", "into local sandbox DOM"]}
    ]
    
    # Draw Nodes
    for n in nodes:
        # Node box
        draw.rounded_rectangle([n["x"], n["y"], n["x"] + box_w, n["y"] + box_h], radius=10, fill=(255, 241, 242) if n["id"] > 3 else (240, 253, 250), outline=(239, 68, 68) if n["id"] > 3 else (16, 185, 129), width=2)
        # Title
        draw.text((n["x"] + 20, n["y"] + 15), n["title"], fill=(15, 23, 42), font=title_font)
        # Subtitle details
        curr_y = n["y"] + 45
        for line in n["lines"]:
            draw.text((n["x"] + 20, curr_y), line, fill=(100, 116, 139), font=sub_font)
            curr_y += 20
            
    # Connect loop with curved/step arrows
    draw_arrow(draw, (365, 150), (415, 150)) # 1 -> 2
    draw_arrow(draw, (685, 150), (735, 150)) # 2 -> 3
    
    draw_arrow(draw, (870, 205), (870, 315)) # 3 -> 4 (down)
    
    draw_arrow(draw, (735, 370), (685, 370)) # 4 -> 5 (left)
    draw_arrow(draw, (415, 370), (365, 370)) # 5 -> 6 (left)
    
    img.save("screenshots/fig5_dynamic_compiler.png")

# ==========================================
# FIGURE 10: Dynamic Error Boundary
# ==========================================
def make_fig10():
    w, h = 900, 500
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_card(draw, (w, h), "Figure 10: Dynamic Error Boundary Runtime Exception Overlay")
    
    font, sub_font, title_font = get_fonts(font_path, 13)
    _, _, main_title_font = get_fonts(font_path, 18)
    
    # Clean Error Boundary Panel Mockup
    draw.rounded_rectangle([150, 100, 750, 420], radius=15, fill=(255, 241, 242), outline=(244, 63, 94), width=2)
    
    # Red Warning Icon Circle
    draw.ellipse([410, 130, 490, 210], fill=(244, 63, 94))
    # Draw "!" inside warning circle
    draw.text((444, 142), "!", fill=(255, 255, 255), font=get_fonts(font_path, 42)[2])
    
    draw.text((310, 230), "React Runtime Exception Caught", fill=(225, 29, 72), font=main_title_font)
    
    # Exception Trace box
    draw.rounded_rectangle([180, 275, 720, 335], radius=5, fill=(15, 23, 42))
    draw.text((200, 292), "ReferenceError: Container is not defined in App.jsx (line 124)", fill=(248, 250, 252), font=font)
    
    # Debugging Tips
    draw.text((200, 355), "💡 Debugging Tip: Click on Monaco Workspace Editor and resolve the variable in line 124.", fill=(71, 85, 105), font=sub_font)
    draw.text((230, 378), "Make sure to declare your container state or component wrapper before using it.", fill=(100, 116, 139), font=sub_font)
    
    img.save("screenshots/fig10_error_boundary.png")

if __name__ == "__main__":
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    make_fig5()
    make_fig10()
    print("Successfully generated all 6 clean vector diagrams with zero AI slop!")
