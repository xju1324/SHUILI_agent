"""
MCP Server 独立启动脚本（stdio 传输模式）
用于验证 MCP Server 可正常启动，工具列表正确暴露

启动方式:
    python run_mcp.py

或配置在 Claude Desktop / Cursor 等 MCP 客户端中:
    {
        "mcpServers": {
            "water-supervision-mcp": {
                "command": "python",
                "args": ["run_mcp.py"],
                "cwd": "/path/to/ai-service"
            }
        }
    }
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.stdio import stdio_server

from app.services import RAGService
from app.mcp_tools import init_mcp_tools
from app.mcp.server import create_mcp_server

rag_service = RAGService()
init_mcp_tools(rag_service)
mcp_server = create_mcp_server(rag_service)


async def main():
    print(f"[MCP] water-supervision-mcp 启动中（stdio 模式）...", file=sys.stderr)
    print(
        f"[MCP] 知识库状态: {'就绪' if rag_service.is_ready() else '空（请先加载文档）'}",
        file=sys.stderr,
    )
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
