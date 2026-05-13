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
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self.main_container = ttk.Frame(self.window)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_file_info(self):
        """创建文件信息区域"""
        file_info_frame = ttk.Frame(self.main_container)
        file_info_frame.pack(fill=tk.X, pady=5)
        ttk.Label(file_info_frame, text=f"文件路径: {self.file_path}").pack(anchor=tk.W)
    
    def _create_stats_section(self):
        """创建数据统计区域"""
        stats_frame = ttk.LabelFrame(self.main_container, text="数据统计")
        stats_frame.pack(fill=tk.X, pady=10, padx=10, ipady=10)
        
        stats_text = f"总行数: {len(self.data_handler.df)}\n"
        stats_text += f"总列数: {len(self.data_handler.columns)}\n"
        stats_text += f"列名: {', '.join(self.data_handler.columns)}\n"
        
        ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT).pack(anchor=tk.W, padx=5, pady=5)
    
    def _create_data_table(self):
        """创建数据表格"""
        table_frame = ttk.LabelFrame(self.main_container, text="数据预览（前20行）")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10, ipady=10)
        
        columns = self.data_handler.columns
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        preview_data = self.data_handler.df.head(20)
        for _, row in preview_data.iterrows():
            values = [str(row[col]) for col in columns]
            self.tree.insert("", tk.END, values=values)
    
    def _create_buttons(self):
        """创建按钮区域"""
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame, 
            text="确认", 
            command=self.confirm, 
            width=10,
            bootstyle="success"
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="取消", 
            command=self.cancel, 
            width=10,
            bootstyle="secondary"
        ).pack(side=tk.RIGHT, padx=5)
    
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
