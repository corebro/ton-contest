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


def _collect_out_destinations(out_msgs: list[Any]) -> list[str]:
    result: list[str] = []
    for msg in out_msgs:
        if not isinstance(msg, dict):
            continue
        out_dest = msg.get("destination") or msg.get("to") or msg.get("recipient")
        out_addr = _extract_address(out_dest)
        if out_addr != "unknown":
            result.append(out_addr)
    return result


def _detect_asset_type(item: dict[str, Any], text_blob: str) -> str:
    actions = item.get("actions") or []
    action_blob = " ".join(str(a) for a in actions).lower()

    if (
        item.get("nft")
        or "nft" in text_blob
        or "nft" in action_blob
        or "getgems" in text_blob
        or "getgems" in action_blob
        or "marketplace" in text_blob
    ):
        return "NFT"

    if (
        item.get("jetton")
        or "jetton" in text_blob
        or "jetton" in action_blob
        or "token" in text_blob
        or "swap" in text_blob
        or "ston" in text_blob
        or "dedust" in text_blob
    ):
        return "Jetton"

    return "TON"


def normalize_transaction(item: dict[str, Any], target_address: str) -> NormalizedTransaction:
    in_msg = item.get("in_msg") or {}
    out_msgs = item.get("out_msgs") or []

    tx_hash = item.get("hash") or item.get("tx_hash") or item.get("transaction_id") or "unknown"

    source_obj = in_msg.get("source") or item.get("from") or item.get("sender")
    destination_obj = in_msg.get("destination") or item.get("to") or item.get("recipient")

    from_address = _extract_address(source_obj)
    to_address = _extract_address(destination_obj)

    out_destinations = _collect_out_destinations(out_msgs)
    if to_address == "unknown" and out_destinations:
        to_address = out_destinations[0]

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

    if destination_label is None and out_msgs:
        first_out = out_msgs[0] if isinstance(out_msgs[0], dict) else {}
        destination_label = _extract_name(
            first_out.get("destination") or first_out.get("to") or first_out.get("recipient")
        )

    contract_label = (
        destination_label
        or description.get("action")
        or description.get("type")
    )

    comment = in_msg.get("message")
    if not comment and out_msgs:
        first_out = out_msgs[0] if isinstance(out_msgs[0], dict) else {}
        comment = first_out.get("message")

    text_blob = " ".join(
        str(x)
        for x in [
            tx_type,
            contract_label,
            source_label,
            destination_label,
            comment,
            item.get("type"),
            item.get("action"),
        ]
        if x
    ).lower()

    asset_type = _detect_asset_type(item, text_blob)

    direction = "unknown"
    counterparty_address = "unknown"

    if from_address == target_address and to_address != "unknown":
        direction = "outgoing"
        counterparty_address = to_address
    elif to_address == target_address and from_address != "unknown":
        direction = "incoming"
        counterparty_address = from_address
    elif out_destinations:
        direction = "outgoing"
        counterparty_address = out_destinations[0]
    elif from_address != "unknown" and from_address != target_address:
        direction = "incoming"
        counterparty_address = from_address
    elif to_address != "unknown" and to_address != target_address:
        counterparty_address = to_address

    return NormalizedTransaction(
        tx_hash=tx_hash,
        account_address=target_address,
        from_address=from_address,
        to_address=to_address,
        counterparty_address=counterparty_address,
        direction=direction,
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