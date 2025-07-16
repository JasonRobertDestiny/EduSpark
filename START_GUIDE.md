# 🚀 EduSpark 智能教育管理平台 - 快速启动指南

## 项目概述
EduSpark 是一个基于 Vue.js + FastAPI 的智能教育管理平台，支持智能试卷生成、作业管理、PPT制作、学情分析等功能。

## 🏗️ 项目结构
```
EduSpark2/
├── front/              # Vue.js 前端
│   ├── src/
│   │   ├── views/      # 页面组件
│   │   ├── components/ # 通用组件
│   │   ├── router/     # 路由配置
│   │   └── services/   # API服务
│   ├── package.json
│   └── vite.config.js
├── backend/            # FastAPI 后端
│   ├── app/
│   │   ├── api/        # API路由
│   │   ├── core/       # 核心配置
│   │   ├── models/     # 数据模型
│   │   └── schemas/    # Pydantic模型
│   ├── requirements.txt
│   ├── simple_server.py # 简化版测试服务
│   └── docker-compose.yml
└── README.md
```

## 🛠️ 技术栈

### 前端
- **Vue 3** - 现代JavaScript框架
- **Vite** - 快速构建工具
- **Vue Router** - 路由管理
- **Axios** - HTTP客户端
- **ECharts** - 数据可视化

### 后端
- **FastAPI** - 高性能Python Web框架
- **SQLAlchemy** - ORM框架
- **MySQL** - 关系型数据库
- **Redis** - 缓存和会话存储
- **JWT** - 身份认证
- **Docker** - 容器化部署

## 🚀 快速启动

### 方法1：使用简化版后端（推荐用于测试）

1. **启动后端服务**
   ```bash
   cd backend
   python simple_server.py
   ```
   
2. **启动前端服务**
   ```bash
   cd front
   npm run dev
   ```

3. **访问应用**
   - 前端地址: http://localhost:5173
   - 后端API文档: http://localhost:8000/docs
   - 后端测试页面: file:///d:/VibeCoding_pgm/EduSpark2/backend/test_frontend.html

### 方法2：完整版部署

1. **环境准备**
   ```bash
   # 安装Python依赖
   cd backend
   pip install -r requirements.txt
   
   # 安装前端依赖
   cd ../front
   npm install
   ```

2. **数据库配置**
   ```bash
   # 启动MySQL和Redis
   cd ../backend
   docker-compose up -d mysql redis
   ```

3. **启动服务**
   ```bash
   # 启动后端
   uvicorn app.main:app --reload
   
   # 启动前端
   cd ../front
   npm run dev
   ```

## 🔧 配置说明

### 后端配置 (.env)
```
DATABASE_URL=mysql://root:222444666888@localhost:3306/eduspark
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

### 前端配置
API地址已配置为: `http://localhost:8000/api`

## 🎯 核心功能

### 教师功能
- ✅ 智能试卷生成 - 基于AI生成个性化试卷
- ✅ 智能作业管理 - 自动生成和批改作业
- ✅ 智能PPT制作 - 一键生成演示文稿
- ✅ 教学大纲管理 - 系统化课程规划
- ✅ 学情分析 - 数据驱动的教学优化

### 学生功能
- ✅ 智能辅助做题 - LeetCode集成练习
- ✅ 个人学情分析 - 学习进度跟踪
- ✅ 社区交流空间 - 学习经验分享
- ✅ 多模态问答 - 文本、图像、文件智能解答

### 通用功能
- ✅ 用户认证系统 - JWT安全登录
- ✅ 文件管理系统 - 上传下载管理
- ✅ 实时问答系统 - AI智能助手
- ✅ 数据可视化 - 图表展示分析

## 📊 API接口

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 智能功能
- `POST /api/exam/generate` - 生成智能试卷
- `POST /api/homework/generate` - 生成智能作业
- `POST /api/ppt/generate` - 生成智能PPT
- `POST /api/qa/multimodal` - 多模态问答

### 数据管理
- `GET /api/courses/` - 获取课程列表
- `GET /api/learning-analysis/` - 获取学情分析
- `GET /api/posts/` - 获取社区帖子
- `POST /api/files/upload` - 上传文件

## 🧪 测试功能

### 后端API测试
```bash
cd backend
python test_simple_api.py
```

### 前端界面测试
1. 访问 http://localhost:5173
2. 使用测试账号登录:
   - 用户名: testuser
   - 密码: testpass123
   - 角色: teacher

## 🔍 故障排除

### 常见问题

1. **后端服务无法启动**
   - 检查Python版本 (推荐3.9+)
   - 安装依赖: `pip install fastapi uvicorn`
   - 检查端口占用: `netstat -ano | findstr :8000`

2. **前端服务无法启动**
   - 检查Node.js版本 (推荐16+)
   - 清理缓存: `npm cache clean --force`
   - 重新安装: `rm -rf node_modules && npm install`

3. **数据库连接失败**
   - 检查MySQL服务状态
   - 验证连接字符串配置
   - 确保数据库已创建

## 📝 开发计划

### 下一步开发
- [ ] 完善AI服务集成
- [ ] 添加实时通知系统
- [ ] 优化前端UI/UX
- [ ] 添加移动端适配
- [ ] 集成更多第三方服务

### 扩展功能
- [ ] 视频会议集成
- [ ] 在线编程环境
- [ ] 成绩管理系统
- [ ] 课表管理功能
- [ ] 家校沟通平台

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add AmazingFeature'`
4. 推送到分支: `git push origin feature/AmazingFeature`
5. 提交Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件

## 📞 联系我们

如有问题或建议，请联系开发团队。

---

**🎉 恭喜！EduSpark 智能教育管理平台后端开发完成！**

现在你可以：
1. 启动后端服务测试API功能
2. 连接前端进行完整测试
3. 根据需要添加更多功能
4. 部署到生产环境
