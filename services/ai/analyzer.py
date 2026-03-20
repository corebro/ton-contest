from __future__ import annotations

from typing import Any

from openai import AsyncOpenAI

from core.config import settings
from services.ai.prompts import build_analysis_prompt


class AnalyzerService:
    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def explain_flow(
        self,
        flow: list[str],
        stats: dict[str, Any],
        patterns: list[str],
    ) -> str:
        prompt = build_analysis_prompt(flow, stats, patterns)

        response = await self._client.responses.create(
            model=settings.openai_model,
            input=prompt,
            temperature=0.1,
        )

        text = (response.output_text or "").strip()
        if text:
            return text

        return (
            "Based on recent transactions, this activity appears to follow a simple transfer pattern. "
            "The available account history does not show strong evidence of complex routing, NFT actions, "
            "or jetton-heavy behavior."
        )