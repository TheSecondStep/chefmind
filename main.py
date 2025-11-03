"""
中华小当家（chefgod）CLI交互主程序
"""

import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

from context import Context
from src.agent import ChefGodAgent


async def main():
    """
    中华小当家（chefgod） main函数
    """

    load_dotenv()
    tools = []

    try:
        mcp_client = MultiServerMCPClient(
            {
                "chef_ocr": {
                    "transport": "streamable_http",
                    "url": "http://localhost:8000/mcp",
                },
                "filesystem": {
                    "transport": "stdio",
                    "command": "npx",
                    "args": [
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        "D:/program/local_llm_models/deepseek/image_input",
                        "D:/program/Python/AI/cursor/chefmind/data/recipes"
                    ]
                },
                "redbook_recipe": {
                    "transport": "streamable_http",
                    "url": "http://localhost:8001/mcp",
                },
                "cooklikehoc": {
                    "transport": "stdio",
                    "command": "node",
                    "args": [
                        "D:/program/Python/AI/CookLikeHOC/mcp/server.js",
                    ]
                },
                "xcf_recipe": {
                    "transport": "streamable_http",
                    "url": "http://localhost:8002/mcp",
                }
            }
        )

        tools = await mcp_client.get_tools()
    except Exception:
        print("Warning：连接MCP服务器失败")

    agent = ChefGodAgent(mcp_tools=tools)
    config = {"configurable": {"thread_id": "1"}}

    while True:
        user_input = input("请输入：")
        if user_input == "exit":
            break

        result = agent.agent.astream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            context=Context(user_id="1"),
            stream_mode="messages"
        )

        async for token, metadata in result:
            if token.content:
                print(token.content, end="")
                if metadata['langgraph_node'] == "tools":
                    print()
        print()

asyncio.run(main())
