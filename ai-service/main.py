"""
涉水审批智能审核系统 - Python AI 服务
FastAPI + MCP Server + LangChain Agent + ChromaDB
"""
import os
import json
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route

from config import HOST, PORT, CHROMA_PERSIST_DIR, AUTO_LOAD_KNOWLEDGE
from app.services import RAGService
from app.mcp_tools import (
    knowledge_search,
    check_completeness,
    init_mcp_tools,
)
from app.mcp.server import create_mcp_server
from agent import WaterReviewAgent

# ============================================================
# 全局服务初始化
# ============================================================
rag_service = RAGService()
init_mcp_tools(rag_service)
water_agent = WaterReviewAgent()
mcp_server = create_mcp_server(rag_service)


# ============================================================
# FastAPI 应用
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    if AUTO_LOAD_KNOWLEDGE and (not rag_service.is_ready() or rag_service.get_document_count() == 0):
        print("[启动] RAG 知识库为空，尝试自动加载文档...")
        chunks_created = rag_service.load_documents()
        doc_count = rag_service.get_document_count()
        print(f"[启动] RAG 自动加载完成，本次创建 chunks: {chunks_created}，当前文档块数: {doc_count}")
    else:
        doc_count = rag_service.get_document_count()
        ready_text = "就绪" if rag_service.is_ready() else "空（请先加载文档）"
        print(f"[启动] RAG 知识库状态: {ready_text}，当前文档块数: {doc_count}")
    print(f"[启动] MCP Server '{mcp_server.name}' 已就绪")
    yield


app = FastAPI(
    title="涉水审批智能审核 AI 服务",
    description="提供 RAG 检索、合规审查、MCP 工具调用能力",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 请求模型 ---
class MaterialReviewRequest(BaseModel):
    material_id: Optional[int] = None
    category: str = "WATER_INTAKE"
    title: Optional[str] = None
    projectName: Optional[str] = None
    applicantCompany: Optional[str] = None
    applicantLegalPerson: Optional[str] = None
    businessLicenseNo: Optional[str] = None
    contactPhone: Optional[str] = None
    waterIntakeLocation: Optional[str] = None
    waterIntakePurpose: Optional[str] = None
    annualWaterVolume: Optional[float] = None
    waterSourceType: Optional[str] = None
    projectLocation: Optional[str] = None
    riverName: Optional[str] = None
    floodControlStandard: Optional[str] = None
    constructionContent: Optional[str] = None
    projectArea: Optional[float] = None
    soilLossAmount: Optional[float] = None
    conservationMeasures: Optional[str] = None
    constructionType: Optional[str] = None
    occupationLength: Optional[float] = None
    outletLocation: Optional[str] = None
    sewageType: Optional[str] = None
    dischargeAmount: Optional[float] = None
    dischargeStandard: Optional[str] = None
    receivingWater: Optional[str] = None
    riverSection: Optional[str] = None
    sandType: Optional[str] = None
    annualMiningAmount: Optional[float] = None
    miningMethod: Optional[str] = None
    applicationFormPath: Optional[str] = None
    businessLicensePath: Optional[str] = None
    idCardPath: Optional[str] = None
    waterCertificatePath: Optional[str] = None
    formData: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    top_k: int = 5


# ============================================================
# API 端点
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "water-supervision-ai",
        "rag_ready": rag_service.is_ready(),
        "doc_count": rag_service.get_document_count(),
        "mcp_server": mcp_server.name,
    }


@app.post("/api/review")
async def review_endpoint(req: MaterialReviewRequest):
    """涉水审批材料智能审查"""
    material_data = req.model_dump(exclude_none=True)
    if req.formData:
        try:
            material_data.update(json.loads(req.formData))
        except json.JSONDecodeError:
            pass

    try:
        # 1. 完整性检查
        completeness = await check_completeness(material_data)
        # 2. 法规检索
        search_query = _build_search_query(material_data)
        regulations = await knowledge_search(query=search_query, category=req.category)
        # 3. LLM 生成审查报告
        from model.factory import create_llm
        llm = create_llm()
        prompt = f"""你是涉水审批智能审核助手。请根据以下信息生成审查报告：

## 材料信息
{json.dumps(material_data, ensure_ascii=False, indent=2)}

## 完整性检查结果
{completeness}

## 相关法规
{regulations}

## 请按以下格式输出审查报告：
### 一、完整性检查
### 二、法规依据
### 三、合规性评估（逐项标注 ✅合规 ⚠️需关注 ❌不合规）
### 四、审查结论与修改建议"""
        response = await llm.ainvoke(prompt)
        review_result = response.content if hasattr(response, "content") else str(response)

        return {
            "material_id": req.material_id,
            "category": req.category,
            "review_result": review_result,
            "status": "completed",
        }
    except Exception as e:
        return {
            "material_id": req.material_id,
            "status": "failed",
            "error": str(e),
        }


