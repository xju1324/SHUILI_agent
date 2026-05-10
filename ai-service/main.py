"""
取水许可材料智能审查系统 - Python AI 服务
FastAPI + LangChain + ChromaDB + MCP
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import HOST, PORT

app = FastAPI(
    title="取水许可材料智能审查 AI 服务",
    description="提供 RAG 检索、合规审查、MCP 工具调用能力",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "water-permit-ai"}


@app.get("/api/review")
async def review_endpoint():
    """审查接口（节点二/三实现具体逻辑）"""
    return {"message": "审查功能将在后续节点实现", "status": "pending"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
