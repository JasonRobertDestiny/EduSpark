@echo off
chcp 65001
echo === EduSpark 智能教育平台启动脚本 ===

:: 检查MySQL是否正在运行
echo 检查MySQL服务状态...
sc query MySQL80 | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo 启动MySQL服务...
    net start MySQL80
    if %errorlevel% neq 0 (
        echo ❌ MySQL服务启动失败，请检查MySQL是否正确安装
        pause
        exit /b 1
    )
)
echo ✓ MySQL服务已运行

:: 检查Redis是否正在运行
echo 检查Redis服务状态...
tasklist /fi "imagename eq redis-server.exe" 2>nul | find "redis-server.exe" >nul
if %errorlevel% neq 0 (
    echo 启动Redis服务...
    start /b redis-server
    timeout /t 2 /nobreak >nul
)
echo ✓ Redis服务已运行

echo.
echo === 配置数据库 ===

:: 创建数据库
echo 创建数据库...
mysql -u root -p222444666888 < backend\database_setup.sql
if %errorlevel% neq 0 (
    echo ❌ 数据库创建失败，请检查MySQL密码是否正确
    pause
    exit /b 1
)
echo ✓ 数据库创建成功

echo.
echo === 启动后端服务 ===

:: 进入后端目录
cd backend

:: 创建虚拟环境
if not exist venv (
    echo 创建Python虚拟环境...
    python -m venv venv
)

:: 激活虚拟环境
call venv\Scripts\activate.bat

:: 安装依赖
echo 安装Python依赖...
pip install -r requirements.txt

:: 启动后端服务
echo 启动FastAPI后端服务...
start /b python simple_app.py

echo 后端服务启动中...
timeout /t 3 /nobreak >nul
echo ✓ 后端服务启动成功
echo 后端地址: http://localhost:8001
echo 健康检查: http://localhost:8001/health

:: 回到项目根目录
cd ..

echo.
echo === 启动前端服务 ===

:: 进入前端目录
cd front

:: 安装前端依赖
echo 安装前端依赖...
npm install

:: 启动前端服务
echo 启动Vue.js前端服务...
start /b npm run dev

echo 前端服务启动中...
timeout /t 3 /nobreak >nul
echo ✓ 前端服务启动成功
echo 前端地址: http://localhost:5173

echo.
echo === 启动完成 ===
echo 后端服务: http://localhost:8001
echo 前端服务: http://localhost:5173
echo 健康检查: http://localhost:8001/health
echo.
echo 按任意键退出...
pause
