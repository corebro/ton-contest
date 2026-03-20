from __future__ import annotations


def format_flow(flow: list[str]) -> str:
    return " → ".join(flow) if flow else "Simple transfer pattern"


def build_analysis_response(
    target: str,
    flow: list[str],
    stats: dict[str, int | float | str],
    patterns: list[str],
    insight: str,
) -> str:
    patterns_block = "\n".join(f"• {item}" for item in patterns)
    stats_block = "\n".join(
        [
            f"• Transactions analyzed: {stats['transactions_count']}",
            f"• Unique contract-like counterparties: {stats['contracts_count']}",
            f"• Unique counterparties: {stats['unique_addresses']}",
            f"• Incoming ops: {stats['incoming_ops']}",
            f"• Outgoing ops: {stats['outgoing_ops']}",
            f"• Average amount: {stats['avg_amount']}",
            f"• Largest amount: {stats['max_amount']}",
            f"• Top counterparty: {stats['top_counterparty']}",
            f"• Hidden steps: {stats['hidden_steps']}",
            f"• Jetton-related ops: {stats['jetton_ops']}",
            f"• NFT-related ops: {stats['nft_ops']}",
        ]
    )

    return (
        "<b>🔍 TON X-Ray</b>\n\n"
        f"<b>Target:</b> <code>{target}</code>\n\n"
        f"<b>Interaction profile:</b>\n{format_flow(flow)}\n\n"
        f"<b>Stats:</b>\n{stats_block}\n\n"
        f"<b>Observed patterns:</b>\n{patterns_block}\n\n"
        f"<b>AI Insight:</b>\n{insight}"
    )