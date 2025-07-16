# EduSpark 智能教育平台 - 快速启动指南

## 🚀 一键启动

### Windows 用户
双击运行 `start.bat` 文件，脚本将自动：
- 检查并启动MySQL服务
- 检查并启动Redis服务  
- 创建数据库和表结构
- 启动后端API服务
- 启动前端Web服务

### Mac/Linux 用户
在终端中运行：
```bash
chmod +x start.sh
./start.sh
```

## 📋 系统要求

### 必需软件
- **MySQL 8.0+** - 数据库服务器
- **Redis** - 缓存服务器
- **Node.js 16+** - 前端开发环境
- **Python 3.8+** - 后端开发环境

### 数据库配置
- 用户名：`root`
- 密码：`222444666888`
- 数据库名：`eduspark`

## 🔧 手动启动步骤

### 1. 启动必需服务
```bash
# 启动MySQL服务
net start MySQL80

# 启动Redis服务
redis-server
```

### 2. 初始化数据库
```bash
mysql -u root -p222444666888 < backend/database_setup.sql
```

### 3. 启动后端服务
```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 启动前端服务
```bash
npm install
npm run dev
```

## 🌐 服务地址

- **前端界面**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **数据库**: localhost:3306

## 👥 测试账户

系统已预置以下测试账户：

| 用户名 | 密码 | 角色 | 描述 |
|--------|------|------|------|
| admin | 123456 | teacher | 系统管理员 |
| teacher1 | 123456 | teacher | 教师账户 |
| student1 | 123456 | student | 学生账户 |

## 🎯 功能模块

### 教师端功能
- 📚 课程管理
- 📝 教学大纲制定
- 📊 考试生成
- 📋 作业布置
- 🎨 PPT生成
- 📈 学习分析
- 💬 智能问答

### 学生端功能
- 📖 课程学习
- 📝 考试答题
- 📋 作业提交
- 💬 社区交流
- 🤖 AI助手
- 📊 学习分析

## 🛠️ 技术架构

### 后端技术栈
- **FastAPI** - 高性能Web框架
- **SQLAlchemy** - ORM数据库操作
- **MySQL** - 关系型数据库
- **Redis** - 缓存和会话存储
- **JWT** - 身份认证
- **OpenAI** - AI功能集成

### 前端技术栈
- **Vue.js 3** - 现代前端框架
- **Vite** - 快速构建工具
- **Vue Router** - 路由管理
- **Axios** - HTTP客户端

## 🔍 常见问题

### 1. MySQL连接失败
- 检查MySQL服务是否启动
- 确认密码是否为 `222444666888`
- 检查端口3306是否被占用

### 2. Redis连接失败
- 检查Redis服务是否启动
- 确认端口6379是否可用

### 3. 前端页面无法访问
- 检查Node.js版本是否为16+
- 确认5173端口是否被占用
- 检查防火墙设置

### 4. API无法访问
- 检查Python虚拟环境是否激活
- 确认所有依赖是否正确安装
- 检查8000端口是否被占用

## 📞 技术支持

如遇问题请检查：
1. 所有必需软件是否正确安装
2. 数据库连接配置是否正确
3. 端口是否被其他程序占用
4. 防火墙是否阻止相关端口

## 📱 移动端支持

前端界面采用响应式设计，支持：
- 桌面端浏览器
- 平板设备
- 手机浏览器

推荐使用Chrome、Firefox、Safari等现代浏览器以获得最佳体验。
