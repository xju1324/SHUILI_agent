"""涉水审批智能审查 Agent — create_react_agent + 回调日志"""
import json
from typing import AsyncGenerator

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from model.factory import create_llm
from utils.prompt_loader import load_system_prompt
from utils.logger import get_logger
from agent.tools import knowledge_search, check_completeness
from agent.callbacks import LoggingCallbackHandler
from config import MAX_ITERATIONS, VERBOSE

logger = get_logger("review_agent")


class WaterReviewAgent:
    """涉水审批材料智能审查 Agent"""

    def __init__(self):
        self.llm = create_llm()
        system_prompt = load_system_prompt()
        self.tools = [knowledge_search, check_completeness]
        self.callbacks = [LoggingCallbackHandler()]

        prompt = PromptTemplate.from_template(system_prompt)
        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=prompt)
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=VERBOSE,
            handle_parsing_errors=True,
            max_iterations=MAX_ITERATIONS,
        )

    async def execute_review(self, material_data: dict) -> str:
        """执行审查，返回完整审查报告文本"""
        input_text = json.dumps(material_data, ensure_ascii=False, indent=2)
        result = await self.executor.ainvoke(
            {"input": input_text},
            config={"callbacks": self.callbacks},
        )
        return result.get("output", "审查未能完成")

    async def execute_stream(self, material_data: dict) -> AsyncGenerator[str, None]:
        """流式执行审查，逐 token 产出内容"""
        input_text = json.dumps(material_data, ensure_ascii=False, indent=2)
        async for event in self.executor.astream_events(
            {"input": input_text},
            config={"callbacks": self.callbacks},
            version="v2",
        ):
            kind = event.get("event")
            if kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    yield chunk.content
