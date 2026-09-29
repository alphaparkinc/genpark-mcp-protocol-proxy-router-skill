"""MCP Protocol Proxy Router & Tool Dispatcher.
100% Python Standard Library.
"""

import json

class MCPProxyRouter:
    """JSON-RPC 2.0 router dispatching tool calls and handling MCP capability negotiations."""
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, description, handler, input_schema=None):
        self.tools[name] = {
            "name": name,
            "description": description,
            "handler": handler,
            "inputSchema": input_schema or {"type": "object", "properties": {}}
        }

    def dispatch(self, json_rpc_req):
        method = json_rpc_req.get("method")
        req_id = json_rpc_req.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "mcp-proxy-router", "version": "1.0.0"}
                }
            }
        elif method == "tools/list":
            tool_list = [{"name": t["name"], "description": t["description"], "inputSchema": t["inputSchema"]} for t in self.tools.values()]
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tool_list}}
        elif method == "tools/call":
            params = json_rpc_req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})
            if name in self.tools:
                try:
                    res = self.tools[name]["handler"](args)
                    return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
                except Exception as e:
                    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{name}' not found"}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
