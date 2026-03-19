from __future__ import annotations

from typing import Any

from services.ton.ton_models import NormalizedTransaction


NANO = 1_000_000_000


def _extract_address(value: Any) -> str:
    if isinstance(value, dict):
        return (
            value.get("address")
            or value.get("account")
            or value.get("wallet")
            or value.get("owner")
            or "unknown"
        )
    if isinstance(value, str):
        return value
    return "unknown"


def normalize_transaction(item: dict[str, Any]) -> NormalizedTransaction:
    in_msg = item.get("in_msg") or {}

    tx_hash = item.get("hash") or item.get("tx_hash") or item.get("transaction_id") or "unknown"
    from_address = _extract_address(in_msg.get("source") or item.get("from") or item.get("sender"))
    to_address = _extract_address(in_msg.get("destination") or item.get("to") or item.get("recipient") or item.get("account"))

    raw_value = (
        in_msg.get("value")
        or item.get("value")
        or item.get("amount")
        or 0
    )
    try:
        amount = int(raw_value) / NANO
    except (TypeError, ValueError):
        amount = 0.0

    description = item.get("description") or {}
    tx_type = (
        description.get("type")
        or item.get("type")
        or item.get("action")
        or "transfer"
    )

    contract_label = None
    destination = in_msg.get("destination")
    if isinstance(destination, dict):
        contract_label = destination.get("name") or destination.get("icon")

    if item.get("nft") or "nft" in str(tx_type).lower():
        asset_type = "NFT"
    elif item.get("jetton") or "jetton" in str(tx_type).lower() or "token" in str(tx_type).lower():
        asset_type = "Jetton"
    else:
        asset_type = "TON"

    return NormalizedTransaction(
        tx_hash=tx_hash,
        from_address=from_address,
        to_address=to_address,
        amount=amount,
        asset_type=asset_type,
        tx_type=str(tx_type),
        timestamp=int(item.get("utime") or item.get("timestamp") or 0),
        success=not bool(item.get("aborted", False)),
        contract_label=contract_label,
        comment=in_msg.get("message"),
    )
