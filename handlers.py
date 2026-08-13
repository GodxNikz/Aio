from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import keyboards as kb


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):

    await message.answer(
        '<tg-emoji emoji-id="5190694304812671934">⚙️</tg-emoji> '
        'Добро пожаловать в наш красивый бот!',
        parse_mode="HTML",
        reply_markup=kb.welcome
    )


@router.message(F.text == "PRIMARY")
async def response_primary(message: Message):

    await message.answer(
        '<tg-emoji emoji-id="5190694304812671934">⚙️</tg-emoji> '
        'You selected PRIMARY.',
        parse_mode="HTML",
        reply_markup=kb.inline_emoji
    )


@router.message(F.text == "SUCCESS")
async def response_success(message: Message):

    await message.answer("✅ Success!")


@router.message(F.text == "DANGER")
async def response_danger(message: Message):

    await message.answer("⚠️ Danger!")
