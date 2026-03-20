from __future__ import annotations

from typing import Any


def build_analysis_prompt(
    flow: list[str],
    stats: dict[str, Any],
    patterns: list[str],
) -> str:
    flow_str = " → ".join(flow) if flow else "Simple transfer pattern"
    patterns_str = ", ".join(patterns) if patterns else "no strong pattern detected"

    visible_stats = [
        ("transactions_count", stats.get("transactions_count")),
        ("unique_addresses", stats.get("unique_addresses")),
        ("incoming_ops", stats.get("incoming_ops")),
        ("outgoing_ops", stats.get("outgoing_ops")),
        ("avg_amount", stats.get("avg_amount")),
        ("max_amount", stats.get("max_amount")),
        ("top_counterparty", stats.get("top_counterparty")),
        ("jetton_ops", stats.get("jetton_ops")),
        ("nft_ops", stats.get("nft_ops")),
    ]
    stats_str = "\n".join(f"- {key}: {value}" for key, value in visible_stats)

    return f"""
You are a TON blockchain analyst.

Your job is to summarize RECENT wallet activity using only the provided facts.
Do not claim certainty when the evidence is limited.
Use cautious wording such as:
- appears
- suggests
- likely
- based on recent transactions

Rules:
1. Do not call the wallet safe or unsafe.
2. Do not invent intent, fraud, laundering, manipulation, or risk labels.
3. Do not mention hidden routing unless the data explicitly supports it.
4. If the profile is mostly wallet-to-wallet transfers, say so directly.
5. If jetton_ops is 0 and nft_ops is 0, explicitly state that no clear jetton or NFT activity was detected in the recent sample.
6. Keep the answer to 3-5 short sentences.
7. Focus only on recent observable activity, not the full lifetime history of the wallet.

Interaction profile: {flow_str}
Observed patterns: {patterns_str}
Stats:
{stats_str}
""".strip()