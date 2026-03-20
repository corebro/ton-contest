from __future__ import annotations

from collections import Counter

from services.ton.ton_models import NormalizedTransaction


def _looks_like_wallet_address(address: str) -> bool:
    if not address or address == "unknown":
        return False

    if len(address) == 48:
        return True

    if ":" in address:
        _, _, right = address.partition(":")
        if len(right) == 64:
            return True

    return False


def build_stats(transactions: list[NormalizedTransaction], flow: list[str]) -> dict[str, int | float | str]:
    if not transactions:
        return {
            "transactions_count": 0,
            "contracts_count": 0,
            "hidden_steps": 0,
            "jetton_ops": 0,
            "nft_ops": 0,
            "unique_addresses": 0,
            "incoming_ops": 0,
            "outgoing_ops": 0,
            "avg_amount": 0.0,
            "max_amount": 0.0,
            "top_counterparty": "n/a",
        }

    target = transactions[0].account_address

    counterparties: list[str] = []
    incoming = 0
    outgoing = 0
    amounts: list[float] = []

    for tx in transactions:
        if tx.amount > 0:
            amounts.append(tx.amount)

        if tx.to_address == target:
            incoming += 1
            if tx.from_address != "unknown":
                counterparties.append(tx.from_address)

        elif tx.from_address == target:
            outgoing += 1
            if tx.to_address != "unknown":
                counterparties.append(tx.to_address)

        else:
            # fallback for malformed / partial tx data
            if tx.from_address != "unknown":
                counterparties.append(tx.from_address)
            if tx.to_address != "unknown":
                counterparties.append(tx.to_address)

    unique_addresses = set(counterparties)

    # считаем "контрактами" только те контрагенты, которые не похожи на обычные адреса кошельков
    contract_counterparties = {
        addr for addr in unique_addresses if not _looks_like_wallet_address(addr)
    }

    top_counterparty = "n/a"
    if counterparties:
        top_counterparty = Counter(counterparties).most_common(1)[0][0]

    return {
        "transactions_count": len(transactions),
        "contracts_count": len(contract_counterparties),
        "hidden_steps": max(len(flow) - 2, 0),
        "jetton_ops": sum(1 for tx in transactions if tx.asset_type == "Jetton"),
        "nft_ops": sum(1 for tx in transactions if tx.asset_type == "NFT"),
        "unique_addresses": len(unique_addresses),
        "incoming_ops": incoming,
        "outgoing_ops": outgoing,
        "avg_amount": round(sum(amounts) / len(amounts), 4) if amounts else 0.0,
        "max_amount": round(max(amounts), 4) if amounts else 0.0,
        "top_counterparty": top_counterparty,
    }