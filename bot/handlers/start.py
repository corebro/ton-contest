from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "<b>TON X-Ray</b>\n\n"
        "Send a TON wallet address or transaction hash to analyze its flow and behavior.\n\n"
        "Examples:\n"
        "• <code>EQC123...</code>\n"
        "• <code>b7d1b2b9...</code>"
    )
    await message.answer(text)
