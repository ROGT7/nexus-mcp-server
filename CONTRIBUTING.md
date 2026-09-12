# Contributing to Nexus MCP Server

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Adding New Services

To add a new M2M service to the x402 catalog:

1. Add the service definition to `m2m_service_registry.json`
2. The MCP server will automatically expose it as a new tool
3. Test with: `python nexus_mcp_server.py`
4. Verify the tool appears in `tools/list`

## Service Definition Format

```json
{
  "name": "your-service-name",
  "description": "What your service does",
  "endpoint": "/api/your-endpoint",
  "method": "POST",
  "price_usdc": 0.05,
  "category": "osint",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Search query"}
    },
    "required": ["query"]
  }
}
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Keep functions under 50 lines

## Testing

```bash
python _test_mcp.py
```

This will verify:
- MCP initialization
- Tool listing (94 tools expected)
- Service enumeration (93 services expected)
