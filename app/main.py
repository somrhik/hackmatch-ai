from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Lightweight model (VERY IMPORTANT for Vercel memory)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Store participants temporarily (in-memory)
participants = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "teams": None
    })


@app.post("/add")
async def add_participant(
    request: Request,
    name: str = Form(...),
    skills: str = Form(...)
):
    participants.append({
        "name": name,
        "skills": skills
    })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "teams": None,
        "message": "User added successfully"
    })


@app.post("/generate", response_class=HTMLResponse)
async def generate_teams(request: Request):
    if len(participants) < 2:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "teams": None,
            "error": "Not enough participants"
        })

    skill_texts = [p["skills"] for p in participants]

    embeddings = model.encode(skill_texts)

    similarity_matrix = cosine_similarity(embeddings)

    team1 = []
    team2 = []

    for i, p in enumerate(participants):
        if i % 2 == 0:
            team1.append(p["name"])
        else:
            team2.append(p["name"])

    teams = {
        "Team 1": team1,
        "Team 2": team2
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "teams": teams
    })