"""AI服务全局配置"""

import os
from dotenv import load_dotenv

# 加载 .env 文件（优先级低于系统环境变量）
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# HuggingFace 镜像（国内加速）
os.environ.setdefault("HF_ENDPOINT", os.getenv("HF_ENDPOINT", "https://hf-mirror.com"))
os.environ.setdefault('HF_HUB_OFFLINE', os.getenv('HF_HUB_OFFLINE', '0'))

# 服务配置
HOST = os.getenv("AI_HOST", "0.0.0.0")
PORT = int(os.getenv("AI_PORT", "8000"))

# ChromaDB 配置
CHROMA_PERSIST_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "water_regulations")
CHROMA_K = int(os.getenv("CHROMA_K", "5"))

# 文档分块
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# MD5 去重存储文件
MD5_STORE_FILE = os.getenv("MD5_STORE_FILE", "./md5_hex.store")

# 允许入库的文件类型
ALLOWED_FILE_TYPES = (".pdf", ".docx", ".txt", ".md")

# Agent 配置
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))
VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"

# ============================================================
# Embedding 配置（支持 local / api 两种模式）
# ============================================================
EMBEDDING_MODE = os.getenv("EMBEDDING_MODE", "local")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")
EMBEDDING_API_BASE = os.getenv("EMBEDDING_API_BASE", "https://ark.cn-beijing.volces.com/api/coding/v3")
EMBEDDING_API_MODEL = os.getenv("EMBEDDING_API_MODEL", "BAAI/bge-large-zh-v1.5")

# 知识库文档目录
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "../docs/knowledge")
AUTO_LOAD_KNOWLEDGE = os.getenv("AUTO_LOAD_KNOWLEDGE", "true").lower() == "true"

# MCP Server 名称
MCP_SERVER_NAME = "water-supervision-mcp"

# ============================================================
# LLM 配置（火山引擎 Ark / OpenAI 兼容）
# ============================================================
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://ark.cn-beijing.volces.com/api/coding/v3")
LLM_MODEL = os.getenv("LLM_MODEL", "doubao-1.5-pro-32k")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))