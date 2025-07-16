from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import settings
from app.core.database import engine, Base
from app.api.auth import router as auth_router
from app.api.courses import router as courses_router
from app.api.exams import router as exams_router
from app.api.homework import router as homework_router
from app.api.ppt import router as ppt_router
from app.api.qa import router as qa_router
from app.api.files import router as files_router
from app.api.analytics import router as analytics_router
from app.api.posts import router as posts_router
from app.api.syllabus import router as syllabus_router
from app.api.leetcode import router as leetcode_router

# 数据库初始化
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时清理资源
    pass

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="智能教育管理平台后端API",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(courses_router, prefix="/api/courses", tags=["课程管理"])
app.include_router(exams_router, prefix="/api/exam", tags=["考试管理"])
app.include_router(homework_router, prefix="/api/homework", tags=["作业管理"])
app.include_router(ppt_router, prefix="/api/ppt", tags=["PPT生成"])
app.include_router(qa_router, prefix="/api/qa", tags=["问答系统"])
app.include_router(files_router, prefix="/api/files", tags=["文件管理"])
app.include_router(analytics_router, prefix="/api/learning-analysis", tags=["学情分析"])
app.include_router(posts_router, prefix="/api/posts", tags=["社区动态"])
app.include_router(syllabus_router, prefix="/api/syllabus", tags=["教学大纲"])
app.include_router(leetcode_router, prefix="/api/leetcode", tags=["LeetCode集成"])

# 根路径
@app.get("/")
async def root():
    return {
        "message": "欢迎使用 EduSpark 智能教育管理平台 API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
