from __future__ import annotations

from typing import Any

import httpx

from core.config import settings
from services.ton.ton_models import NormalizedTransaction
from services.ton.ton_normalizer import normalize_transaction


class TonApiClient:
    def __init__(self) -> None:
        headers = {"Accept": "application/json"}
        if settings.tonapi_api_key:
            headers["Authorization"] = f"Bearer {settings.tonapi_api_key}"

        self._client = httpx.AsyncClient(
            base_url=settings.tonapi_base_url,
            headers=headers,
            timeout=settings.request_timeout,
        )

    async def __aenter__(self) -> "TonApiClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get_wallet_transactions(self, address: str) -> list[NormalizedTransaction]:
        response = await self._client.get(
            f"/blockchain/accounts/{address}/transactions",
            params={"limit": settings.transactions_limit},
        )
        response.raise_for_status()
        data = response.json()
        txs = data.get("transactions", [])
        return [normalize_transaction(tx, address) for tx in txs]

    async def get_transaction(self, tx_hash: str) -> list[NormalizedTransaction]:
        response = await self._client.get(f"/blockchain/transactions/{tx_hash}")
        response.raise_for_status()
        tx = response.json()

        account = self._extract_account_from_tx(tx)
        if not account:
            return [normalize_transaction(tx, "unknown")]

        account_response = await self._client.get(
            f"/blockchain/accounts/{account}/transactions",
            params={"limit": min(settings.transactions_limit, 10)},
        )
        account_response.raise_for_status()
        account_data = account_response.json()
        related = account_data.get("transactions", [])

        normalized = [normalize_transaction(tx, account)]
        normalized.extend(normalize_transaction(item, account) for item in related[:5])
        return normalized

    @staticmethod
    def _extract_account_from_tx(tx: dict[str, Any]) -> str | None:
        account = tx.get("account")
        if isinstance(account, dict):
            return account.get("address")
        if isinstance(account, str):
            return account

        in_msg = tx.get("in_msg") or {}
        dest = in_msg.get("destination")
        if isinstance(dest, dict):
            return dest.get("address")
        return None