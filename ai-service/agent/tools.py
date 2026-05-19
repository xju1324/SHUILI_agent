"""LangChain Agent 工具 — 委托到 app/mcp_tools 实现函数"""
from langchain_core.tools import tool

from app.mcp_tools import knowledge_search as _impl_knowledge_search
from app.mcp_tools import check_completeness as _impl_check_completeness


@tool(description="搜索涉水审批法规知识库。输入 query（查询语句）和可选的 category（审批类型），返回相关法规片段及其来源和相似度分数。")
async def knowledge_search(query: str, category: str = None) -> str:
    return await _impl_knowledge_search(query=query, category=category)


@tool(description="检查申请材料的完整性。输入 material_data（包含 category 和各字段的材料字典），返回缺失的字段和附件清单。")
async def check_completeness(material_data: dict) -> str:
    return await _impl_check_completeness(material_data=material_data)
