from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="EduSpark API",
    description="智能教育平台后端API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EduSpark API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "服务运行正常"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
