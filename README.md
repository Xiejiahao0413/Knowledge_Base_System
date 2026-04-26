# Knowledge Base System

一个基于 Streamlit、FastAPI、LangChain 和 Chroma 的轻量级知识库问答系统。项目已经从“单文件脚本组合”重构为分层架构，保留了原有的知识入库、RAG 检索问答和会话历史能力，同时补上了配置治理、API 接口、日志、测试和部署骨架。


`new.text` 已经具备企业级开发的正确方向，但它本身还只是“企业级骨架”，并不等同于企业级落地。它的优点是：

- 明确了 `config / core / rag / services / api / web / tests` 的分层思路
- 已经从脚本式开发转向模块化、可维护架构
- 预留了测试、部署、文档、依赖分层这些企业项目常见要素

距离真正的企业级标准，还缺这些关键项：

- 配置治理：不仅要有目录，还要有统一加载、环境变量覆盖、密钥隔离
- 依赖注入：不同入口应共享同一套服务，而不是各自 new 对象
- 异常边界：上传、解码、模型调用、向量库操作需要清晰失败语义
- 接口契约：API 请求/响应模型需要稳定定义
- 可测试性：核心服务必须可脱离外部模型做单元测试
- 运维能力：日志、中间件、初始化脚本、备份、部署说明要成体系

这次重构就是在 `new.text` 的目录标准之上，把这些缺口补成一个可运行的最小企业化版本。

## 重构后的目录

```text
Knowledge_Base_System/
├── app.py
├── app_chat.py
├── app_upload.py
├── app_file_uploader.py          # 旧入口兼容
├── app_qa.py                     # 旧入口兼容
├── src/
│   ├── config/
│   ├── core/
│   ├── rag/
│   ├── services/
│   ├── api/
│   ├── models/
│   ├── utils/
│   └── web/
├── tests/
├── docs/
├── requirements/
├── scripts/
├── docker/
├── .env.example
├── pyproject.toml
└── README.md
```

## 核心改造点

### 1. 配置层统一

- 使用 `src/config/settings.py` 统一加载 `config.yaml`
- 支持通过环境变量覆盖核心配置
- 将路径、模型、RAG 参数、日志、安全配置集中管理

### 2. 业务逻辑分层

- `src/services/document_service.py`：负责文件解码、预览、上传请求构造
- `src/services/knowledge_service.py`：负责 MD5 去重、切分、写入向量库、统计
- `src/services/chat_service.py`：负责问答编排与来源返回
- `src/services/chat_history_service.py`：负责会话历史落盘

### 3. 核心能力拆分

- `src/core/embeddings.py`：嵌入模型工厂
- `src/core/llm.py`：大模型工厂
- `src/core/vector_store.py`：Chroma 向量库封装
- `src/rag/chain.py`：RAG chain 组装
- `src/rag/prompt.py`：提示词模板

### 4. 双入口能力

- Streamlit Web：`app.py`、`app_upload.py`、`app_chat.py`
- FastAPI：`src/api/app.py`

### 5. 工程治理补齐

- `tests/test_services.py`：补充服务层单元测试
- `docs/ARCHITECTURE.md`：架构说明
- `docs/API.md`：接口说明
- `docs/DEPLOY.md`：部署说明
- `scripts/init_db.py`、`scripts/backup.py`：初始化与备份脚本
- `docker/`：容器化基础文件

## 运行方式

### 1. 安装依赖

```bash
pip install -r requirements/base.txt
```

### 2. 配置环境变量

至少需要：

```bash
DASHSCOPE_API_KEY=your_key
```

可以参考 `.env.example`。

### 3. 初始化运行目录

```bash
python scripts/init_db.py
```

### 4. 启动 Streamlit

统一入口：

```bash
streamlit run app.py
```

兼容旧入口：

```bash
streamlit run app_upload.py
streamlit run app_chat.py
```

### 5. 启动 FastAPI

```bash
uvicorn src.api.app:app --reload
```

## API 概览

- `GET /health`
- `POST /api/documents/preview`
- `GET /api/knowledge/stats`
- `POST /api/knowledge/upload`
- `POST /api/chat`

## 当前这一版离“真正企业级”还差什么

这次重构已经达到“企业级开发的最小可维护标准”，但还没有到大型生产系统的完整成熟度。下一阶段建议继续补：

- 数据库级元数据管理，而不是仅依赖 `md5.text`
- 更完整的权限体系和用户体系
- 统一 observability：trace、metrics、告警
- 更强的测试体系：API 集成测试、RAG 回归测试、性能测试
- 多文档格式解析、异步任务队列、重试与熔断
- CI/CD 与镜像发布流程

