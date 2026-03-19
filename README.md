# TON X-Ray

We reveal what actually happens inside TON transactions — not just raw data, but flow, structure, and meaning.

## What it is
TON X-Ray is a simple Telegram bot that accepts a TON wallet address or a transaction hash, fetches recent on-chain activity from TON API, builds a lightweight flow, and asks OpenAI to explain the behavior in human language.

## Positioning
This is **not**:
- a scam detector
- a reputation score
- a wallet

This **is**:
- an AI assistant for understanding TON transaction behavior

## MVP features
- Telegram bot on `aiogram`
- Address or transaction hash input
- Recent TON transaction fetch via `tonapi.io`
- Simple flow parsing
- AI explanation in 3–5 sentences
- Clean Telegram output for demo

## Project structure
```text
bot/
  handlers/
core/
services/
  ai/
  formatting/
  parsing/
  ton/
utils/
main.py
```

## Quick start
### 1. Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure
Copy `.env.example` to `.env` and fill in:
- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- optional `TONAPI_API_KEY`

### 3. Run
```bash
python main.py
```

## User flow
### `/start`
Bot says:
```text
Send a TON wallet address or transaction hash to analyze its flow and behavior.
```

### User sends
```text
EQC123...
```
or
```text
0xabc123...
```

### Bot returns
```text
🔍 TON X-Ray

Target: EQ...
Flow:
Wallet → Router → Pool → Jetton → NFT Marketplace

Stats:
• Transactions analyzed: 12
• Unique contracts: 4
• Hidden steps: 3
• Jetton-related ops: 5
• NFT-related ops: 1

Observed patterns:
• swap-like routing through contracts
• token-related activity
• nft-related activity

AI Insight:
This address appears to use TON DeFi infrastructure rather than making only direct transfers...
```

## Notes on implementation
- `services/ton/ton_api.py` contains the required methods:
  - `get_wallet_transactions(address)`
  - `get_transaction(tx_hash)`
- `services/parsing/parser.py` builds a simplified flow for MVP
- `services/ai/analyzer.py` sends a compact factual prompt to OpenAI
- `services/formatting/formatter.py` builds a judge-friendly message

## Why this fits the hackathon
### Product quality
Clean Telegram UX and easy live demo.

### Technical execution
Real TON API integration, transaction extraction, parser layer, and AI explanation.

### Ecosystem value
Can be integrated into wallets, escrow systems, and DeFi tools to provide explainable transaction insights.

### User potential
Built for beginners and advanced users. Simplifies blockchain complexity.

## Fast demo plan
1. Run the bot
2. Send one TON address
3. Show the flow
4. Show the AI explanation
5. Done in under 10 seconds

## Future upgrades
- Better contract labeling
- Trace-based analysis
- TON Center v3 fallback
- Jetton/NFT enrichment
- Caching and rate-limit handling
- Inline buttons and history
