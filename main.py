import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher

from handlers import router


BOT_TOKEN = os.environ["BOT_TOKEN"]

PORT = int(os.environ.get("PORT", 10000))


async def health_check(request):
    return web.Response(text="Bot is running!")


async def start_web_server():
    app = web.Application()

    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        PORT
    )

    await site.start()

    print(f"Web server running on port {PORT}")


async def main():

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()
    dp.include_router(router)

    await start_web_server()

    print("================================")
    print("       TELEGRAM BOT")
    print("================================")
    print("Bot started...")
    print("Polling started...")
    print("================================")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
