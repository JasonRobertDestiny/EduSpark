from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import User, QASession
from app.schemas.schemas import QARequest, QAResponse
from app.api.dependencies import get_current_user
import json
import openai
from app.core.config import settings

router = APIRouter()

@router.post("/multimodal", response_model=dict)
async def multimodal_qa(
    question: str = Form(...),
    files: List[UploadFile] = File(None),
    images: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """多模态问答"""
    try:
        # 处理文件内容
        context_parts = []
        
        # 处理文本文件
        if files:
            for file in files:
                if file.filename.endswith(('.txt', '.md')):
                    content = await file.read()
                    context_parts.append(f"文件内容 ({file.filename}):\n{content.decode('utf-8')}")
                elif file.filename.endswith('.pdf'):
                    # 这里需要PDF处理库
                    context_parts.append(f"PDF文件: {file.filename} (需要PDF处理)")
        
        # 处理图片
        if images:
            for image in images:
                context_parts.append(f"图片: {image.filename} (需要图像识别)")
        
        # 构建完整的上下文
        full_context = "\n\n".join(context_parts) if context_parts else ""
        
        # 构建AI提示
        prompt = f"""
        用户问题：{question}
        
        相关上下文：
        {full_context}
        
        请根据用户问题和提供的上下文，给出详细、准确的回答。
        """
        
        # 调用AI服务
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个知识渊博的AI助手，擅长回答各种问题。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
        else:
            # 没有配置AI服务时返回示例回答
            answer = f"关于您的问题「{question}」，我需要更多信息来提供准确的答案。请确保已正确配置AI服务。"
        
        # 保存到数据库
        db_qa = QASession(
            user_id=current_user.id,
            question=question,
            answer=answer,
            context=full_context
        )
        
        db.add(db_qa)
        db.commit()
        db.refresh(db_qa)
        
        return {
            "success": True,
            "question": question,
            "answer": answer,
            "session_id": db_qa.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"问答处理失败: {str(e)}"
        )

@router.post("/", response_model=QAResponse)
async def ask_question(
    qa_request: QARequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """简单问答"""
    try:
        # 构建AI提示
        prompt = f"""
        用户问题：{qa_request.question}
        
        {f"相关上下文：{qa_request.context}" if qa_request.context else ""}
        
        请给出详细、准确的回答。
        """
        
        # 调用AI服务
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个知识渊博的AI助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
        else:
            answer = f"关于您的问题「{qa_request.question}」，我需要更多信息来提供准确的答案。"
        
        # 保存到数据库
        db_qa = QASession(
            user_id=current_user.id,
            question=qa_request.question,
            answer=answer,
            context=qa_request.context
        )
        
        db.add(db_qa)
        db.commit()
        db.refresh(db_qa)
        
        return QAResponse(
            id=db_qa.id,
            question=db_qa.question,
            answer=db_qa.answer,
            created_at=db_qa.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"问答处理失败: {str(e)}"
        )

@router.get("/history", response_model=List[QAResponse])
async def get_qa_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取问答历史"""
    qa_history = db.query(QASession).filter(
        QASession.user_id == current_user.id
    ).order_by(QASession.created_at.desc()).limit(50).all()
    
    return [
        QAResponse(
            id=qa.id,
            question=qa.question,
            answer=qa.answer,
            created_at=qa.created_at
        )
        for qa in qa_history
    ]
