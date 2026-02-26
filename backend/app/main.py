from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

app = FastAPI()

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
users = []

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class UserProfile(BaseModel):
    name: str
    skills: List[str]
    experience_level: str
    preferred_role: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add-user")
def add_user(profile: UserProfile):
    users.append(profile)
    return {"message": "User added successfully"}

@app.get("/form-teams")
def form_teams():
    if len(users) < 2:
        return {"message": "Not enough users"}

    texts = [" ".join(user.skills) for user in users]
    embeddings = model.encode(texts)

    kmeans = KMeans(n_clusters=2, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    teams = {}
    for idx, label in enumerate(labels):
        teams.setdefault(f"Team {label+1}", []).append(users[idx].name)

    return teams