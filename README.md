# ChefMind - 大模型 Agent 开发学习项目
本文档由大模型生成，仅供参考。
基于 LangChain/LangGraph 的个人学习项目。项目实现了一个名为"中华小当家"的智能食谱推荐 Agent，集成了 RAG、MCP、Tool、Agent、中间件、向量数据库等核心功能。本项目是 AI 学习项目，仅供个人学习使用。

## 项目特点

- 🤖 **Agent 架构**: 基于 LangGraph 构建的 Agent 系统
- 🔧 **MCP 集成**: 集成多个 MCP 服务器（食谱解析、文件系统、OCR 等）
- 🛠️ **自定义工具**: 实现用户画像管理和更新工具
- 🔄 **中间件机制**: 实现工具错误处理、消息摘要、模型回退等中间件
- 📊 **向量数据库**: 基于 InMemoryStore 的向量存储和检索
- 🔍 **RAG 能力**: 结合嵌入模型实现语义检索
- 💾 **上下文管理**: 支持长期记忆和用户画像存储

## 技术栈

- **框架**: LangChain, LangGraph
- **模型**: DeepSeek Chat (主模型), HuggingFace Qwen (回退模型)
- **嵌入模型**: sentence-transformers/distiluse-base-multilingual-cased-v2
- **存储**: InMemorySaver, InMemoryStore
- **MCP**: langchain_mcp_adapters

## 核心功能模块

### Agent (`src/agent.py`)
- 创建基于 LangGraph 的 Agent
- 集成系统提示词和工具链
- 配置检查点和向量存储

### 工具 (`tools/tool.py`)
- `get_user_info`: 获取用户画像
- `update_user_info`: 更新用户偏好（食材、菜系、口味、过敏原等）

### 中间件 (`middleware/custom_middleware.py`)
- `CustomToolErrorMiddleware`: 自定义工具错误处理
- `SummarizationMiddleware`: 消息摘要中间件
- `ModelFallbackMiddleware`: 模型回退中间件

### 上下文管理 (`context.py`)
- `Context`: 用户上下文信息
- `UserInfo`: 用户画像数据模型

### MCP 服务器（自定义MCP Server见其他仓库）
- `chef_ocr`: 基于 deepseek_ocr 的 OCR MCP服务
- `filesystem`: MCP官方的文件系统MCP
- `redbook_recipe`: 小红书食谱解析MCP服务
- `cooklikehoc`: 老乡鸡食谱推荐MCP服务
- `xcf_recipe`: 下厨房食谱推荐MCP服务

## 快速开始

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
# 在 .env 文件中配置必要的 API 密钥和端点
```

3. 运行项目
```bash
python main.py
```

4. 使用说明
- 输入查询内容，Agent 会根据用户偏好推荐食谱
- 输入 `exit` 退出程序

## 项目结构

```
chefmind/
├── main.py              # 主程序入口
├── context.py           # 上下文定义
├── src/
│   └── agent.py        # Agent 核心实现
├── tools/
│   └── tool.py         # 自定义工具
├── middleware/
│   └── custom_middleware.py  # 自定义中间件
├── data/
│   └── recipes/        # 食谱数据
```

## 学习要点

本项目涵盖了以下大模型 Agent 开发的核心技术：

1. **Agent 设计与实现**: 使用 LangGraph 构建可复用的 Agent
2. **工具调用机制**: 自定义工具和 MCP 工具集成
3. **中间件开发**: 错误处理、摘要、回退等中间件实现
4. **RAG 实现**: 向量存储、嵌入和语义检索
5. **上下文管理**: 长期记忆和用户状态管理
6. **模型集成**: 多模型支持和回退机制

## 注意事项

- 本项目为学习项目，主要用于技术学习和求职展示
- 部分 MCP 服务器需要单独部署和配置
- 向量存储使用内存存储，适合开发和测试场景

## License

详见 [LICENSE.md](LICENSE.md)

