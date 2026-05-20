Project Title
AI Software Development Team
________________________________________
Description

This project simulates a complete software development team using AI agents. Given a project idea, the system generates requirements, architecture, backend code, frontend code, tests, and deployment strategy using multiple specialized agents coordinated by an orchestrator.
________________________________________
Features

•	Multi-agent architecture

•	Automated software development pipeline

•	Role-based AI agents

•	Iterative code improvement

•	Memory integration using FAISS

•	API-based backend and Streamlit UI
________________________________________
Tech Stack

•	Python

•	FastAPI

•	Streamlit

•	AWS Bedrock

•	FAISS
________________________________________
Project Structure

AI-SOFTWARE-TEAM/

│── agents/

│   ├── base_agent.py

│   ├── product_manager.py

│   ├── architect.py

│   ├── backend_dev.py

│   ├── frontend_dev.py

│   ├── code_reviewer.py

│   ├── qa_agent.py

│   ├── devops_agent.py

│

│── app/

│   ├── main.py

│   ├── orchestrator.py

│   ├── config.py

│

│── tools/

│   ├── vector_store.py

│

│── ui/

│   ├── streamlit_app.py

│

│── requirements.txt

│── .env

________________________________________
Prerequisites

•	Python 3.8 or above

•	AWS Bedrock access

•	AWS credentials configured
________________________________________
Installation

pip install -r requirements.txt
________________________________________
Configuration

Create a .env file:

AWS_REGION=your_region

MODEL_ID=your_bedrock_model
________________________________________
Running the Application

Simply execute the main starter script to spin up both the FastAPI backend and React + Tailwind CSS v4 frontend parallelly:

./start.sh
________________________________________
Usage

1.	Enter a project idea

2.	Click “Build Project”

3.	View outputs from each agent

4.	Analyze generated software components
________________________________________
How It Works

•	Input idea is passed to orchestrator

•	Agents process input sequentially

•	Outputs are stored and reused via memory

•	Final result includes all development stages
•	Or generate a complete IEEE paper combining your best project




Start both backend & React frontend services: ./start.sh