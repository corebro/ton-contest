from __future__ import annotations

import logging

import httpx
from aiogram import F, Router
from aiogram.types import Message

from services.ai.analyzer import AnalyzerService
from services.formatting.formatter import build_analysis_response
from services.parsing.metrics import build_stats
from services.parsing.parser import build_flow_result
from services.ton.ton_api import TonApiClient
from utils.validators import (
    detect_input_type,
    is_evm_address,
    is_supported_input,
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text)
async def analyze_input(message: Message) -> None:
    if not message.text:
        return

    user_input = message.text.strip()
    if user_input.startswith("/"):
        return

    if is_evm_address(user_input):
        await message.answer(
            "This looks like an EVM address (0x...40 hex), not a TON wallet address.\n\n"
            "Please send:\n"
            "• a TON wallet address like EQ... or UQ...\n"
            "• a raw TON address like 0:abcd...\n"
            "• or a TON transaction hash (64 hex chars)"
        )
        return

    if not is_supported_input(user_input):
        await message.answer(
            "Please send a valid TON wallet address or transaction hash.\n\n"
            "Supported formats:\n"
            "• TON wallet: EQ... / UQ...\n"
            "• RAW TON address: 0:abcd...\n"
            "• TON tx hash: 64 hex chars or 0x + 64 hex chars"
        )
        return

    wait_msg = await message.answer("🔍 Analyzing TON activity...")
    input_type = detect_input_type(user_input)

    if input_type == "unknown":
        await wait_msg.edit_text(
            "Unsupported input format.\n\n"
            "Please send a TON wallet address or TON transaction hash."
        )
        return

    try:
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

    except httpx.HTTPStatusError as exc:
        logger.exception("TON API request failed: %s", exc)

        status = exc.response.status_code if exc.response is not None else None

        if input_type == "address":
            if status == 400:
                await wait_msg.edit_text(
                    "This TON address is invalid or malformed.\n\n"
                    "Check the address and try again."
                )
                return

            if status == 404:
                await wait_msg.edit_text(
                    "This TON address was not found."
                )
                return

        if input_type == "tx_hash":
            if status == 400:
                await wait_msg.edit_text(
                    "This transaction hash is invalid or not in TON format.\n\n"
                    "A TON tx hash should be 64 hexadecimal characters."
                )
                return

            if status == 404:
                await wait_msg.edit_text(
                    "This transaction hash was not found in TON."
                )
                return

        await wait_msg.edit_text(
            "TON API returned an error while analyzing this activity. Please try again."
        )

    except Exception as exc:  # noqa: BLE001
        logger.exception("Analysis failed: %s", exc)
        await wait_msg.edit_text(
            "Something went wrong while analyzing this TON activity. Please try again."
        )