from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# 用户相关模式
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 认证相关模式
class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# 课程相关模式
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    grade: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    teacher_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 教学大纲相关模式
class SyllabusItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    week: Optional[int] = None
    objectives: Optional[str] = None
    content: Optional[str] = None

class SyllabusItemCreate(SyllabusItemBase):
    course_id: int

class SyllabusItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    week: Optional[int] = None
    objectives: Optional[str] = None
    content: Optional[str] = None

class SyllabusItemResponse(SyllabusItemBase):
    id: int
    course_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 考试相关模式
class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    grade: Optional[str] = None
    duration: int
    total_score: float = 100.0

class ExamCreate(ExamBase):
    course_id: Optional[int] = None
    questions: Optional[str] = None

class ExamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    duration: Optional[int] = None
    total_score: Optional[float] = None
    questions: Optional[str] = None

class ExamResponse(ExamBase):
    id: int
    creator_id: int
    course_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# 作业相关模式
class HomeworkBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    grade: Optional[str] = None
    due_date: Optional[datetime] = None

class HomeworkCreate(HomeworkBase):
    course_id: Optional[int] = None
    questions: Optional[str] = None

class HomeworkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    due_date: Optional[datetime] = None
    questions: Optional[str] = None

class HomeworkResponse(HomeworkBase):
    id: int
    creator_id: int
    course_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# 帖子相关模式
class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class PostResponse(PostBase):
    id: int
    author_id: int
    likes: int
    comments: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 文件相关模式
class FileResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    file_size: int
    content_type: str
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# PPT生成相关模式
class PPTGenerationBase(BaseModel):
    title: str
    config: Optional[str] = None

class PPTGenerationCreate(PPTGenerationBase):
    pass

class PPTGenerationResponse(PPTGenerationBase):
    id: int
    status: str
    result_path: Optional[str] = None
    creator_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 问答相关模式
class QARequest(BaseModel):
    question: str
    context: Optional[str] = None

class QAResponse(BaseModel):
    id: int
    question: str
    answer: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
