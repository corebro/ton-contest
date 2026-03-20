from __future__ import annotations

from dataclasses import dataclass

from services.parsing.classifier import classify_transaction
from services.ton.ton_models import NormalizedTransaction


@dataclass(slots=True)
class FlowResult:
    flow: list[str]
    patterns: list[str]


def build_flow_result(transactions: list[NormalizedTransaction]) -> FlowResult:
    raw_flow = [classify_transaction(tx) for tx in transactions]

    flow: list[str] = []
    for item in raw_flow:
        if not flow or flow[-1] != item:
            flow.append(item)

    if not flow:
        flow = ["Unknown"]

    patterns: list[str] = []

    jetton_ops = sum(1 for tx in transactions if tx.asset_type == "Jetton")
    nft_ops = sum(1 for tx in transactions if tx.asset_type == "NFT")

    unique_counterparties = set()
    for tx in transactions:
        if tx.account_address and tx.from_address == tx.account_address and tx.to_address != "unknown":
            unique_counterparties.add(tx.to_address)
        elif tx.account_address and tx.to_address == tx.account_address and tx.from_address != "unknown":
            unique_counterparties.add(tx.from_address)

    if jetton_ops > 0:
        patterns.append("token-related activity")

    if nft_ops > 0:
        patterns.append("nft-related activity")

    if len(unique_counterparties) >= 20:
        patterns.append("broad interaction with many counterparties")
    elif len(unique_counterparties) >= 5:
        patterns.append("repeated transfers across several counterparties")

    if len(flow) >= 4:
        patterns.append("multi-step contract path")

    if not patterns:
        if flow == ["Wallet"]:
            patterns.append("mostly direct wallet activity")
        elif flow == ["Contract"]:
            patterns.append("repeated smart contract interaction")
        else:
            patterns.append("mixed wallet and contract interaction")

    return FlowResult(flow=flow, patterns=patterns)