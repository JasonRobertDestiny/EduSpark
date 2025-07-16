#!/bin/bash

# EduSpark 项目启动脚本
echo "=== EduSpark 智能教育平台启动脚本 ==="

# 检查是否已安装MySQL
echo "检查MySQL安装..."
if command -v mysql &> /dev/null; then
    echo "✓ MySQL已安装"
else
    echo "❌ MySQL未安装，请先安装MySQL 8.0+"
    exit 1
fi

# 检查是否已安装Redis
echo "检查Redis安装..."
if command -v redis-server &> /dev/null; then
    echo "✓ Redis已安装"
else
    echo "❌ Redis未安装，请先安装Redis"
    exit 1
fi

# 检查是否已安装Node.js
echo "检查Node.js安装..."
if command -v node &> /dev/null; then
    echo "✓ Node.js已安装"
else
    echo "❌ Node.js未安装，请先安装Node.js"
    exit 1
fi

# 检查是否已安装Python
echo "检查Python安装..."
if command -v python &> /dev/null; then
    echo "✓ Python已安装"
else
    echo "❌ Python未安装，请先安装Python 3.8+"
    exit 1
fi

echo ""
echo "=== 配置数据库 ==="

# 创建数据库
echo "创建数据库..."
mysql -u root -p222444666888 < backend/database_setup.sql
if [ $? -eq 0 ]; then
    echo "✓ 数据库创建成功"
else
    echo "❌ 数据库创建失败"
    exit 1
fi

echo ""
echo "=== 启动后端服务 ==="

# 进入后端目录
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 启动Redis服务
echo "启动Redis服务..."
redis-server --daemonize yes

# 启动后端服务
echo "启动FastAPI后端服务..."
python simple_app.py &
BACKEND_PID=$!

echo "后端服务启动成功，PID: $BACKEND_PID"
echo "后端地址: http://localhost:8001"
echo "健康检查: http://localhost:8001/health"

# 回到项目根目录
cd ..

echo ""
echo "=== 启动前端服务 ==="

# 进入前端目录
cd front

# 安装前端依赖
echo "安装前端依赖..."
npm install

# 启动前端服务
echo "启动Vue.js前端服务..."
npm run dev &
FRONTEND_PID=$!

echo "前端服务启动成功，PID: $FRONTEND_PID"
echo "前端地址: http://localhost:5173"

echo ""
echo "=== 启动完成 ==="
echo "后端服务: http://localhost:8001"
echo "前端服务: http://localhost:5173"
echo "健康检查: http://localhost:8001/health"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户停止服务
wait
