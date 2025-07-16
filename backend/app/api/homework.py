from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import User, Homework
from app.schemas.schemas import HomeworkCreate, HomeworkResponse, HomeworkUpdate
from app.api.dependencies import get_current_user, require_teacher
import json
import openai
from app.core.config import settings

router = APIRouter()

@router.post("/generate", response_model=dict)
async def generate_homework(
    homework_config: dict,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """生成智能作业"""
    try:
        # 从前端获取的配置
        title = homework_config.get("title", "")
        subject = homework_config.get("subject", "")
        grade = homework_config.get("grade", "")
        description = homework_config.get("description", "")
        difficulty = homework_config.get("difficulty", "medium")
        question_count = homework_config.get("questionCount", 5)
        
        # 构建AI提示
        prompt = f"""
        请为以下条件生成一份作业：
        
        作业标题：{title}
        学科：{subject}
        年级：{grade}
        作业描述：{description}
        难度级别：{difficulty}
        题目数量：{question_count}
        
        请按照以下JSON格式返回作业：
        {{
            "title": "{title}",
            "description": "{description}",
            "questions": [
                {{
                    "id": 1,
                    "type": "essay",
                    "question": "题目内容",
                    "requirements": "答题要求",
                    "points": 10,
                    "reference_answer": "参考答案"
                }}
            ]
        }}
        
        请确保题目内容与{subject}学科和{grade}年级水平相符，难度适中。
        """
        
        # 调用AI生成作业
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的教师，擅长设计作业和练习题。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            generated_content = response.choices[0].message.content
            
            try:
                homework_data = json.loads(generated_content)
            except json.JSONDecodeError:
                homework_data = {
                    "title": title,
                    "description": description,
                    "questions": [
                        {
                            "id": 1,
                            "type": "essay",
                            "question": f"这是一道{subject}的示例作业题目",
                            "requirements": "请详细回答问题，字数不少于200字",
                            "points": 10,
                            "reference_answer": "这是参考答案"
                        }
                    ]
                }
        else:
            # 没有配置AI服务时返回示例数据
            homework_data = {
                "title": title,
                "description": description,
                "questions": [
                    {
                        "id": 1,
                        "type": "essay",
                        "question": f"这是一道{subject}的示例作业题目",
                        "requirements": "请详细回答问题，字数不少于200字",
                        "points": 10,
                        "reference_answer": "这是参考答案"
                    }
                ]
            }
        
        # 保存到数据库
        db_homework = Homework(
            title=title,
            description=description,
            subject=subject,
            grade=grade,
            creator_id=current_user.id,
            questions=json.dumps(homework_data)
        )
        
        db.add(db_homework)
        db.commit()
        db.refresh(db_homework)
        
        return {
            "success": True,
            "homework_id": db_homework.id,
            "homework_data": homework_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成作业失败: {str(e)}"
        )

@router.get("/", response_model=List[HomeworkResponse])
async def get_homework_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取作业列表"""
    homework_list = db.query(Homework).filter(Homework.creator_id == current_user.id).all()
    return homework_list

@router.get("/{homework_id}", response_model=HomeworkResponse)
async def get_homework(
    homework_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取作业详情"""
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Homework not found"
        )
    
    # 检查权限
    if homework.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this homework"
        )
    
    return homework
