from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import Message

from services.ai.analyzer import AnalyzerService
from services.formatting.formatter import build_analysis_response
from services.parsing.metrics import build_stats
from services.parsing.parser import build_flow_result
from services.ton.ton_api import TonApiClient
from utils.validators import detect_input_type, is_supported_input

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text)
async def analyze_input(message: Message) -> None:
    if not message.text:
        return

    user_input = message.text.strip()
    if user_input.startswith("/"):
        return

    if not is_supported_input(user_input):
        await message.answer(
            "Please send a valid TON wallet address or transaction hash."
        )
        return

    wait_msg = await message.answer("🔍 Analyzing TON activity...")

    try:
        input_type = detect_input_type(user_input)
        async with TonApiClient() as ton_client:
            if input_type == "address":
                transactions = await ton_client.get_wallet_transactions(user_input)
                target_label = user_input
            else:
                transactions = await ton_client.get_transaction(user_input)
                target_label = user_input

        if not transactions:
            await wait_msg.edit_text("No transactions were found for this input.")
            return

        parsed = build_flow_result(transactions)
        stats = build_stats(transactions, parsed.flow)

        analyzer = AnalyzerService()
        insight = await analyzer.explain_flow(parsed.flow, stats, parsed.patterns)

        response = build_analysis_response(
            target=target_label,
            flow=parsed.flow,
            stats=stats,
            patterns=parsed.patterns,
            insight=insight,
        )
        await wait_msg.edit_text(response)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Analysis failed: %s", exc)
        await wait_msg.edit_text(
            "Something went wrong while analyzing this TON activity. Please try again."
        )
