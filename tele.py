from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

import json
import os

TOKEN = "8816208869:AAF5iS6IdqiFtYScXRIy-ZQPnoWXbPsme9M"

ADMIN_ID = 8354329880  # bu yerga /id dan chiqqan ID ni yozing

VIDEOS = {
    "1": "BAACAgIAAyEFAAMBBhVlXQADCmo2_Hf9CdSOuuSiIh6hjnHrJMdgAAJ6sAAC69y4STp2boe_0CvtPAQ",
    "2": "BAACAgIAAyEFAAMBBhVlXQADCWo2_HdnbPSLRKTJWQ3shj93wC3FAALoowACSaK5SWBn1kxM4V37PAQ",
    "3": "BAACAgIAAyEFAAMBBhVlXQADCGo2_HbCXX8xHqTe0ImQ_m1xI6KpAALnowACSaK5SfAQLwejizxmPAQ",
    "4": "BAACAgIAAxkBAAMUajcAAVjbalYa8umI4j9AEOgpL8_bAALEnAACyPa4Scft4V7hG3OWPAQ",
    "5": "BAACAgQAAxkBAANkajcfBmbbugIbVQJD5WAoCYmjVIcAAlAJAALF06hR15gpv5HeCnQ8BA",
    "6": "BAACAgIAAxkBAANqajcgeg9pUomR7uMckCokF7CtmBcAAoy3AALU9RFJMfXY-Rejg6U8BA"
}

USERS_FILE = "users.json"

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = set(json.load(f))
else:
    users = set()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in users:
        users.add(user_id)

        with open(USERS_FILE, "w") as f:
            json.dump(list(users), f)

    text = update.message.text

    if text in VIDEOS:
        await update.message.reply_video(VIDEOS[text])
    else:
        await update.message.reply_text("❌ Bunday video topilmadi.")


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        await update.message.reply_text(
            f"FILE ID:\n\n{update.message.video.file_id}"
        )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"📊 Foydalanuvchilar soni: {len(users)}"
        )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Sizning ID: {update.effective_user.id}"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("id", myid))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
)

app.add_handler(
    MessageHandler(filters.VIDEO, get_file_id)
)

print("Bot ishga tushdi...")

app.run_polling()
