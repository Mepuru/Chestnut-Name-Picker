#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块，提供各种辅助功能
"""

import time
from typing import Dict


def format_datetime(timestamp: int) -> str:
    """
    格式化时间戳为可读日期时间字符串
    
    Args:
        timestamp: 时间戳
        
    Returns:
        格式化后的日期时间字符串
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


def format_stats(stats: Dict) -> str:
    """
    格式化统计信息为可读字符串
    
    Args:
        stats: 统计信息字典
        
    Returns:
        格式化后的统计信息字符串
    """
    total_candidates = stats.get('total_candidates', 0)
    
    # 仅保留基础统计信息
    info = []
    info.append(f"本次抽选总人数: {stats.get('selected_count', 0)}人")
    info.append(f"抽选比例: {stats.get('selection_ratio', 0)}% (总候选人数: {total_candidates}人)")
    
    return '\n'.join(info)


def format_student_info(student) -> str:
    """
    格式化学生信息为可读字符串
    
    Args:
        student: 学生数据（Series对象）
        
    Returns:
        格式化后的学生信息字符串
    """
    info = []
    
    # 仅保留学号和姓名作为固定字段
    fixed_fields = ['学号', '姓名']
    
    # 先显示固定字段
    for field in fixed_fields:
        if field in student:
            info.append(f"{field}: {student[field]}")
    
    # 然后动态显示其他所有字段
    for field in student.index:
        if field not in fixed_fields:
            info.append(f"{field}: {student[field]}")
    
    return '\n'.join(info)



