from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

WEB_APP_URL = "https://thergeditz09-png.github.io/rgx-esports/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    from database import get_db
    conn = get_db()
    conn.execute(
        """INSERT OR REPLACE INTO players
        (user_id, username, full_name)
        VALUES (?, ?, ?)""",
        (user.id, user.username, user.full_name)
    )
    conn.commit()
    conn.close()

    keyboard = [[
        InlineKeyboardButton(
            "🚀 OPEN RGX ESPORTS",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    ]]

    await update.message.reply_text(
        "⚡ RGX ESPORTS ⚡\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🏆 WELCOME TO THE BATTLEGROUND!\n\n"
        "🎮 Games: CPM 1 | CPM 2\n"
        "⚔️ Modes: SOLO | TEAM\n"
        "🏅 Compete with players and climb the leaderboard.\n\n"
        "📱 Tournaments, matches, rankings and your profile "
        "are waiting inside our Mini App.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🔥 ENTER THE ARENA. MAKE YOUR MARK.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
