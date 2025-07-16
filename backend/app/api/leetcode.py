from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import User
from app.api.dependencies import get_current_user
import json

router = APIRouter()

@router.get("/problems", response_model=dict)
async def search_problems(
    difficulty: Optional[str] = None,
    tags: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """搜索LeetCode题目"""
    try:
        # 模拟LeetCode题目数据
        problems = [
            {
                "id": 1,
                "title": "Two Sum",
                "difficulty": "Easy",
                "tags": ["Array", "Hash Table"],
                "acceptance_rate": 49.5,
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
            },
            {
                "id": 2,
                "title": "Add Two Numbers",
                "difficulty": "Medium",
                "tags": ["Linked List", "Math"],
                "acceptance_rate": 36.8,
                "description": "You are given two non-empty linked lists representing two non-negative integers."
            },
            {
                "id": 3,
                "title": "Longest Substring Without Repeating Characters",
                "difficulty": "Medium",
                "tags": ["String", "Sliding Window"],
                "acceptance_rate": 33.9,
                "description": "Given a string s, find the length of the longest substring without repeating characters."
            }
        ]
        
        # 简单的筛选逻辑
        if difficulty:
            problems = [p for p in problems if p["difficulty"].lower() == difficulty.lower()]
        
        return {
            "problems": problems,
            "total": len(problems)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"搜索题目失败: {str(e)}"
        )

@router.get("/problems/{problem_id}", response_model=dict)
async def get_problem_detail(
    problem_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取题目详情"""
    try:
        # 模拟题目详情
        problem_detail = {
            "id": problem_id,
            "title": "Two Sum",
            "difficulty": "Easy",
            "tags": ["Array", "Hash Table"],
            "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.""",
            "examples": [
                {
                    "input": "nums = [2,7,11,15], target = 9",
                    "output": "[0,1]",
                    "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
                }
            ],
            "constraints": [
                "2 <= nums.length <= 10^4",
                "-10^9 <= nums[i] <= 10^9",
                "-10^9 <= target <= 10^9",
                "Only one valid answer exists."
            ]
        }
        
        return problem_detail
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取题目详情失败: {str(e)}"
        )

@router.post("/hint", response_model=dict)
async def get_hint(
    hint_request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取AI提示"""
    try:
        problem_id = hint_request.get("problemId")
        language = hint_request.get("language", "python")
        code = hint_request.get("code", "")
        
        # 模拟AI提示
        hint = {
            "problem_id": problem_id,
            "language": language,
            "hint": "考虑使用哈希表来存储已经遍历过的数字及其索引。这样可以在O(1)时间内查找目标数字。",
            "next_step": "尝试遍历数组，对于每个数字，检查target减去当前数字的结果是否在哈希表中。"
        }
        
        return hint
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取提示失败: {str(e)}"
        )

@router.post("/run", response_model=dict)
async def run_code(
    run_request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """运行代码"""
    try:
        problem_id = run_request.get("problemId")
        language = run_request.get("language", "python")
        code = run_request.get("code", "")
        
        # 模拟代码运行结果
        result = {
            "problem_id": problem_id,
            "language": language,
            "status": "Accepted",
            "runtime": "52 ms",
            "memory": "14.1 MB",
            "test_results": [
                {
                    "input": "[2,7,11,15], 9",
                    "expected": "[0,1]",
                    "actual": "[0,1]",
                    "passed": True
                }
            ]
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"运行代码失败: {str(e)}"
        )

@router.post("/submit", response_model=dict)
async def submit_code(
    submit_request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交代码"""
    try:
        problem_id = submit_request.get("problemId")
        language = submit_request.get("language", "python")
        code = submit_request.get("code", "")
        
        # 模拟提交结果
        result = {
            "problem_id": problem_id,
            "language": language,
            "status": "Accepted",
            "runtime": "48 ms",
            "memory": "13.9 MB",
            "runtime_percentile": 85.2,
            "memory_percentile": 91.7,
            "submission_id": 12345
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交代码失败: {str(e)}"
        )
