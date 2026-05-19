"""
RAG 知识库服务 — LangChain + ChromaDB
支持本地模型 (HuggingFace) 和外部 API (OpenAI 兼容) 两种 Embedding 模式
覆盖: 文档解析 + 文本分块 + 向量化存储 + 检索 + MD5 去重
"""
import os
from typing import List, Dict, Optional

from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import (
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    KNOWLEDGE_DIR,
    MD5_STORE_FILE,
    ALLOWED_FILE_TYPES,
)
from model.factory import create_embeddings
from utils.file_handler import (
    get_file_md5_hex,
    listdir_with_allowed_type,
    pdf_loader,
    txt_loader,
)
from utils.logger import get_logger

logger = get_logger("rag_service")


class RAGService:
    """涉水审批知识库 RAG 服务（Embedding 延迟初始化）"""

    def __init__(self):
        self._embeddings = None
        self.vector_store: Optional[Chroma] = None
        self._init_vector_store()

    def _ensure_embeddings(self):
        """延迟创建 Embedding 实例（避免启动时就下载模型/校验 API key）"""
        if self._embeddings is None:
            self._embeddings = create_embeddings()
        return self._embeddings

    def _init_vector_store(self):
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        if os.path.exists(CHROMA_PERSIST_DIR) and os.listdir(CHROMA_PERSIST_DIR):
            self.vector_store = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=self._ensure_embeddings(),
                collection_name=CHROMA_COLLECTION_NAME,
            )

    def _check_md5_hex(self, md5_hex: str) -> bool:
        """检查 MD5 是否已入库"""
        if not os.path.exists(MD5_STORE_FILE):
            return False
        with open(MD5_STORE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == md5_hex:
                    return True
        return False

    def _save_md5_hex(self, md5_hex: str):
        """记录 MD5 到去重文件"""
        with open(MD5_STORE_FILE, "a", encoding="utf-8") as f:
            f.write(md5_hex + "\n")

    def _load_file_documents(self, filepath: str) -> list:
        """根据文件类型加载文档"""
        if filepath.endswith(".pdf"):
            return pdf_loader(filepath)
        elif filepath.endswith(".docx"):
            return Docx2txtLoader(filepath).load()
        elif filepath.endswith((".txt", ".md")):
            return txt_loader(filepath)
        return []

    def load_documents(self, doc_dir: str = None) -> int:
        """从目录加载文档，分块后向量化存入 ChromaDB（MD5 去重）"""
        if doc_dir is None:
            doc_dir = KNOWLEDGE_DIR

        if not os.path.exists(doc_dir):
            logger.warning(f"知识库目录不存在: {doc_dir}")
            return 0

        allowed_files = listdir_with_allowed_type(doc_dir, ALLOWED_FILE_TYPES)
        if not allowed_files:
            logger.info(f"知识库目录 {doc_dir} 中无合法文件")
            return 0

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "；", "，", " ", ""],
        )

        total_chunks = 0
        for filepath in allowed_files:
            filename = os.path.basename(filepath)

            md5_hex = get_file_md5_hex(filepath)
            if self._check_md5_hex(md5_hex):
                logger.info(f"[知识库] {filename} MD5 已存在，跳过")
                continue

            try:
                documents = self._load_file_documents(filepath)
                if not documents:
                    logger.warning(f"[知识库] {filename} 内无有效文本，跳过")
                    continue

                for doc in documents:
                    doc.metadata["source"] = filename

                chunks = text_splitter.split_documents(documents)
                if not chunks:
                    logger.warning(f"[知识库] {filename} 分块后无内容，跳过")
                    continue

                if self.vector_store is None:
                    self.vector_store = Chroma.from_documents(
                        documents=chunks,
                        embedding=self._ensure_embeddings(),
                        persist_directory=CHROMA_PERSIST_DIR,
                        collection_name=CHROMA_COLLECTION_NAME,
                    )
                else:
                    self.vector_store.add_documents(chunks)

                self._save_md5_hex(md5_hex)
                total_chunks += len(chunks)
                logger.info(f"[知识库] {filename} 加载成功 ({len(chunks)} chunks)")

            except Exception as e:
                logger.error(f"[知识库] {filename} 加载失败: {e}")

        return total_chunks

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """语义检索，返回: 内容 + 来源 + 相似度分数"""
        if self.vector_store is None:
            return []

        results = self.vector_store.similarity_search_with_score(query, k=k)

        return [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", None),
                "score": round(float(score), 4),
            }
            for doc, score in results
        ]

    def get_document_count(self) -> int:
        if self.vector_store is None:
            return 0
        return self.vector_store._collection.count()

    def is_ready(self) -> bool:
        return self.vector_store is not None
