"""
中华小当家Agent类
"""
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelFallbackMiddleware,
    SummarizationMiddleware,
)
from langchain.embeddings import init_embeddings
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain_huggingface.llms import HuggingFaceEndpoint
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from mcp.types import Tool

from context import Context
from middleware.custom_middleware import CustomToolErrorMiddleware
from tools.tool import get_user_info, update_user_info


class ChefGodAgent:
    """
    中华小当家Agent类
    """

    def __init__(self, mcp_tools: list[Tool]):
        self.mcptools = mcp_tools
        self.tools = [update_user_info, get_user_info]
        self.system_prompt = self._get_system_prompt()
        self.model = ChatDeepSeek(model="deepseek-chat", temperature=0.2,
                                  max_tokens=512, timeout=20)
        self.checkpointer = InMemorySaver()
        self.store = InMemoryStore(index={
            "dims": 512,
            "embed": init_embeddings("huggingface:sentence-transformers/distiluse-base-multilingual-cased-v2")
        })
        # 回退模型：HuggingFace Inference 端点
        self.fallback_model = ChatHuggingFace(
            llm=HuggingFaceEndpoint(
                repo_id="Qwen/Qwen3-32B",
                task="text-generation",
                temperature=0.2,
                max_new_tokens=512
            )
        )
        self.agent = create_agent(
            model=self.model,
            tools=self.tools + self.mcptools,
            system_prompt=self.system_prompt,
            checkpointer=self.checkpointer,
            store=self.store,
            context_schema=Context,
            middleware=[
                SummarizationMiddleware(
                    model=self.model,
                    max_tokens_before_summary=2048,
                    messages_to_keep=20,
                    summary_prompt="总结对话内容，重点记忆与食品、食谱、用户口味偏好等相关的信息。"
                ),
                ModelFallbackMiddleware(self.fallback_model),
                CustomToolErrorMiddleware(),
            ]
        )

    def _get_system_prompt(self) -> str:
        """
        获取系统提示词
        """

        return """
        你是中华小当家，了解各种食材和烹饪技巧。

        规则：
        1、当用户输入中包含以下标签时，你需要执行对应动作：
        - @本地食谱：根据用户输入和当前食材，查找data/recipes目录下的食谱文件，推荐食谱。
        - @解析小红书食谱：根据小红书链接，解析食谱, 并根据菜名作为文件名，保存到data/recipes目录下， 如果文件已存在，则更新文件。
        - @CookLikeHOC：根据用户输入和当前食材，推荐相关的老乡鸡食谱。
        - @下厨房食谱：根据用户输入和当前食材，搜索下厨房食谱数据集并推荐。
        - @解析食材：解析本地路径下的食材|购物小票图片，识别食材名称、生产日期、保质期。
        2、$$确保$$当用户输入中涉及食物、口味、烹饪习惯、过敏食物、菜系等用户偏好时，你需要先调用@get_user_info工具获取用户偏好，结合用户输入，再调用@update_user_info工具更新用户偏好。
        3、推荐食谱强依赖用户偏好，不要推荐用户不喜欢的食材、口味、菜系等，除非用户明确说明可以推荐。

        请保持热情和耐心，与用户进行互动，直到用户满意为止。
        """
