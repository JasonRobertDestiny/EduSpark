from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import User, Exam
from app.schemas.schemas import ExamCreate, ExamResponse, ExamUpdate
from app.api.dependencies import get_current_user, require_teacher
import json
import openai
from app.core.config import settings

router = APIRouter()

@router.post("/generate", response_model=dict)
async def generate_exam(
    exam_config: dict,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """生成智能试卷"""
    try:
        # 从前端获取的配置
        title = exam_config.get("title", "")
        subject = exam_config.get("subject", "")
        grade = exam_config.get("grade", "")
        duration = exam_config.get("duration", 60)
        knowledge_points = exam_config.get("knowledgePoints", "")
        question_types = exam_config.get("questionTypes", [])
        
        # 构建AI提示
        prompt = f"""
        请为以下条件生成一份考试试卷：
        
        试卷标题：{title}
        学科：{subject}
        年级：{grade}
        考试时长：{duration}分钟
        知识点范围：{knowledge_points}
        
        题型要求：
        """
        
        # 处理题型配置
        total_questions = 0
        for q_type in question_types:
            if q_type.get("enabled", False):
                count = q_type.get("count", 0)
                points = q_type.get("points", 0)
                name = q_type.get("name", "")
                prompt += f"- {name}: {count}题，每题{points}分\n"
                total_questions += count
        
        prompt += f"""
        
        请按照以下JSON格式返回试卷：
        {{
            "title": "{title}",
            "instructions": "考试说明",
            "questions": [
                {{
                    "id": 1,
                    "type": "single_choice",
                    "question": "题目内容",
                    "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
                    "answer": "A",
                    "points": 2,
                    "explanation": "答案解析"
                }}
            ]
        }}
        
        请确保题目内容与{subject}学科和{grade}年级水平相符，涵盖指定的知识点范围。
        """
        
        # 调用AI生成试卷（这里需要根据你使用的AI服务调整）
        # 示例：使用OpenAI
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的教师，擅长出题和设计考试。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            
            generated_content = response.choices[0].message.content
            
            # 尝试解析AI返回的JSON
            try:
                exam_data = json.loads(generated_content)
            except json.JSONDecodeError:
                # 如果AI返回的不是标准JSON，创建一个基本结构
                exam_data = {
                    "title": title,
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
        else:
            # 没有配置AI服务时返回示例数据
            exam_data = {
                "title": title,
                "instructions": "请仔细阅读题目，选择正确答案。",
                "questions": [
                    {
                        "id": 1,
                        "type": "single_choice",
                        "question": f"这是一道{subject}的示例题目",
                        "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
                        "answer": "A",
                        "points": 2,
                        "explanation": "这是答案解析"
                    }
                ]
            }
        
        # 保存到数据库
        db_exam = Exam(
            title=title,
            subject=subject,
            grade=grade,
            duration=duration,
            creator_id=current_user.id,
            questions=json.dumps(exam_data)
        )
        
        db.add(db_exam)
        db.commit()
        db.refresh(db_exam)
        
        return {
            "success": True,
            "exam_id": db_exam.id,
            "exam_data": exam_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成试卷失败: {str(e)}"
        )

@router.get("/", response_model=List[ExamResponse])
async def get_exams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试列表"""
    exams = db.query(Exam).filter(Exam.creator_id == current_user.id).all()
    return exams

@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试详情"""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # 检查权限
    if exam.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this exam"
        )
    
    return exam

@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam(
    exam_id: int,
    exam_update: ExamUpdate,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """更新考试"""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # 检查权限
    if exam.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this exam"
        )
    
    # 更新字段
    for field, value in exam_update.dict(exclude_unset=True).items():
        setattr(exam, field, value)
    
    db.commit()
    db.refresh(exam)
    
    return exam

@router.delete("/{exam_id}")
async def delete_exam(
    exam_id: int,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """删除考试"""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # 检查权限
    if exam.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this exam"
        )
    
    db.delete(exam)
    db.commit()
    
    return {"message": "Exam deleted successfully"}
