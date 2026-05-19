import os
from utils.logger import get_logger

logger = get_logger("prompt_loader")

_PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")


def _read_text(filename: str) -> str:
    filepath = os.path.join(_PROMPTS_DIR, filename)
    if not os.path.exists(filepath):
        logger.warning(f"提示词文件不存在: {filepath}")
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_system_prompt() -> str:
    """加载审查系统提示词"""
    return _read_text("review_system.txt")
