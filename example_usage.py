from client import MCPProxyRouter

router = MCPProxyRouter()
router.register_tool("calculate_sum", "Sum numbers", lambda args: sum(args.get("values", [])))

res = router.dispatch({
    "jsonrpc": "2.0",
    "id": "req-1",
    "method": "tools/call",
    "params": {"name": "calculate_sum", "arguments": {"values": [10, 25, 45]}}
})
print("MCP Dispatch Response:", res)
