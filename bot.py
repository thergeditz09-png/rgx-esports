import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from database import init_db
from handlers.start import start

logging.basicConfig(level=logging.INFO)

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()

    messages = {
        "home": "⚡ RGX ESPORTS HOME",
        "tournaments": "🏆 Available tournaments will appear here.",
        "profile": "👤 Your player profile.",
        "leaderboard": "📊 Player leaderboard."
    }

    await query.edit_message_text(messages.get(query.data, "Unknown option."))

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing in .env")

    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("RGX ESPORTS BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
