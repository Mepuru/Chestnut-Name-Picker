#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块，提供各种辅助功能
"""

import time
import tkinter as tk
import ttkbootstrap as ttk
from typing import Dict, Tuple


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


def create_scrollable_frame(parent: ttk.Frame, tag: str = "content") -> Tuple[tk.Canvas, ttk.Frame]:
    """
    创建带垂直滚动条的可滚动框架
    
    Args:
        parent: 父容器
        tag: 画布窗口标签，用于后续配置
        
    Returns:
        (canvas, inner_frame) 元组
    """
    # 创建带垂直滚动条的容器
    scrollable_container = ttk.Frame(parent)
    scrollable_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # 创建垂直滚动条
    v_scrollbar = ttk.Scrollbar(scrollable_container, orient=tk.VERTICAL)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 创建画布
    canvas = tk.Canvas(scrollable_container, yscrollcommand=v_scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    v_scrollbar.config(command=canvas.yview)
    
    # 创建内部框架
    inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW, tags=tag)
    
    # 绑定内部框架大小变化事件，更新滚动区域
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    inner_frame.bind("<Configure>", update_scroll_region)
    
    # 绑定画布大小变化事件，更新内部框架宽度
    def update_canvas_width(event):
        canvas_width = event.width - 2
        canvas.itemconfig(tag, width=canvas_width)
    
    canvas.bind("<Configure>", update_canvas_width)
    
    return canvas, inner_frame

