from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import User
from app.api.dependencies import get_current_user
import json

router = APIRouter()

@router.get("/", response_model=dict)
async def get_learning_analysis(
    subject: Optional[str] = None,
    timeframe: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学情分析数据"""
    try:
        # 这里应该根据实际的学习数据进行分析
        # 现在返回模拟数据
        
        analysis_data = {
            "user_id": current_user.id,
            "username": current_user.username,
            "subject": subject or "all",
            "timeframe": timeframe or "month",
            "overall_score": 85.5,
            "progress": {
                "completed_tasks": 45,
                "total_tasks": 60,
                "completion_rate": 75.0
            },
            "performance_by_subject": [
                {"subject": "数学", "score": 88, "improvement": 5},
                {"subject": "语文", "score": 82, "improvement": -2},
                {"subject": "英语", "score": 90, "improvement": 8},
                {"subject": "物理", "score": 85, "improvement": 3}
            ],
            "recent_activities": [
                {
                    "date": "2024-01-15",
                    "activity": "完成数学作业",
                    "score": 92,
                    "duration": 45
                },
                {
                    "date": "2024-01-14",
                    "activity": "参加英语测试",
                    "score": 88,
                    "duration": 60
                }
            ],
            "learning_patterns": {
                "most_active_time": "19:00-21:00",
                "preferred_subjects": ["英语", "数学"],
                "average_study_duration": 120,
                "weekly_study_hours": [2, 3, 2.5, 3, 2, 1, 1.5]
            },
            "recommendations": [
                "建议增加语文学习时间",
                "保持数学学习的良好状态",
                "可以尝试更多的英语阅读练习"
            ]
        }
        
        return analysis_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学情分析失败: {str(e)}"
        )

@router.get("/trends", response_model=List[dict])
async def get_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取热门话题"""
    try:
        # 模拟热门话题数据
        trends = [
            {
                "id": 1,
                "title": "人工智能在教育中的应用",
                "category": "科技",
                "posts_count": 125,
                "trend_score": 95
            },
            {
                "id": 2,
                "title": "在线学习最佳实践",
                "category": "教育",
                "posts_count": 89,
                "trend_score": 87
            },
            {
                "id": 3,
                "title": "编程学习资源分享",
                "category": "技术",
                "posts_count": 156,
                "trend_score": 92
            }
        ]
        
        return trends
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取热门话题失败: {str(e)}"
        )
