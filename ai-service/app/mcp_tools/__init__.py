from app.services.rag_service import RAGService
from app.mcp_tools.knowledge_search import knowledge_search, init_tool as init_ks
from app.mcp_tools.check_completeness import check_completeness

__all__ = ["knowledge_search", "check_completeness", "init_mcp_tools"]


def init_mcp_tools(rag: RAGService):
    """初始化所有 MCP 工具（注入共享依赖）"""
    init_ks(rag)
