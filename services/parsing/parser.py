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

    patterns: list[str] = []
    lowered_flow = [item.lower() for item in flow]

    if lowered_flow.count("router") >= 1 and lowered_flow.count("pool") >= 1:
        patterns.append("swap-like routing through contracts")
    if lowered_flow.count("jetton") >= 1:
        patterns.append("token-related activity")
    if lowered_flow.count("nft marketplace") >= 1:
        patterns.append("nft-related activity")
    if len(flow) >= 4:
        patterns.append("multi-step contract path")

    if not patterns:
        patterns.append("mostly direct wallet and contract interaction")

    return FlowResult(flow=flow, patterns=patterns)
