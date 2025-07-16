from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import redis

# 数据库引擎
engine = create_engine(settings.DATABASE_URL)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型类
Base = declarative_base()

# Redis 连接
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis 依赖
def get_redis():
    return redis_client