@app.post("/api/review/quick")
async def quick_review(req: MaterialReviewRequest):
    """快速审查（仅执行完整性检查 + 法规检索，不经过 Agent）"""
    material_data = req.model_dump(exclude_none=True)
    if req.formData:
        try:
            material_data.update(json.loads(req.formData))
        except json.JSONDecodeError:
            pass

    completeness = await check_completeness(material_data)
    search_query = _build_search_query(material_data)
    regulations = await knowledge_search(query=search_query, category=req.category)

    return {
        "material_id": req.material_id,
        "category": req.category,
        "completeness_check": completeness,
        "regulation_search": regulations,
        "status": "completed",
    }


@app.post("/api/review/stream")
async def review_stream(req: MaterialReviewRequest):
    """流式审查（SSE 推送 token 级别输出）"""
    material_data = req.model_dump(exclude_none=True)
    if req.formData:
        try:
            material_data.update(json.loads(req.formData))
        except json.JSONDecodeError:
            pass

    async def event_generator():
        async for chunk in water_agent.execute_stream(material_data):
            yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/api/knowledge/load")
async def load_knowledge(doc_dir: Optional[str] = None):
    """加载/重新加载知识库文档"""
    count = rag_service.load_documents(doc_dir)
    return {
        "status": "ok",
        "chunks_created": count,
        "doc_count": rag_service.get_document_count(),
    }


@app.post("/api/knowledge/search")
async def search_knowledge(req: SearchRequest):
    """直接检索知识库"""
    results = rag_service.search(req.query, k=req.top_k)
    return {
        "query": req.query,
        "results": results,
        "count": len(results),
    }


@app.get("/api/knowledge/status")
async def knowledge_status():
    """知识库状态"""
    return {
        "ready": rag_service.is_ready(),
        "doc_count": rag_service.get_document_count(),
        "persist_dir": os.path.abspath(CHROMA_PERSIST_DIR),
    }


# ============================================================
# MCP SSE 传输（挂载在 /mcp 路径）
# ============================================================
sse_transport = SseServerTransport("/messages/")


async def mcp_sse_endpoint(request):
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options(),
        )


async def mcp_messages_endpoint(request):
    await sse_transport.handle_post_message(
        request.scope, request.receive, request._send
    )


mcp_subapp = Starlette(
    routes=[
        Route("/sse", mcp_sse_endpoint, methods=["GET"]),
        Route("/messages/", mcp_messages_endpoint, methods=["POST"]),
    ]
)

app.mount("/mcp", mcp_subapp)


# ============================================================
# 辅助函数
# ============================================================
def _build_search_query(material_data: dict) -> str:
    """根据材料数据构建法规检索查询"""
    category = material_data.get("category", "WATER_INTAKE")
    queries = {
        "WATER_INTAKE": f"取水许可申请条件 取水地点: {material_data.get('waterIntakeLocation', '')} 取水用途: {material_data.get('waterIntakePurpose', '')}",
        "FLOOD_IMPACT": f"洪水影响评价审批要求 河流: {material_data.get('riverName', '')} 防洪标准: {material_data.get('floodControlStandard', '')}",
        "SOIL_CONSERVATION": f"水土保持方案审批标准 占地面积: {material_data.get('projectArea', '')} 土壤流失量: {material_data.get('soilLossAmount', '')}",
        "RIVER_CONSTRUCTION": f"河道管理范围建设项目审批 建设类型: {material_data.get('constructionType', '')} 占用长度: {material_data.get('occupationLength', '')}",
        "SEWAGE_OUTLET": f"入河排污口设置审批 污水类型: {material_data.get('sewageType', '')} 排放标准: {material_data.get('dischargeStandard', '')}",
        "SAND_MINING": f"河道采砂许可审批 采砂河段: {material_data.get('riverSection', '')} 开采量: {material_data.get('annualMiningAmount', '')}",
    }
    return queries.get(category, f"涉水审批法规要求 项目: {material_data.get('projectName', '')}")


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
