import os
import hashlib

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from utils.logger import get_logger

logger = get_logger("file_handler")


def get_file_md5_hex(filepath: str) -> str:
    """计算文件 MD5（4KB 分块读取）"""
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def listdir_with_allowed_type(path: str, allowed_types: tuple) -> list[str]:
    """列出目录中符合指定扩展名的文件"""
    result = []
    if not os.path.exists(path):
        return result
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path) and entry.lower().endswith(allowed_types):
            result.append(full_path)
    return result


def pdf_loader(filepath: str) -> list[Document]:
    return PyPDFLoader(filepath).load()


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()
