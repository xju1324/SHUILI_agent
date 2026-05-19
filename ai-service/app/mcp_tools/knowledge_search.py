"""
MCP Tool: knowledge_search — 涉水法规知识库语义检索
接收查询语句，返回相关法规片段（含内容、来源、相似度分数）
"""
from typing import Optional
from app.services.rag_service import RAGService

_rag_service: Optional[RAGService] = None


def init_tool(rag: RAGService):
    global _rag_service
    _rag_service = rag


async def knowledge_search(query: str, category: str = None) -> str:
    """搜索涉水审批法规知识库，返回相关法规片段。

    Args:
        query: 查询语句，描述需要查找的法规内容
        category: 可选，审批类型过滤 (WATER_INTAKE/FLOOD_IMPACT/...)

    Returns:
        包含文档内容、来源、相似度分数的检索结果
    """
    if _rag_service is None:
        return "错误：知识库服务未初始化，请先加载文档。"

    if not _rag_service.is_ready():
        return "知识库为空，请先通过 /api/knowledge/load 加载法规文档。"

    results = _rag_service.search(query, k=5)
    if not results:
        return "未找到与查询相关的法规片段。"

    lines = [f"检索 query: {query}", f"共找到 {len(results)} 条相关法规片段：", ""]
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] 来源: {r['source']} | 相似度分数: {r['score']:.4f}")
        if r.get("page") is not None:
            lines[-1] += f" | 页码: {r['page']}"
        lines.append(f"    内容: {r['content']}")
        lines.append("")
    return "\n".join(lines)
