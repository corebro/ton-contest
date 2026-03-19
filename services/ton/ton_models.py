from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class NormalizedTransaction:
    tx_hash: str
    from_address: str
    to_address: str
    amount: float
    asset_type: str
    tx_type: str
    timestamp: int
    success: bool
    contract_label: str | None = None
    comment: str | None = None
