from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


welcome = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="PRIMARY"),
        ],
        [
            KeyboardButton(text="SUCCESS"),
        ],
        [
            KeyboardButton(text="DANGER"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню..."
)


inline_emoji = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="YouTube",
                url="https://youtube.com/",
                icon_custom_emoji_id="5359523901200651432",
                style="danger",
            )
        ],
        [
            InlineKeyboardButton(
                text="Telegram",
                url="https://t.me/",
                icon_custom_emoji_id="5436302963117137450",
                style="primary",
            )
        ],
    ]
)
