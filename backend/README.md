# EduSpark Backend

智能教育管理平台后端API服务

## 技术栈

- **FastAPI**: 现代高性能的Python Web框架
- **PostgreSQL**: 关系型数据库
- **Redis**: 缓存和会话存储
- **SQLAlchemy**: ORM框架
- **JWT**: 身份认证
- **Docker**: 容器化部署

## 功能模块

### 1. 用户认证系统
- 用户注册/登录
- JWT token认证
- 角色权限管理（教师/学生）

### 2. 教师功能
- 智能课程管理
- 教学大纲管理
- 智能PPT生成
- 智能试卷生成
- 智能作业生成
- 教学资源管理
- 学情分析

### 3. 学生功能
- 智能辅助做题（LeetCode集成）
- 个人学情分析
- 社区空间

### 4. 通用功能
- 文件上传/下载/管理
- 多模态问答系统
- 数据分析和可视化

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd EduSpark2/backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并配置相关参数：

```bash
cp .env.example .env
```

### 3. 数据库设置

```bash
# 启动PostgreSQL和Redis (使用Docker)
docker-compose up -d postgres redis

# 或手动安装并启动PostgreSQL和Redis
```

### 4. 运行应用

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用Docker
docker-compose up -d
```

### 5. 访问API文档

打开浏览器访问：
- API文档: http://localhost:8000/docs
- 备选文档: http://localhost:8000/redoc

## API端点

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 课程管理
- `GET /api/courses/` - 获取课程列表
- `POST /api/courses/` - 创建课程
- `GET /api/courses/{id}` - 获取课程详情
- `PUT /api/courses/{id}` - 更新课程
- `DELETE /api/courses/{id}` - 删除课程

### 考试管理
- `POST /api/exam/generate` - 生成智能试卷
- `GET /api/exam/` - 获取考试列表
- `GET /api/exam/{id}` - 获取考试详情

### 作业管理
- `POST /api/homework/generate` - 生成智能作业
- `GET /api/homework/` - 获取作业列表
- `GET /api/homework/{id}` - 获取作业详情

### PPT生成
- `POST /api/ppt/generate` - 生成智能PPT
- `GET /api/ppt/` - 获取PPT列表
- `GET /api/ppt/{id}` - 获取PPT详情

### 问答系统
- `POST /api/qa/multimodal` - 多模态问答
- `POST /api/qa/` - 简单问答
- `GET /api/qa/history` - 问答历史

### 文件管理
- `POST /api/files/upload` - 上传文件
- `GET /api/files/` - 获取文件列表
- `GET /api/files/{id}` - 获取文件详情
- `DELETE /api/files/{id}` - 删除文件

### 社区功能
- `POST /api/posts/` - 创建帖子
- `GET /api/posts/` - 获取帖子列表
- `POST /api/posts/{id}/like` - 点赞帖子

### 学情分析
- `GET /api/learning-analysis/` - 获取学情分析
- `GET /api/learning-analysis/trends` - 获取热门话题

### LeetCode集成
- `GET /api/leetcode/problems` - 搜索题目
- `GET /api/leetcode/problems/{id}` - 获取题目详情
- `POST /api/leetcode/hint` - 获取AI提示
- `POST /api/leetcode/run` - 运行代码
- `POST /api/leetcode/submit` - 提交代码

## 开发指南

### 项目结构
```
backend/
├── app/
│   ├── api/              # API路由
│   ├── core/             # 核心配置
│   ├── models/           # 数据模型
│   ├── schemas/          # Pydantic模型
│   └── main.py           # 应用入口
├── requirements.txt      # 依赖文件
├── Dockerfile           # Docker配置
├── docker-compose.yml   # Docker编排
└── .env                 # 环境变量
```

### 添加新功能

1. 在 `app/models/` 中定义数据模型
2. 在 `app/schemas/` 中定义Pydantic模型
3. 在 `app/api/` 中创建API路由
4. 在 `app/main.py` 中注册路由

### 数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head
```

## 部署

### Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

### 生产部署

1. 修改 `.env` 文件中的生产配置
2. 设置 `DEBUG=False`
3. 配置反向代理（Nginx）
4. 使用进程管理器（PM2, Supervisor）

## 测试

```bash
# 运行测试
pytest

# 运行特定测试
pytest tests/test_auth.py
```

## 注意事项

1. 确保在生产环境中更改 `SECRET_KEY`
2. 配置AI服务的API密钥
3. 设置适当的文件上传限制
4. 定期备份数据库
5. 监控应用性能和错误日志

## 许可证

MIT License
