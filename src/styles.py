#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
样式配置模块，负责定义和配置应用程序的UI样式
"""

import ttkbootstrap as ttk


def configure_styles(style: ttk.Style):
    """
    配置应用程序的所有UI样式
    
    Args:
        style: ttkbootstrap样式对象
    """
    # 优化基础样式配置，增强现代感
    style.configure(
        "TLabel", 
        font=("Segoe UI", 10),
        padding=5,
        foreground="#333333"
    )
    
    # 优化按钮样式，添加圆角和阴影效果
    style.configure(
        "TButton", 
        font=("Segoe UI", 10),
        padding=8,
        borderwidth=0,
        borderradius=4
    )
    
    # 增强按钮悬停效果
    style.map(
        "TButton",
        background=[("active", "!disabled", "#e6e6e6"),
                    ("disabled", "#f5f5f5")],
        foreground=[("disabled", "#a0a0a0")]
    )
    
    # 优化标题样式
    style.configure(
        "Header.TLabel", 
        font=("Segoe UI", 12, "bold"),
        padding=10,
        foreground="#2c3e50",
        background="#f8f9fa"
    )
    
    # 优化标签框架样式
    style.configure(
        "TLabelframe",
        background="#ffffff",
        borderwidth=1,
        bordercolor="#e0e0e0",
        borderradius=6,
        padding=6,
        relief="solid"
    )
    
    # 优化滚动条样式
    style.configure(
        "Vertical.TScrollbar",
        background="#e9ecef",
        troughcolor="#f8f9fa",
        arrowcolor="#6c757d",
        borderwidth=0,
        borderradius=4
    )
    
    style.configure(
        "Horizontal.TScrollbar",
        background="#e9ecef",
        troughcolor="#f8f9fa",
        arrowcolor="#6c757d",
        borderwidth=0,
        borderradius=4
    )
    
    # 增强滚动条悬停效果
    style.map(
        "Vertical.TScrollbar",
        background=[("active", "!disabled", "#dee2e6"),
                    ("hover", "!disabled", "#dee2e6")],
        arrowcolor=[("active", "!disabled", "#495057"),
                   ("hover", "!disabled", "#495057")]
    )
    
    style.map(
        "Horizontal.TScrollbar",
        background=[("active", "!disabled", "#dee2e6"),
                    ("hover", "!disabled", "#dee2e6")],
        arrowcolor=[("active", "!disabled", "#495057"),
                   ("hover", "!disabled", "#495057")]
    )
    
    # 优化输入框样式
    style.configure(
        "TEntry",
        font=("Segoe UI", 10),
        padding=6,
        background="#ffffff",
        borderwidth=1,
        bordercolor="#ced4da",
        borderradius=4,
        relief="solid"
    )
    
    # 增强输入框焦点效果
    style.map(
        "TEntry",
        bordercolor=[("focus", "#007bff"),
                    ("active", "#80bdff")],
        background=[("disabled", "#f5f5f5")],
        foreground=[("disabled", "#a0a0a0")]
    )
    
    # 优化下拉框样式
    style.configure(
        "TCombobox",
        font=("Segoe UI", 10),
        padding=6,
        background="#ffffff",
        borderwidth=1,
        bordercolor="#ced4da",
        borderradius=4,
        relief="solid"
    )
    
    # 增强下拉框交互效果
    style.map(
        "TCombobox",
        bordercolor=[("focus", "#007bff"),
                    ("active", "#80bdff")],
        background=[("disabled", "#f5f5f5"),
                    ("!disabled", "#ffffff")],
        foreground=[("disabled", "#a0a0a0"),
                   ("!disabled", "#333333")]
    )
    
    # 优化复选框样式
    style.configure(
        "TCheckbutton",
        font=("Segoe UI", 10),
        padding=4
    )
    
    # 增强复选框交互效果
    style.map(
        "TCheckbutton",
        background=[("active", "!disabled", "#e9ecef"),
                    ("disabled", "#f5f5f5")],
        foreground=[("disabled", "#a0a0a0"),
                   ("!disabled", "#333333")]
    )
    
    # 优化表格（Treeview）样式
    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        background="#ffffff",
        foreground="#333333",
        fieldbackground="#ffffff",
        borderwidth=1,
        bordercolor="#e0e0e0",
        rowheight=28,
        relief="solid"
    )
    
    # 优化表格表头样式
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#f8f9fa",
        foreground="#2c3e50",
        padding=8,
        borderwidth=1,
        bordercolor="#e0e0e0",
        relief="solid"
    )
    
    # 增强表头悬停效果
    style.map(
        "Treeview.Heading",
        background=[("hover", "#e9ecef")],
        foreground=[("hover", "#1a252f")]
    )
    
    # 增强表格行交互效果
    style.map(
        "Treeview",
        background=[("selected", "#007bff"),
                    ("active", "#e9ecef")],
        foreground=[("selected", "#ffffff"),
                   ("active", "#007bff")]
    )
    
    # 优化标签框架标题样式
    style.configure(
        "TLabelframe.Label",
        font=("Segoe UI", 11, "bold"),
        foreground="#2c3e50",
        background="#ffffff",
        padding=4
    )
    
    # 优化选项卡样式
    style.configure(
        "Tab.TNotebook", 
        font=("Segoe UI", 10),
        background="#f8f9fa",
        borderwidth=0
    )
    
    # 优化选项卡标签样式
    style.configure(
        "TNotebook.Tab",
        font=("Segoe UI", 10),
        padding=[12, 6],
        borderwidth=0,
        borderradius=4
    )
    
    # 增强选项卡标签悬停和选中效果
    style.map(
        "TNotebook.Tab",
        background=[("selected", "#ffffff"),
                    ("active", "!disabled", "#e9ecef"),
                    ("!active", "#f8f9fa")],
        foreground=[("selected", "#007bff"),
                    ("!selected", "#6c757d")]
    )
    
    # 配置ttkbootstrap按钮样式
    _configure_button_styles(style)


def _configure_button_styles(style: ttk.Style):
    """
    配置按钮相关样式
    
    Args:
        style: ttkbootstrap样式对象
    """
    # Primary按钮
    style.configure(
        "Primary.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        background="#007bff",
        foreground="white",
        borderwidth=0,
        borderradius=4
    )
    
    style.map(
        "Primary.TButton",
        background=[("active", "!disabled", "#0056b3"),
                    ("hover", "!disabled", "#0069d9")],
        foreground=[("disabled", "#a0a0a0")]
    )
    
    # Secondary按钮
    style.configure(
        "Secondary.TButton",
        font=("Segoe UI", 10),
        padding=8,
        background="#6c757d",
        foreground="white",
        borderwidth=0,
        borderradius=4
    )
    
    style.map(
        "Secondary.TButton",
        background=[("active", "!disabled", "#545b62"),
                    ("hover", "!disabled", "#5a6268")],
        foreground=[("disabled", "#a0a0a0")]
    )
    
    # Danger按钮
    style.configure(
        "Danger.TButton",
        font=("Segoe UI", 10),
        padding=8,
        background="#dc3545",
        foreground="white",
        borderwidth=0,
        borderradius=4
    )
    
    style.map(
        "Danger.TButton",
        background=[("active", "!disabled", "#c82333"),
                    ("hover", "!disabled", "#c82333")],
        foreground=[("disabled", "#a0a0a0")]
    )
    
    # Success按钮
    style.configure(
        "Success.TButton",
        font=("Segoe UI", 10),
        padding=8,
        background="#28a745",
        foreground="white",
        borderwidth=0,
        borderradius=4
    )
    
    style.map(
        "Success.TButton",
        background=[("active", "!disabled", "#1e7e34"),
                    ("hover", "!disabled", "#218838")],
        foreground=[("disabled", "#a0a0a0")]
    )
    
    # Warning按钮
    style.configure(
        "Warning.TButton",
        font=("Segoe UI", 10),
        padding=8,
        background="#ffc107",
        foreground="#212529",
        borderwidth=0,
        borderradius=4
    )
    
    style.map(
        "Warning.TButton",
        background=[("active", "!disabled", "#e0a800"),
                    ("hover", "!disabled", "#e0a800")],
        foreground=[("disabled", "#a0a0a0")]
    )
