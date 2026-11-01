from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_db, init_db
from telegram_auth import verify_telegram_init_data

app = FastAPI(title="RGX ESPORTS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://thergeditz09-png.github.io",
        "http://127.0.0.1:8080",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Telegram-Init-Data"],
)

ADMIN_IDS = [7811880836]


class TournamentCreate(BaseModel):
    title: str
    game: str
    mode: str
    max_players: int


def get_current_user(
    init_data: str = Header(default="", alias="X-Telegram-Init-Data")
):
    user = verify_telegram_init_data(init_data)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Telegram session")

    return user


def require_admin(user=Depends(get_current_user)):
    if user["id"] not in ADMIN_IDS:
        raise HTTPException(status_code=403, detail="Admin access denied")
    return user


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {"name": "RGX ESPORTS", "status": "online"}


@app.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "user_id": user["id"],
        "is_admin": user["id"] in ADMIN_IDS
    }


@app.get("/tournaments")
def get_tournaments():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM tournaments ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.post("/admin/tournaments")
def create_tournament(
    data: TournamentCreate,
    user=Depends(require_admin)
):
    if not data.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    if data.game not in ["CPM 1", "CPM 2"]:
        raise HTTPException(status_code=400, detail="Invalid game")

    if data.mode not in ["Solo", "Team"]:
        raise HTTPException(status_code=400, detail="Invalid mode")

    if data.max_players < 2 or data.max_players > 500:
        raise HTTPException(status_code=400, detail="Slots must be 2-500")

    conn = get_db()
    cur = conn.execute(
        """INSERT INTO tournaments
        (title, game, mode, max_players, status)
        VALUES (?, ?, ?, ?, 'OPEN')""",
        (data.title.strip(), data.game, data.mode, data.max_players)
    )
    conn.commit()
    tournament_id = cur.lastrowid
    conn.close()

    return {"success": True, "tournament_id": tournament_id}
