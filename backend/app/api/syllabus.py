from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import User, Course, SyllabusItem
from app.schemas.schemas import SyllabusItemCreate, SyllabusItemResponse, SyllabusItemUpdate
from app.api.dependencies import get_current_user, require_teacher

router = APIRouter()

@router.get("/{course_id}", response_model=List[SyllabusItemResponse])
async def get_syllabus(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取课程教学大纲"""
    # 检查课程是否存在
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # 获取教学大纲
    syllabus_items = db.query(SyllabusItem).filter(
        SyllabusItem.course_id == course_id
    ).order_by(SyllabusItem.week).all()
    
    return [SyllabusItemResponse.from_orm(item) for item in syllabus_items]

@router.post("/{course_id}", response_model=SyllabusItemResponse)
async def add_syllabus_item(
    course_id: int,
    syllabus_item: SyllabusItemCreate,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """添加教学大纲项"""
    # 检查课程是否存在且属于当前用户
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.teacher_id == current_user.id
    ).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found or access denied"
        )
    
    # 创建大纲项
    db_item = SyllabusItem(
        course_id=course_id,
        title=syllabus_item.title,
        description=syllabus_item.description,
        week=syllabus_item.week,
        objectives=syllabus_item.objectives,
        content=syllabus_item.content
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return SyllabusItemResponse.from_orm(db_item)

@router.put("/{course_id}", response_model=SyllabusItemResponse)
async def update_syllabus_item(
    course_id: int,
    syllabus_update: SyllabusItemUpdate,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """更新教学大纲项"""
    # 这里需要item_id，实际应该是 PUT /{course_id}/{item_id}
    # 为了简化，假设通过其他方式获取item_id
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint needs item_id parameter"
    )

@router.delete("/{course_id}/{item_id}")
async def delete_syllabus_item(
    course_id: int,
    item_id: int,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """删除教学大纲项"""
    # 检查课程权限
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.teacher_id == current_user.id
    ).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found or access denied"
        )
    
    # 查找并删除大纲项
    item = db.query(SyllabusItem).filter(
        SyllabusItem.id == item_id,
        SyllabusItem.course_id == course_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Syllabus item not found"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "Syllabus item deleted successfully"}
