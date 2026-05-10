"""AI服务全局配置"""

import os

# 服务配置
HOST = os.getenv("AI_HOST", "0.0.0.0")
PORT = int(os.getenv("AI_PORT", "8000"))

# ChromaDB 向量数据库路径
CHROMA_PERSIST_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")

# Embedding 模型 (中文优化)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")

# 知识库文档目录
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "../docs/knowledge")

# MCP Server 名称
MCP_SERVER_NAME = "water-permit-mcp"
