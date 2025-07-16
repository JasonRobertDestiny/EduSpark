# 🎓 EduSpark - 智能教育平台

<div align="center">
  <img src="https://img.shields.io/badge/Vue.js-3.0-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</div>

## 📖 项目简介

EduSpark是一个基于FastAPI + Vue.js的智能教育管理平台，集成了AI功能，为教育机构提供完整的教学管理解决方案。平台支持智能内容生成、个性化学习分析、互动式教学等现代化教育功能。

## ✨ 功能特性

### 👨‍🏫 教师端功能
- 📚 **课程管理** - 创建、编辑、管理课程内容
- 📝 **教学大纲制定** - 智能生成结构化教学大纲
- 📊 **智能考试生成** - AI辅助生成各类考试题目
- 📋 **作业管理** - 布置、批改、统计作业情况
- 🎨 **AI PPT生成** - 自动生成精美教学PPT
- 📈 **学习分析** - 深度分析学生学习情况
- 💬 **智能问答助手** - AI驱动的教学问答系统

### 👨‍🎓 学生端功能
- 📖 **课程学习** - 在线学习课程内容
- 📝 **考试答题** - 参与各类在线考试
- 📋 **作业提交** - 提交和查看作业反馈
- 💬 **社区交流** - 与同学和老师互动交流
- 🤖 **AI学习助手** - 个性化学习建议和答疑
- 📊 **学习分析** - 查看个人学习进度和成绩分析

## 🏗️ 技术架构

### 后端技术栈
- **FastAPI** - 高性能异步Web框架
- **SQLAlchemy** - 现代化ORM数据库操作
- **MySQL** - 稳定可靠的关系型数据库
- **Redis** - 高性能缓存和会话存储
- **JWT** - 安全的身份认证机制
- **OpenAI API** - 先进的AI功能集成

### 前端技术栈
- **Vue.js 3** - 渐进式JavaScript框架
- **Vite** - 快速的前端构建工具
- **Vue Router** - 官方路由管理器
- **Axios** - 优雅的HTTP客户端

### 部署方案
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排
- **Nginx** - 反向代理和负载均衡

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Redis 6.0+

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/JasonRobertDestiny/EduSpark.git
cd EduSpark
```

2. **一键启动**
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

3. **访问应用**
- 前端界面: http://localhost:5173
- 后端API: http://localhost:8001
- 健康检查: http://localhost:8001/health

### 手动部署

#### 后端部署
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python simple_app.py
```

#### 前端部署
```bash
cd front
npm install
npm run dev
```

## 📁 项目结构

```
EduSpark/
├── backend/                 # 后端API服务
│   ├── app/
│   │   ├── api/            # API路由模块
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   └── schemas/        # 数据模式
│   ├── simple_app.py       # 简化版API服务
│   ├── requirements.txt    # Python依赖
│   └── database_setup.sql  # 数据库初始化脚本
├── front/                  # 前端Vue应用
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面视图
│   │   ├── router/         # 路由配置
│   │   └── services/       # API服务
│   └── package.json        # 前端依赖
├── start.bat               # Windows启动脚本
├── start.sh                # Linux/Mac启动脚本
└── README.md               # 项目文档
```

## 👥 测试账户

系统预置了以下测试账户：

| 用户名 | 密码 | 角色 | 描述 |
|--------|------|------|------|
| admin | 123456 | teacher | 系统管理员 |
| teacher1 | 123456 | teacher | 教师账户 |
| student1 | 123456 | student | 学生账户 |

## 🎯 核心功能演示

### AI智能生成
- 🧠 智能考试题目生成
- 📊 个性化学习分析报告
- 🎨 自动PPT内容生成
- 💬 智能问答系统

### 教学管理
- 📅 课程计划制定
- 📚 教学资源管理
- 📈 学习进度跟踪
- 💯 成绩统计分析

### 互动学习
- 🗣️ 在线讨论社区
- 🤝 师生互动问答
- 📱 移动端适配
- 🔔 实时消息通知

## 📊 项目状态

- ✅ 前后端分离架构
- ✅ RESTful API设计
- ✅ 响应式界面设计
- ✅ 数据库优化
- ✅ 缓存机制
- ✅ 容器化部署
- 🔄 持续集成/持续部署 (规划中)
- 🔄 微服务架构 (规划中)

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 📞 联系我们

- 项目作者: JasonRobertDestiny
- GitHub: https://github.com/JasonRobertDestiny
- 项目主页: https://github.com/JasonRobertDestiny/EduSpark

---

<div align="center">
  ⭐ 如果这个项目对你有帮助，请给我们一个星标！
</div>
