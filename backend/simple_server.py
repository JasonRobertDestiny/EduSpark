from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# 简化的数据模型
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    full_name: Optional[str] = None

# 内存存储（仅用于测试）
users_db = {}
user_id_counter = 1

# 创建 FastAPI 应用
app = FastAPI(
    title="EduSpark Backend - 简化版",
    version="1.0.0",
    description="智能教育管理平台后端API - 测试版本"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路径
@app.get("/")
async def root():
    return {
        "message": "欢迎使用 EduSpark 智能教育管理平台 API",
        "version": "1.0.0",
        "status": "运行中",
        "docs": "/docs"
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "memory"}

# 用户注册
@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    global user_id_counter
    
    # 检查用户名是否已存在
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 创建用户
    user_data = {
        "id": user_id_counter,
        "username": user.username,
        "password": user.password,  # 实际项目中应该加密
        "role": user.role,
        "email": user.email,
        "full_name": user.full_name
    }
    
    users_db[user.username] = user_data
    user_id_counter += 1
    
    return UserResponse(
        id=user_data["id"],
        username=user_data["username"],
        role=user_data["role"],
        full_name=user_data["full_name"]
    )

# 用户登录
@app.post("/api/auth/login")
async def login(login_data: LoginRequest):
    # 查找用户
    if login_data.username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    user = users_db[login_data.username]
    
    # 验证密码
    if user["password"] != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # 验证角色
    if user["role"] != login_data.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid role for this user"
        )
    
    return {
        "access_token": f"fake_token_{user['id']}",
        "token_type": "bearer",
        "user": UserResponse(
            id=user["id"],
            username=user["username"],
            role=user["role"],
            full_name=user["full_name"]
        )
    }

# 获取用户信息
@app.get("/api/auth/me")
async def get_current_user():
    return {"message": "This endpoint requires authentication"}

# 生成考试 - 简化版
@app.post("/api/exam/generate")
async def generate_exam(exam_config: dict):
    return {
        "success": True,
        "exam_id": 1,
        "exam_data": {
            "title": exam_config.get("title", "测试试卷"),
            "instructions": "请仔细阅读题目，选择正确答案。",
            "questions": [
                {
                    "id": 1,
                    "type": "single_choice",
                    "question": "这是一道示例题目",
                    "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
                    "answer": "A",
                    "points": 2,
                    "explanation": "这是答案解析"
                }
            ]
        }
    }

# 获取用户列表 - 测试用
@app.get("/api/users")
async def get_users():
    return {
        "users": [
            {
                "id": user_data["id"],
                "username": user_data["username"],
                "role": user_data["role"],
                "full_name": user_data["full_name"]
            }
            for user_data in users_db.values()
        ],
        "total": len(users_db)
    }

if __name__ == "__main__":
    print("启动 EduSpark 后端服务...")
    print("API文档地址: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
