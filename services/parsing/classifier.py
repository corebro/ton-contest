from __future__ import annotations

from services.ton.ton_models import NormalizedTransaction


def classify_transaction(tx: NormalizedTransaction) -> str:
    tx_type = tx.tx_type.lower()
    label = (tx.contract_label or "").lower()
    comment = (tx.comment or "").lower()

    if tx.asset_type == "NFT" or "nft" in tx_type or "nft" in label:
        return "NFT Marketplace"
    if tx.asset_type == "Jetton" or "jetton" in tx_type or "token" in tx_type:
        return "Jetton"
    if any(word in tx_type or word in label or word in comment for word in ["swap", "dex", "router"]):
        return "Router"
    if any(word in tx_type or word in label or word in comment for word in ["pool", "liquidity", "lp"]):
        return "Pool"
    if tx.to_address.startswith("EQ") or tx.from_address.startswith("EQ"):
        return "Wallet"
    return "Contract"
