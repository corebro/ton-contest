from __future__ import annotations

from services.ton.ton_models import NormalizedTransaction


KNOWN_LABEL_RULES = {
    "ston": "Router",
    "dedust": "Router",
    "swap": "Router",
    "router": "Router",
    "pool": "Pool",
    "liquidity": "Pool",
    "lp": "Pool",
    "nft": "NFT Marketplace",
    "getgems": "NFT Marketplace",
    "marketplace": "NFT Marketplace",
    "collection": "NFT Marketplace",
    "validator": "Validator",
    "staking": "Staking",
    "stake": "Staking",
    "exchange": "Exchange",
    "wallet": "Wallet",
}


def _looks_like_wallet_address(address: str) -> bool:
    if not address or address == "unknown":
        return False

    if len(address) == 48:
        return True

    if ":" in address:
        left, _, right = address.partition(":")
        if right and len(right) == 64:
            return True

    return False


def _classify_by_text(text: str) -> str | None:
    lowered = text.lower()
    for key, value in KNOWN_LABEL_RULES.items():
        if key in lowered:
            return value
    return None


def classify_transaction(tx: NormalizedTransaction) -> str:
    tx_type = (tx.tx_type or "").lower()
    label = (tx.contract_label or "").lower()
    comment = (tx.comment or "").lower()
    source_label = (tx.source_label or "").lower()
    destination_label = (tx.destination_label or "").lower()

    combined = f"{tx_type} {label} {comment} {source_label} {destination_label}".strip()

    text_based = _classify_by_text(combined)
    if text_based:
        return text_based

    if tx.asset_type == "NFT":
        return "NFT Marketplace"

    if tx.asset_type == "Jetton":
        return "Jetton"

    from_is_wallet = _looks_like_wallet_address(tx.from_address)
    to_is_wallet = _looks_like_wallet_address(tx.to_address)

    if from_is_wallet and to_is_wallet:
        return "Wallet"

    if from_is_wallet or to_is_wallet:
        return "Contract"

    return "Contract"