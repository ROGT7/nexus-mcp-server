#!/usr/bin/env python3
"""
Nexus Intelligence MCP Server
Wraps the 93 x402 M2M services as MCP tools for AI agents.
Agents can call these tools and pay via x402 protocol.

Usage:
    python nexus_mcp_server.py

Or with MCP client (Cursor, Windsurf, Claude):
    Add to MCP config: {"command": "python", "args": ["nexus_mcp_server.py"]}
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

# MCP server protocol (stdio-based)
class NexusMCPServer:
    def __init__(self):
        self.registry_path = Path(__file__).parent / "memory" / "m2m_service_registry.json"
        self.services = self._load_services()
        self.x402_base_url = os.environ.get("X402_BASE_URL", "http://169.58.38.67:8091")
        self.wallet = os.environ.get("X402_WALLET", "0xcb648B5233af72b32319B2F5d7508f7C1433d9c8")

    def _load_services(self):
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        services = []
        for s in data.get("core_services", []):
            services.append(s)
        for s in data.get("alternative_services", []):
            services.append(s)
        return services

    def _call_x402(self, endpoint, params=None):
        url = f"{self.x402_base_url}{endpoint}"
        if params:
            import urllib.parse
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            "X402-Wallet": self.wallet,
            "User-Agent": "Nexus-MCP/1.0"
        })
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}

    def list_tools(self):
        tools = []
        for svc in self.services:
            tool = {
                "name": f"nexus_{svc['id']}_{svc['endpoint'].replace('/', '_').strip('_')}",
                "description": f"{svc['name']} - {svc.get('description', '')} (Price: {svc.get('price_usdc', 0)} USDC)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Input parameter for the service"}
                    }
                }
            }
            tools.append(tool)
        tools.append({
            "name": "nexus_list_services",
            "description": "List all available Nexus M2M services with prices",
            "inputSchema": {"type": "object", "properties": {}}
        })
        return tools

    def call_tool(self, name, args):
        if name == "nexus_list_services":
            return {"content": [{"type": "text", "text": json.dumps([
                {"id": s["id"], "name": s["name"], "price": s.get("price_usdc", 0), "endpoint": s["endpoint"]}
                for s in self.services
            ], indent=2)}]}

        # Parse service ID from tool name
        parts = name.split("_")
        if len(parts) >= 2 and parts[0] == "nexus":
            try:
                svc_id = int(parts[1])
                svc = next((s for s in self.services if s["id"] == svc_id), None)
                if svc:
                    result = self._call_x402(svc["endpoint"], args if isinstance(args, dict) else None)
                    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            except ValueError:
                pass
        return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

    def run_stdio(self):
        """Run MCP server over stdio protocol."""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                msg = json.loads(line)
                method = msg.get("method", "")

                if method == "initialize":
                    response = {"jsonrpc": "2.0", "id": msg["id"], "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "nexus-intelligence", "version": "1.0.0"}
                    }}
                elif method == "tools/list":
                    response = {"jsonrpc": "2.0", "id": msg["id"], "result": {"tools": self.list_tools()}}
                elif method == "tools/call":
                    result = self.call_tool(msg["params"]["name"], msg["params"].get("arguments", {}))
                    response = {"jsonrpc": "2.0", "id": msg["id"], "result": result}
                else:
                    response = {"jsonrpc": "2.0", "id": msg.get("id", 0), "error": {"code": -1, "message": f"Unknown method: {method}"}}

                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")


if __name__ == "__main__":
    server = NexusMCPServer()
    server.run_stdio()
