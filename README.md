# 取水许可材料智能审查系统

## 项目简介

本项目是一个基于 **Java + Python 双栈架构** 的智能审查系统，用于自动检查取水许可申请材料的合规性。系统通过 LangChain Agent 结合 MCP 协议，调用知识库（RAG）对申请材料进行形式审查、数据规范审查和实质合规审查。

## 技术架构

```
┌─────────────────────────────────────────────────┐
│                   前端 (Vue 3)                    │
│           材料列表 / 新建材料 / 材料详情            │
│             文件上传 / 审查结果展示                  │
└─────────────────┬───────────────────────────────┘
                  │ HTTP (RESTful API)
┌─────────────────▼───────────────────────────────┐
│            Java 后端 (Spring Boot 3.x)            │
│         端口 8080  │  MySQL 8.0 结构化数据         │
│    CORS 支持  │  RESTful API  │  文件管理         │
└─────────────────┬───────────────────────────────┘
                  │ HTTP
┌─────────────────▼───────────────────────────────┐
│          Python AI 服务 (FastAPI)                 │
│         端口 8000                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  LangChain Agent + MCP Server             │   │
│  │  • knowledge_search (知识库检索)           │   │
│  │  • check_completeness (完整性检查)         │   │
│  │  RAG 检索 + ChromaDB 向量数据库            │   │
│  │  OCR 非结构化文档解析                       │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## 项目结构

```
├── backend/                  # Java Spring Boot 后端
│   ├── pom.xml               # Maven 配置
│   ├── sql/schema.sql        # MySQL 数据库初始化脚本
│   └── src/main/java/com/waterpermit/
│       ├── WaterPermitApplication.java
│       ├── config/CorsConfig.java
│       ├── entity/           # 数据实体 (User, Material, ReviewRecord)
│       ├── repository/       # JPA 数据访问层
│       ├── service/          # 业务逻辑层 + AI服务客户端
│       └── controller/       # RESTful API 控制器
├── ai-service/               # Python AI 服务
│   ├── main.py               # FastAPI 主入口
│   ├── config.py             # 配置
│   ├── requirements.txt      # Python 依赖
│   └── app/
│       ├── mcp_tools/        # MCP 工具实现
│       └── services/         # RAG / 审查 / OCR 服务
├── frontend/                 # Vue 3 前端
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue
│       ├── router/index.js
│       ├── api/index.js      # Axios API 封装
│       └── views/
│           ├── MaterialList.vue    # 材料列表页
│           ├── MaterialCreate.vue  # 新建材料页（含文件上传）
│           └── MaterialDetail.vue  # 材料详情页
└── docs/                     # 项目文档
```

## 快速启动

### 1. 数据库初始化
```bash
mysql -u root -p < backend/sql/schema.sql
```

### 2. 启动 Java 后端
```bash
cd backend
mvn spring-boot:run
# 访问: http://localhost:8080
```

### 3. 启动 Python AI 服务
```bash
cd ai-service
pip install -r requirements.txt
python main.py
# 访问: http://localhost:8000/docs (Swagger UI)
```

### 4. 启动前端
```bash
cd frontend
npm install
npm run dev
# 访问: http://localhost:3000
```

## 评分节点

| 节点 | 内容 | 分值 |
|------|------|------|
| 节点一 | 项目基础架构搭建 | 15分 |
| 节点二 | 知识库与MCP Server | 30分 |
| 节点三 | Agent与系统集成 | 35分 |
| 节点四 | 项目答辩与展示 | 20分 |

## 团队分工

| 模块 | 负责人 | 说明 |
|------|--------|------|
| Java 后端 | 待分配 | Spring Boot + MySQL |
| 前端页面 | 待分配 | Vue 3 + Vite |
| Python AI 服务 | 待分配 | FastAPI + LangChain + ChromaDB |
| 文档与测试 | 待分配 | README + API文档 + 测试 |
