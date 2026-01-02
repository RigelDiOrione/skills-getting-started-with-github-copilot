"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Tennis Club": {
        "description": "Learn tennis techniques and participate in matches",
        "schedule": "Wednesdays and Saturdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu"]
        },
        "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
        "description": "Theater performances and acting workshops",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["grace@mergington.edu", "noah@mergington.edu"]
        },
        "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["ryan@mergington.edu"]
        },
        "Math Olympiad": {
        "description": "Advanced mathematics and problem-solving competitions",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["zoe@mergington.edu", "ethan@mergington.edu"]
        },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email
    normalized_email: str = email.strip().lower()

    # Prevent duplicate signups
    if normalized_email in (p.strip().lower() for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Email already signed up for this activity")

    # Prevent exceeding capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.post("/activities/{activity_name}/unsubscribe")
def unsubscribe_from_activity(activity_name: str, email: str):
    """Unsubscribe a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    normalized_email: str = email.strip().lower()

    # Check if the email is actually signed up
    if normalized_email not in (p.strip().lower() for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Email not signed up for this activity")

    # Remove the student
    activity["participants"] = [p for p in activity["participants"] if p.strip().lower() != normalized_email]
    return {"message": f"Unsubscribed {normalized_email} from {activity_name}"}
