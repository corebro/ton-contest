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


def _extract_name(value: Any) -> str | None:
    if isinstance(value, dict):
        return (
            value.get("name")
            or value.get("label")
            or value.get("title")
            or value.get("icon")
        )
    return None


def normalize_transaction(item: dict[str, Any]) -> NormalizedTransaction:
    in_msg = item.get("in_msg") or {}
    out_msgs = item.get("out_msgs") or []

    tx_hash = item.get("hash") or item.get("tx_hash") or item.get("transaction_id") or "unknown"

    account_obj = item.get("account")
    account_address = _extract_address(account_obj)

    source_obj = in_msg.get("source") or item.get("from") or item.get("sender")
    destination_obj = in_msg.get("destination") or item.get("to") or item.get("recipient") or account_obj

    from_address = _extract_address(source_obj)
    to_address = _extract_address(destination_obj)

    raw_value = in_msg.get("value") or item.get("value") or item.get("amount") or 0
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

    source_label = _extract_name(source_obj)
    destination_label = _extract_name(destination_obj)

    contract_label = (
        destination_label
        or description.get("action")
        or description.get("type")
    )

    comment = in_msg.get("message")
    if not comment and out_msgs:
        first_out = out_msgs[0] if isinstance(out_msgs[0], dict) else {}
        comment = first_out.get("message")

    asset_type = "TON"
    text_blob = " ".join(
        str(x) for x in [
            tx_type,
            contract_label,
            source_label,
            destination_label,
            comment,
            item.get("type"),
            item.get("action"),
        ] if x
    ).lower()

    if item.get("nft") or "nft" in text_blob or "getgems" in text_blob:
        asset_type = "NFT"
    elif (
        item.get("jetton")
        or "jetton" in text_blob
        or "token" in text_blob
        or "swap" in text_blob
        or "ston" in text_blob
        or "dedust" in text_blob
    ):
        asset_type = "Jetton"

    return NormalizedTransaction(
        tx_hash=tx_hash,
        account_address=account_address,
        from_address=from_address,
        to_address=to_address,
        amount=amount,
        asset_type=asset_type,
        tx_type=str(tx_type),
        timestamp=int(item.get("utime") or item.get("timestamp") or 0),
        success=not bool(item.get("aborted", False)),
        contract_label=contract_label,
        comment=comment,
        source_label=source_label,
        destination_label=destination_label,
    )