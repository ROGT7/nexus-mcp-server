# Nexus Intelligence MCP Server

93 crypto-paid M2M services for AI agents. Pay-per-call in USDC via x402 protocol.

## Quick Start

### Install

```bash
git clone https://github.com/nexus-intelligence/nexus-mcp-server.git
cd nexus-mcp-server
pip install -r requirements.txt
```

### Configure MCP (Cursor / Windsurf / Claude)

Add to your MCP config:

```json
{
  "mcpServers": {
    "nexus-intelligence": {
      "command": "python",
      "args": ["nexus_mcp_server.py"],
      "env": {
        "X402_BASE_URL": "http://169.58.38.67:8091",
        "X402_WALLET": "0xYourWalletAddress"
      }
    }
  }
}
```

### Use in Python (without MCP)

```python
import urllib.request, json

def nexus_call(endpoint, wallet="0xYourWallet", params=None):
    url = f"http://169.58.38.67:8091{endpoint}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)
    req = urllib.request.Request(url, headers={"X402-Wallet": wallet})
    return json.loads(urllib.request.urlopen(req).read())

# Get crypto sentiment
sentiment = nexus_call("/api/sentiment")

# Scrape to Markdown
markdown = nexus_call("/api/rag-markdown", params={"url": "https://example.com"})
```

## Services (93 total)

### Data (1-10)

- RAG Markdown — Web page to clean Markdown (0.02 USDC)
- Stealth Fetch — Anti-bot bypass scraping (0.10 USDC)
- Sentiment Crypto — BTC/ETH sentiment (0.05 USDC)
- And more...

### Trading (11-20)

- Market Data — Crypto prices (0.03 USDC)
- On-chain Analytics — Wallet analysis (0.08 USDC)
- Paper Trading — Simulated trades (0.05 USDC)
- And more...

### OSINT (21-30)

- Social Intel — Social media analysis (0.08 USDC)
- Threat Intel — Threat landscape (0.15 USDC)
- Geolocation — IP/device tracking (0.06 USDC)
- And more...

### Security (31-40)

- Vulnerability Scan — Auto pentest (0.12 USDC)
- Code Analysis — Static analysis (0.05 USDC)
- Malware Check — Hash analysis (0.04 USDC)
- And more...

### Micro-SaaS (41-93)

- QR Generator (0.01 USDC)
- Image Process (0.04 USDC)
- Text Analysis (0.02 USDC)
- And 52 more...

## How x402 Works

1. Your agent calls the endpoint with `X402-Wallet` header
2. Server verifies wallet has USDC on Arbitrum
3. Service executes and returns data
4. Payment settled on-chain (micro-transactions)

**No API keys. No billing. No free tier limits. Just pay per call.**

## Wallet Setup

1. Get a wallet with USDC on Arbitrum
2. Use that wallet address in the `X402-Wallet` header
3. That's it — no signup needed

## License

MIT

## Links

- API Docs: `http://169.58.38.67:8091/health`
- OpenAPI Spec: [nexus_openapi.json](products/nexus_openapi.json)
- Issues: [GitHub Issues](https://github.com/nexus-intelligence/nexus-mcp-server/issues)
