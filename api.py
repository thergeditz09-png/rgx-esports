from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_db, init_db

app = FastAPI(title="RGX ESPORTS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_IDS = [7811880836]

class TournamentCreate(BaseModel):
    admin_id: int
    title: str
    game: str
    mode: str
    max_players: int

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def home():
    return {"name": "RGX ESPORTS", "status": "online"}

@app.get("/tournaments")
def get_tournaments():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM tournaments ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/admin/tournaments")
def create_tournament(data: TournamentCreate):
    if data.admin_id not in ADMIN_IDS:
        raise HTTPException(status_code=403, detail="Admin access denied")

    if data.mode not in ["Solo", "Team"]:
        raise HTTPException(status_code=400, detail="Invalid mode")

    if data.max_players < 2:
        raise HTTPException(status_code=400, detail="Minimum 2 slots required")

    conn = get_db()
    cur = conn.execute(
        """INSERT INTO tournaments
        (title, game, mode, max_players, status)
        VALUES (?, ?, ?, ?, 'OPEN')""",
        (data.title, data.game, data.mode, data.max_players)
    )
    conn.commit()
    tournament_id = cur.lastrowid
    conn.close()

    return {"success": True, "tournament_id": tournament_id}
