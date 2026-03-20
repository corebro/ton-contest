from __future__ import annotations

import re

# TON user-friendly address in base64/base64url form.
# In practice it is 48 chars and may contain letters, digits, '-' and '_'.
# Do not hardcode only EQ/UQ prefixes.
USER_FRIENDLY_TON_ADDRESS_RE = re.compile(r"^[A-Za-z0-9_-]{48}$")

# RAW TON address: workchain:64hex
RAW_TON_ADDRESS_RE = re.compile(r"^-?\d+:[a-fA-F0-9]{64}$")

# TON tx hash: 64 hex chars, optional 0x prefix
TON_TX_HASH_RE = re.compile(r"^(0x)?[a-fA-F0-9]{64}$")

# EVM/BEP20 wallet address: 0x + 40 hex
EVM_ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")


def is_ton_address(value: str) -> bool:
    return bool(
        USER_FRIENDLY_TON_ADDRESS_RE.fullmatch(value)
        or RAW_TON_ADDRESS_RE.fullmatch(value)
    )


def is_tx_hash(value: str) -> bool:
    return bool(TON_TX_HASH_RE.fullmatch(value))


def is_evm_address(value: str) -> bool:
    return bool(EVM_ADDRESS_RE.fullmatch(value))


def is_supported_input(value: str) -> bool:
    return is_ton_address(value) or is_tx_hash(value)


def detect_input_type(value: str) -> str:
    if is_ton_address(value):
        return "address"
    if is_tx_hash(value):
        return "tx_hash"
    return "unknown"