# EduSpark 智能教育平台

## 项目简介
EduSpark是一个基于FastAPI + Vue.js的智能教育管理平台，集成了AI功能，提供完整的教学管理解决方案。

## 技术栈
- **后端**: FastAPI + MySQL + Redis + JWT
- **前端**: Vue.js 3 + Vite + Vue Router
- **AI集成**: OpenAI API
- **部署**: Docker

## 快速启动

### 1. 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Redis

### 2. 数据库配置
确保MySQL服务运行，用户名：root，密码：222444666888

### 3. 启动项目
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### 4. 访问地址
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 功能特性

### 教师端
- 📚 课程管理
- 📝 教学大纲制定
- 📊 智能考试生成
- 📋 作业管理
- 🎨 AI PPT生成
- 📈 学习分析
- 💬 智能问答助手

### 学生端
- 📖 课程学习
- 📝 考试答题
- 📋 作业提交
- 💬 社区交流
- 🤖 AI学习助手
- 📊 学习分析

## 项目结构
```
EduSpark2/
├── backend/           # 后端API服务
│   ├── app/
│   │   ├── api/       # API路由
│   │   ├── core/      # 核心配置
│   │   ├── models/    # 数据模型
│   │   └── schemas/   # 数据模式
│   ├── requirements.txt
│   └── database_setup.sql
├── front/             # 前端Vue应用
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   └── router/
│   └── package.json
├── start.bat          # Windows启动脚本
├── start.sh           # Linux/Mac启动脚本
└── QUICK_START.md     # 详细启动指南
```

## 开发团队
- 后端开发: FastAPI + MySQL + Redis
- 前端开发: Vue.js 3 + 现代化UI
- AI集成: OpenAI GPT模型
- 部署运维: Docker容器化
