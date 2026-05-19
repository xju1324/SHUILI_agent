"""LLM 和 Embedding 模型工厂"""
from langchain_openai import ChatOpenAI

from config import (
    EMBEDDING_MODE,
    EMBEDDING_MODEL,
    EMBEDDING_API_KEY,
    EMBEDDING_API_BASE,
    EMBEDDING_API_MODEL,
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
)


def create_llm() -> ChatOpenAI:
    """创建 LLM 实例（火山引擎 Ark / OpenAI 兼容 API）"""
    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
    )


def create_embeddings():
    """根据 EMBEDDING_MODE 创建 Embedding 实例（local 或 api）"""
    if EMBEDDING_MODE == "api":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=EMBEDDING_API_MODEL,
            api_key=EMBEDDING_API_KEY,
            base_url=EMBEDDING_API_BASE,
            # 部分 OpenAI 兼容服务（如火山方舟 Coding Plan）不支持 token 数组输入，
            # 关闭长度检查以确保始终以字符串方式请求 embeddings。
            check_embedding_ctx_length=False,
        )
    else:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
