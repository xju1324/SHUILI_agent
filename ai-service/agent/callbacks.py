"""Agent 回调 — 等价于参考项目的中间件日志功能"""
from typing import Any, Dict, List
from langchain_core.callbacks.base import BaseCallbackHandler

from utils.logger import get_logger

logger = get_logger("agent")


class LoggingCallbackHandler(BaseCallbackHandler):
    """记录工具调用和模型调用的日志"""

    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        tool_name = serialized.get("name", "?")
        logger.info(f"[Tool] 开始: {tool_name}")
        logger.debug(f"[Tool] {tool_name} 参数: {input_str[:300]}")

    async def on_tool_end(self, output: str, **kwargs: Any) -> None:
        preview = str(output)[:200].replace("\n", " ")
        logger.info(f"[Tool] 完成 -> {preview}")

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        logger.info(f"[Model] 调用模型，提示词数: {len(prompts)}")
