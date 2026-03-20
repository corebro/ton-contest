from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class NormalizedTransaction:
    tx_hash: str
    account_address: str
    from_address: str
    to_address: str
    counterparty_address: str
    direction: str  # incoming | outgoing | unknown
    amount: float
    asset_type: str
    tx_type: str
    timestamp: int
    success: bool
    contract_label: str | None = None
    comment: str | None = None
    source_label: str | None = None
    destination_label: str | None = None