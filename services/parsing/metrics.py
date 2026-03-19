from __future__ import annotations

from services.ton.ton_models import NormalizedTransaction


def build_stats(transactions: list[NormalizedTransaction], flow: list[str]) -> dict[str, int]:
    unique_addresses = {
        tx.to_address for tx in transactions if tx.to_address != "unknown"
    } | {
        tx.from_address for tx in transactions if tx.from_address != "unknown"
    }

    contracts_count = sum(1 for step in flow if step not in {"Wallet"})

    return {
        "transactions_count": len(transactions),
        "contracts_count": max(contracts_count, len(unique_addresses) // 4),
        "hidden_steps": max(len(flow) - 2, 0),
        "jetton_ops": sum(1 for tx in transactions if tx.asset_type == "Jetton"),
        "nft_ops": sum(1 for tx in transactions if tx.asset_type == "NFT"),
    }
