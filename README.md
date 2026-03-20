# TON X-Ray

AI-powered Telegram bot for quick TON wallet analysis.

🎥 Demo video:  
https://www.youtube.com/watch?v=D71Oj5jhkm4

---

## What it does
TON X-Ray analyzes recent TON wallet activity and explains it in simple human language.

- Fetches recent transactions via TON API
- Extracts key metrics (counterparties, volume, flow)
- Generates a short AI summary of behavior

---

## Positioning
This is **not**:
- a scam detector
- a reputation score
- a wallet

This **is**:
- a simple tool to understand TON transaction activity

---

## Features
- Telegram bot (`aiogram`)
- Wallet address or transaction input
- Real-time TON API integration
- Basic flow parsing
- AI explanation (3–5 sentences)
- Clean demo-ready output

---

## Quick start

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure
Create `.env`:
```env
TELEGRAM_BOT_TOKEN=...
OPENAI_API_KEY=...
TONAPI_API_KEY=...  # optional
```

### Run
```bash
python main.py
```

---

## How it works
1. User sends a TON address  
2. Bot fetches recent transactions  
3. Parser extracts simple metrics  
4. AI generates a short explanation  
5. Result is returned in Telegram  

---

## Example output
```text
🔍 TON X-Ray

Target: EQ...

Stats:
• Transactions analyzed: 100
• Unique counterparties: 42
• Incoming ops: 99
• Outgoing ops: 1

AI Insight:
Based on recent transactions, the wallet appears to mostly receive transfers from multiple sources...
```

---

## Why this project
- Makes TON activity easier to understand
- Works instantly inside Telegram
- No blockchain expertise required

---

## Future improvements
- Better contract detection
- Trace-based analysis
- Jetton/NFT enrichment
- Caching and performance improvements
