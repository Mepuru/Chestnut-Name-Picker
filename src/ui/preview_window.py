#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据预览窗口模块，负责展示Excel数据预览
"""

import tkinter as tk
import ttkbootstrap as ttk


class DataPreviewWindow:
    """数据预览窗口"""
    
    def __init__(self, parent, data_handler, file_path):
        """
        初始化数据预览窗口
        
        Args:
            parent: 父窗口
            data_handler: 数据处理器
            file_path: 文件路径
        """
        self.parent = parent
        self.data_handler = data_handler
        self.file_path = file_path
        self.result = False
        
        self._create_window()
        self._create_file_info()
        self._create_stats_section()
        self._create_data_table()
        self._create_buttons()
    
    def _create_window(self):
        """创建预览窗口"""
        self.window = ttk.Toplevel(self.parent)
        self.window.title("数据预览")
        
        # 获取屏幕尺寸，自适应窗口大小
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = min(900, int(screen_width * 0.8))
        window_height = min(700, int(screen_height * 0.8))
        
        # 居中显示
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.window.resizable(True, True)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # 主容器使用 grid 布局，确保按钮固定在底部
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.main_container = ttk.Frame(self.window)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_rowconfigure(2, weight=1)  # 表格区域可扩展
        self.main_container.grid_columnconfigure(0, weight=1)
    
    def _create_file_info(self):
        """创建文件信息区域"""
        file_info_frame = ttk.Frame(self.main_container)
        file_info_frame.grid(row=0, column=0, sticky="ew", pady=5)
        ttk.Label(file_info_frame, text=f"文件路径: {self.file_path}").pack(anchor=tk.W)
    
    def _create_stats_section(self):
        """创建数据统计区域"""
        stats_frame = ttk.LabelFrame(self.main_container, text="数据统计")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=10, padx=10)
        
        stats_text = f"总行数: {len(self.data_handler.df)}\n"
        stats_text += f"总列数: {len(self.data_handler.columns)}\n"
        stats_text += f"列名: {', '.join(self.data_handler.columns)}\n"
        
        ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT).pack(anchor=tk.W, padx=5, pady=5)
    
    def _create_data_table(self):
        """创建数据表格"""
        table_frame = ttk.LabelFrame(self.main_container, text="数据预览（前20行）")
        table_frame.grid(row=2, column=0, sticky="nsew", pady=10, padx=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        columns = self.data_handler.columns
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        preview_data = self.data_handler.df.head(20)
        for _, row in preview_data.iterrows():
            values = [str(row[col]) for col in columns]
            self.tree.insert("", tk.END, values=values)
    
    def _create_buttons(self):
        """创建按钮区域 - 固定在底部"""
        button_frame = ttk.Frame(self.main_container)
        button_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        # 使用 grid 布局让按钮居中
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)
        
        ttk.Button(
            button_frame, 
            text="确认", 
            command=self.confirm, 
            width=12,
            bootstyle="success"
        ).grid(row=0, column=1, padx=10)
        
        ttk.Button(
            button_frame, 
            text="取消", 
            command=self.cancel, 
            width=12,
            bootstyle="secondary"
        ).grid(row=0, column=2, padx=10)
    
    def confirm(self):
        """确认选择"""
        self.result = True
        self.window.destroy()
    
    def cancel(self):
        """取消选择"""
        self.result = False
        self.window.destroy()
    
    def get_result(self):
        """获取选择结果"""
        return self.result
