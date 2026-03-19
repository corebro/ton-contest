from __future__ import annotations


def build_analysis_prompt(
    flow: list[str],
    stats: dict[str, int],
    patterns: list[str],
) -> str:
    flow_str = " → ".join(flow)
    patterns_str = ", ".join(patterns)
    stats_str = "\n".join(f"- {key}: {value}" for key, value in stats.items())

    return f"""
You are a blockchain analyst for TON.
Explain the observed transaction behavior in plain English.
Do not call it safe or unsafe.
Do not speculate beyond the provided facts.
Write 3 to 5 short sentences.
Focus on:
1. flow structure,
2. repeated interaction patterns,
3. likely user intent,
4. whether activity looks like transfers, swaps, NFT actions, or contract routing.

Flow: {flow_str}
Patterns: {patterns_str}
Stats:
{stats_str}
""".strip()
