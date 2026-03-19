from __future__ import annotations


def format_flow(flow: list[str]) -> str:
    return " → ".join(flow) if flow else "Wallet"


def build_analysis_response(
    target: str,
    flow: list[str],
    stats: dict[str, int],
    patterns: list[str],
    insight: str,
) -> str:
    patterns_block = "\n".join(f"• {item}" for item in patterns)
    stats_block = "\n".join(
        [
            f"• Transactions analyzed: {stats['transactions_count']}",
            f"• Unique contracts: {stats['contracts_count']}",
            f"• Hidden steps: {stats['hidden_steps']}",
            f"• Jetton-related ops: {stats['jetton_ops']}",
            f"• NFT-related ops: {stats['nft_ops']}",
        ]
    )

    return (
        "<b>🔍 TON X-Ray</b>\n\n"
        f"<b>Target:</b> <code>{target}</code>\n\n"
        f"<b>Flow:</b>\n{format_flow(flow)}\n\n"
        f"<b>Stats:</b>\n{stats_block}\n\n"
        f"<b>Observed patterns:</b>\n{patterns_block}\n\n"
        f"<b>AI Insight:</b>\n{insight}"
    )
