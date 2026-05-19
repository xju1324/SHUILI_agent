"""共享 MCP Server 工厂 — main.py 和 run_mcp.py 复用"""
from mcp.server import Server as MCPServer
from mcp.types import Tool as MCPTool, TextContent

from config import MCP_SERVER_NAME
from app.mcp_tools import knowledge_search, check_completeness


def create_mcp_server(rag_service=None) -> MCPServer:
    """
    创建并配置 MCP Server 实例。

    rag_service 参数保留用于未来扩展（如动态获取工具状态），
    当前工具通过 app.mcp_tools 模块级函数直接调用。
    """
    mcp_server = MCPServer(MCP_SERVER_NAME)

    @mcp_server.list_tools()
    async def list_tools() -> list[MCPTool]:
        return [
            MCPTool(
                name="knowledge_search",
                description="搜索涉水审批法规知识库，返回相关法规片段（包含文档来源和相似度分数）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "查询语句，如'取水许可的申请条件有哪些'",
                        },
                        "category": {
                            "type": "string",
                            "description": "审批类型（可选）：WATER_INTAKE/FLOOD_IMPACT/SOIL_CONSERVATION/RIVER_CONSTRUCTION/SEWAGE_OUTLET/SAND_MINING",
                        },
                    },
                    "required": ["query"],
                },
            ),
            MCPTool(
                name="check_completeness",
                description="检查涉水审批申请材料的完整性，对照各类审批的检查清单，返回缺失字段和附件报告",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "material_data": {
                            "type": "object",
                            "description": "包含 category 和各项字段/文件路径的材料数据字典",
                        }
                    },
                    "required": ["material_data"],
                },
            ),
        ]

    @mcp_server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == "knowledge_search":
            result = await knowledge_search(
                query=arguments.get("query", ""),
                category=arguments.get("category"),
            )
        elif name == "check_completeness":
            result = await check_completeness(arguments.get("material_data", {}))
        else:
            result = f"未知工具: {name}"
        return [TextContent(type="text", text=result)]

    return mcp_server
