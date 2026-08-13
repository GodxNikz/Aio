import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.client.default import DefaultBotProperties


# ============================================================
# CONFIG
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing."
    )


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# BOT
# ============================================================

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


# ============================================================
# CUSTOM EMOJIS
# ============================================================

EMOJI_WELCOME = (
    '<tg-emoji emoji-id="5190926525104432174">👋</tg-emoji>'
)

EMOJI_FIRE = (
    '<tg-emoji emoji-id="5190869694097166564">🔥</tg-emoji>'
)

EMOJI_WARNING = (
    '<tg-emoji emoji-id="5188634283878686284">❗️</tg-emoji>'
)

EMOJI_PREMIUM = (
    '<tg-emoji emoji-id="5190694304812671934">💎</tg-emoji>'
)


# ============================================================
# MAIN KEYBOARD
# ============================================================

def main_keyboard() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 My Info",
                    callback_data="my_info"
                ),
                InlineKeyboardButton(
                    text="🆔 My ID",
                    callback_data="my_id"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📖 Help",
                    callback_data="help"
                ),
            ],
        ]
    )


# ============================================================
# BACK KEYBOARD
# ============================================================

def back_keyboard() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{EMOJI_PREMIUM} Back",
                    callback_data="back"
                )
            ]
        ]
    )


# ============================================================
# START TEXT
# ============================================================

def start_text(name: str) -> str:

    return (
        f"{EMOJI_WELCOME} "
        f"<b>Welcome, {name}!</b>\n\n"

        f"{EMOJI_FIRE} "
        f"This is an Aiogram Telegram bot.\n\n"

        f"{EMOJI_WARNING} "
        f"Use the buttons below to explore the bot."
    )


# ============================================================
# /START
# ============================================================

@dp.message(CommandStart())
async def start_handler(message: Message):

    user = message.from_user

    if not user:
        return

    name = user.first_name or "User"

    await message.answer(
        start_text(name),
        reply_markup=main_keyboard()
    )


# ============================================================
# /HELP
# ============================================================

@dp.message(Command("help"))
async def help_handler(message: Message):

    text = (
        f"{EMOJI_WARNING} "
        "<b>Bot Help</b>\n\n"

        f"{EMOJI_WELCOME} "
        "/start - Start the bot\n\n"

        "📖 /help - Show help\n"
        "🆔 /id - Show your Telegram ID\n"
        "🏓 /ping - Check bot status\n"
        "📢 /broadcast - Admin command"
    )

    await message.answer(text)


# ============================================================
# /ID
# ============================================================

@dp.message(Command("id"))
async def id_handler(message: Message):

    user = message.from_user

    if not user:
        return

    await message.answer(
        f"{EMOJI_FIRE} "
        "<b>Your Telegram ID</b>\n\n"
        f"<code>{user.id}</code>"
    )


# ============================================================
# /PING
# ============================================================

@dp.message(Command("ping"))
async def ping_handler(message: Message):

    await message.answer(
        "🏓 <b>Pong!</b>\n\n"
        "✅ Bot is online."
    )


# ============================================================
# MY INFO BUTTON
# ============================================================

@dp.callback_query(F.data == "my_info")
async def my_info_callback(
    callback: CallbackQuery
):

    user = callback.from_user

    username = (
        f"@{user.username}"
        if user.username
        else "No username"
    )

    name = user.first_name or "Unknown"

    text = (
        "👤 <b>Your Information</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Name: {name}\n"
        f"🔗 Username: {username}\n"
        f"🌐 Language: "
        f"{user.language_code or 'Unknown'}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=back_keyboard()
    )

    await callback.answer()


# ============================================================
# MY ID BUTTON
# ============================================================

@dp.callback_query(F.data == "my_id")
async def my_id_callback(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "🆔 <b>Your Telegram ID</b>\n\n"
        f"<code>{callback.from_user.id}</code>",
        reply_markup=back_keyboard()
    )

    await callback.answer()


# ============================================================
# HELP BUTTON
# ============================================================

@dp.callback_query(F.data == "help")
async def help_callback(
    callback: CallbackQuery
):

    text = (
        "📖 <b>Help</b>\n\n"

        "Available commands:\n\n"

        "▶️ /start\n"
        "▶️ /help\n"
        "▶️ /id\n"
        "▶️ /ping\n\n"

        "🤖 Built with <b>Aiogram 3.x</b>."
    )

    await callback.message.edit_text(
        text,
        reply_markup=back_keyboard()
    )

    await callback.answer()


# ============================================================
# BACK BUTTON
# ============================================================

@dp.callback_query(F.data == "back")
async def back_callback(
    callback: CallbackQuery
):

    user = callback.from_user

    name = user.first_name or "User"

    await callback.message.edit_text(
        start_text(name),
        reply_markup=main_keyboard()
    )

    await callback.answer()


# ============================================================
# PREMIUM BUTTON
# ============================================================

@dp.callback_query(F.data == "premium")
async def premium_callback(
    callback: CallbackQuery
):

    text = (
        f"{EMOJI_PREMIUM} "
        "<b>Premium</b>\n\n"
        "Premium features are coming soon."
    )

    await callback.message.edit_text(
        text,
        reply_markup=back_keyboard()
    )

    await callback.answer()


# ============================================================
# ADMIN BROADCAST
# ============================================================

@dp.message(Command("broadcast"))
async def broadcast_handler(
    message: Message
):

    if message.from_user.id != ADMIN_ID:

        await message.answer(
            "❌ <b>Access Denied</b>\n\n"
            "You are not authorized to use this command."
        )

        return

    if not message.reply_to_message:

        await message.answer(
            "📢 <b>Broadcast</b>\n\n"
            "Reply to a message and send "
            "<code>/broadcast</code>."
        )

        return

    await message.answer(
        "✅ <b>Broadcast message received.</b>\n\n"
        "A user database is required to send "
        "the message to all registered users."
    )


# ============================================================
# UNKNOWN MESSAGE
# ============================================================

@dp.message()
async def unknown_handler(
    message: Message
):

    await message.answer(
        f"{EMOJI_WARNING} "
        "<b>Unknown command</b>\n\n"
        "Use /help to see available commands."
    )


# ============================================================
# MAIN
# ============================================================

async def main():

    logger.info("Starting Telegram bot...")

    # Remove webhook before starting polling.
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    me = await bot.get_me()

    logger.info(
        "Bot started successfully: @%s",
        me.username
    )

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        logger.info("Bot stopped.")

    except Exception as error:

        logger.exception(
            "Bot crashed: %s",
            error
)
