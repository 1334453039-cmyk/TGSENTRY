import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", "10000"))
RENDER_URL = os.environ["RENDER_EXTERNAL_URL"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 查询用户", callback_data="check")],
        [InlineKeyboardButton("🚨 提交举报", callback_data="report")],
        [InlineKeyboardButton("ℹ️ 使用说明", callback_data="help")],
    ]

    text = """🛡️ TGSENTRY

Telegram 风险查询与举报平台

请选择你需要的功能："""

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check":
        await query.message.reply_text(
            "🔍 用户查询\n\n"
            "请输入 Telegram 用户名或 ID，例如：\n"
            "@username"
        )

    elif query.data == "report":
        await query.message.reply_text(
            "🚨 提交举报\n\n"
            "请先输入被举报人的 Telegram 用户名或 ID。"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ 使用说明\n\n"
            "TGSENTRY 用于查询和管理风险举报记录。\n\n"
            "⚠️ 查询结果仅供风险参考，不代表对任何个人作出最终认定。"
        )


async def post_init(application: Application):
    webhook_url = f"{RENDER_URL}/telegram"
    await application.bot.set_webhook(
        url=webhook_url,
        allowed_updates=Update.ALL_TYPES,
    )
    print(f"Webhook set: {webhook_url}")


def main():
    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("TGSENTRY is starting...")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=f"{RENDER_URL}/telegram",
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()
