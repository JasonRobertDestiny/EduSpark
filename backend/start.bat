@echo off
echo 正在启动 EduSpark 后端服务...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Python未安装或不在PATH中
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中
python -c "import sys; print('虚拟环境:', hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))"

REM 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

REM 创建上传目录
if not exist "uploads" mkdir uploads

echo.
echo 后端服务将在 http://localhost:8000 启动
echo API文档地址: http://localhost:8000/docs
echo.

REM 启动应用
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
