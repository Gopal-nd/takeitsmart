import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    idea = Column(Text, nullable=False)
    model_id = Column(String, nullable=True)
    temperature = Column(Float, default=0.2)
    status = Column(String, default="created")  # created, requirements, architecture, code, qa, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    steps = relationship("ProjectStep", back_populates="project", cascade="all, delete-orphan")

class ProjectStep(Base):
    __tablename__ = 'project_steps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    step_name = Column(String, nullable=False)  # requirements, architecture, backend_code, frontend_code, review, tests, deployment
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="steps")

# Database setup
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ai_software_team.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
