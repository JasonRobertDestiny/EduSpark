from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import User, PPTGeneration
from app.schemas.schemas import PPTGenerationCreate, PPTGenerationResponse
from app.api.dependencies import get_current_user, require_teacher
import json
import openai
from app.core.config import settings

router = APIRouter()

@router.post("/generate", response_model=dict)
async def generate_ppt(
    ppt_config: dict,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """生成智能PPT"""
    try:
        # 从前端获取的配置
        title = ppt_config.get("title", "")
        description = ppt_config.get("description", "")
        audience = ppt_config.get("audience", "")
        duration = ppt_config.get("duration", 15)
        style = ppt_config.get("style", "professional")
        slide_count = ppt_config.get("slideCount", 10)
        include_images = ppt_config.get("includeImages", False)
        
        # 构建AI提示
        prompt = f"""
        请为以下条件生成一份PPT大纲：
        
        PPT标题：{title}
        内容描述：{description}
        目标受众：{audience}
        演示时长：{duration}分钟
        PPT风格：{style}
        预期页数：{slide_count}页
        是否包含图片：{include_images}
        
        请按照以下JSON格式返回PPT大纲：
        {{
            "title": "{title}",
            "slides": [
                {{
                    "id": 1,
                    "title": "幻灯片标题",
                    "content": "幻灯片内容要点",
                    "layout": "title_slide",
                    "notes": "演讲者备注"
                }}
            ]
        }}
        
        请确保内容结构合理，适合{audience}群体，时长控制在{duration}分钟内。
        """
        
        # 调用AI生成PPT大纲
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的演示文稿设计师，擅长制作精美的PPT。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            generated_content = response.choices[0].message.content
            
            try:
                ppt_data = json.loads(generated_content)
            except json.JSONDecodeError:
                ppt_data = {
                    "title": title,
                    "slides": [
                        {
                            "id": 1,
                            "title": "封面",
                            "content": title,
                            "layout": "title_slide",
                            "notes": "欢迎大家参加今天的演示"
                        },
                        {
                            "id": 2,
                            "title": "目录",
                            "content": "1. 引言\n2. 主要内容\n3. 总结",
                            "layout": "content_slide",
                            "notes": "介绍今天的演示内容"
                        }
                    ]
                }
        else:
            # 没有配置AI服务时返回示例数据
            ppt_data = {
                "title": title,
                "slides": [
                    {
                        "id": 1,
                        "title": "封面",
                        "content": title,
                        "layout": "title_slide",
                        "notes": "欢迎大家参加今天的演示"
                    },
                    {
                        "id": 2,
                        "title": "目录",
                        "content": "1. 引言\n2. 主要内容\n3. 总结",
                        "layout": "content_slide",
                        "notes": "介绍今天的演示内容"
                    }
                ]
            }
        
        # 保存到数据库
        db_ppt = PPTGeneration(
            title=title,
            config=json.dumps(ppt_config),
            status="completed",
            creator_id=current_user.id
        )
        
        db.add(db_ppt)
        db.commit()
        db.refresh(db_ppt)
        
        return {
            "success": True,
            "ppt_id": db_ppt.id,
            "ppt_data": ppt_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成PPT失败: {str(e)}"
        )

@router.get("/", response_model=List[PPTGenerationResponse])
async def get_ppt_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取PPT列表"""
    ppt_list = db.query(PPTGeneration).filter(PPTGeneration.creator_id == current_user.id).all()
    return ppt_list

@router.get("/{ppt_id}", response_model=PPTGenerationResponse)
async def get_ppt(
    ppt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取PPT详情"""
    ppt = db.query(PPTGeneration).filter(PPTGeneration.id == ppt_id).first()
    if not ppt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PPT not found"
        )
    
    # 检查权限
    if ppt.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this PPT"
        )
    
    return ppt
