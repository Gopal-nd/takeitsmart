from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define the BMI calculation formula
def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)

# Define the BMI categories
bmi_categories = {
    "underweight": (0, 18.5),
    "normal": (18.5, 24.9),
    "overweight": (25, 29.9),
    "obese": (30, float("inf"))
}

# Define the user model
class User(BaseModel):
    id: int
    height: float
    weight: float
    bmi: float
    goal: str

# Define the progress model
class Progress(BaseModel):
    id: int
    user_id: int
    bmi: float
    weight: float
    height: float
    timestamp: str

# Define the API routes
@app.get("/calculateBMI")
async def calculate_bmi_route(height: float, weight: float):
    bmi = calculate_bmi(weight, height)
    category = next((category for category, (min, max) in bmi_categories.items() if min <= bmi <= max), "unknown")
    return {"bmi": bmi, "category": category}

@app.post("/setGoal")
async def set_goal_route(user: User):
    # Store the user's goal in the database
    # ...
    return {"message": "Goal set successfully"}

@app.get("/trackProgress")
async def track_progress_route(user_id: int):
    # Retrieve the user's progress data from the database
    # ...
    return {"progress": progress_data}

@app.get("/getProgressHistory")
async def get_progress_history_route(user_id: int):
    # Retrieve the user's progress history from the database
    # ...
    return {"progress_history": progress_history}

@app.post("/reminders")
async def send_reminders_route(user_id: int):
    # Send reminders to the user
    # ...
    return {"message": "Reminders sent successfully"}


class User(BaseModel):
    id: int
    height: float
    weight: float
    bmi: float
    goal: str

class Progress(BaseModel):
    id: int
    user_id: int
    bmi: float
    weight: float
    height: float
    timestamp: str

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["bmi_calculator"]
users_collection = db["users"]
progress_collection = db["progress"]

# Define the database connection

# Define the API routes
@app.get("/calculateBMI")
async def calculate_bmi_route(height: float, weight: float):
    # Calculate the BMI
    bmi = calculate_bmi(weight, height)
    category = next((category for category, (min, max) in bmi_categories.items() if min <= bmi <= max), "unknown")
    return {"bmi": bmi, "category": category}

@app.post("/setGoal")
async def set_goal_route(user: User):
    # Store the user's goal in the database
    users_collection.insert_one(user.dict())
    return {"message": "Goal set successfully"}

@app.get("/trackProgress")
async def track_progress_route(user_id: int):
    # Retrieve the user's progress data from the database
    user_data = users_collection.find_one({"_id": user_id})
    progress_data = progress_collection.find({"user_id": user_id})
    return {"progress": progress_data}

@app.get("/getProgressHistory")
async def get_progress_history_route(user_id: int):
    # Retrieve the user's progress history from the database
    progress_history = progress_collection.find({"user_id": user_id})
    return {"progress_history": progress_history}

@app.post("/reminders")
async def send_reminders_route(user_id: int):
    # Send reminders to the user
    # ...
    return {"message": "Reminders sent successfully"}