#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则框架模块，负责单个抽选规则的UI展示
"""

import tkinter as tk
import ttkbootstrap as ttk


class RuleFrame:
    """单个抽选规则的UI框架"""
    
    def __init__(self, parent, index, delete_callback, copy_callback, column_metadata=None):
        self.frame = ttk.LabelFrame(parent, text=f"规则 {index+1}")
        self.index = index
        self.delete_callback = delete_callback
        self.copy_callback = copy_callback
        self.column_metadata = column_metadata or {}
        self.filter_widgets = []
        self.filter_vars = {}
        self.selected_fields = []
        
        self._create_top_row()
        self._create_filter_frame()
        self.frame.pack(fill=tk.X, pady=5, padx=5)
        self._generate_filter_widgets()
    
    def _create_top_row(self):
        """创建顶部行（抽选人数和按钮）"""
        top_row = ttk.Frame(self.frame)
        top_row.pack(fill=tk.X, padx=5, pady=5)
        
        # 抽选人数（左侧）
        count_frame = ttk.Frame(top_row)
        count_frame.pack(side=tk.LEFT, padx=5)
        ttk.Label(count_frame, text="抽选人数:").pack(side=tk.LEFT, padx=5, pady=5)
        self.count_var = tk.StringVar(value="1")
        ttk.Entry(count_frame, textvariable=self.count_var, width=8).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 右侧按钮区域
        right_buttons = ttk.Frame(top_row)
        right_buttons.pack(side=tk.RIGHT, padx=5)
        
        self.delete_btn = ttk.Button(right_buttons, text="删除", command=self.delete, bootstyle="danger")
        self.delete_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.copy_btn = ttk.Button(right_buttons, text="复制", command=self.copy, bootstyle="warning")
        self.copy_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.field_select_btn = ttk.Button(right_buttons, text="选择筛选字段", command=self._show_field_selection, bootstyle="secondary")
        self.field_select_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _create_filter_frame(self):
        """创建筛选条件区域"""
        self.filter_frame = ttk.Frame(self.frame)
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def _show_field_selection(self):
        """显示字段选择窗口"""
        self.field_window = ttk.Toplevel(self.frame)
        self.field_window.title(f"选择筛选字段 - 规则 {self.index+1}")
        self.field_window.geometry("600x500")
        self.field_window.transient(self.frame)
        self.field_window.grab_set()
        
        # 创建滚动区域
        scroll_frame = ttk.Frame(self.field_window)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(scroll_frame)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        field_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.create_window((0, 0), window=field_frame, anchor="nw")
        
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        field_frame.bind("<Configure>", on_configure)
        
        # 字段复选框变量
        self.field_vars = {}
        
        ttk.Label(field_frame, text="请选择需要筛选的字段（未选择的字段默认为'全部'）", style="Header.TLabel").pack(anchor=tk.W, pady=10)
        
        for col_name, metadata in self.column_metadata.items():
            if self._is_suitable_filter_column(metadata):
                var = tk.BooleanVar(value=col_name in self.selected_fields)
                self.field_vars[col_name] = var
                ttk.Checkbutton(field_frame, text=col_name, variable=var).pack(anchor=tk.W, padx=10, pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(self.field_window)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(btn_frame, text="确认", command=self._apply_field_selection, bootstyle="success").pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.field_window.destroy, bootstyle="secondary").pack(side=tk.RIGHT, padx=5)
    
    def _apply_field_selection(self):
        """应用字段选择"""
        self.selected_fields = [col for col, var in self.field_vars.items() if var.get()]
        self._generate_filter_widgets()
        self.field_window.destroy()
    
    def _generate_filter_widgets(self):
        """动态生成筛选条件组件"""
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
        
        self.filter_widgets = []
        self.filter_vars.clear()
        
        if self.selected_fields:
            filter_container = ttk.Frame(self.filter_frame)
            filter_container.pack(fill=tk.X, pady=5)
            
            h_scrollbar = ttk.Scrollbar(filter_container, orient=tk.HORIZONTAL)
            h_scrollbar.pack(fill=tk.X, side=tk.BOTTOM)
            
            canvas = tk.Canvas(filter_container, xscrollcommand=h_scrollbar.set, background="#f0f0f0")
            canvas.pack(fill=tk.X, side=tk.TOP, pady=5)
            h_scrollbar.config(command=canvas.xview)
            
            inner_frame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")
            
            def update_scroll_region(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.configure(height=max(60, inner_frame.winfo_reqheight()))
            
            inner_frame.bind("<Configure>", update_scroll_region)
            
            col_index = 0
            for col_name in self.selected_fields:
                if col_name in self.column_metadata:
                    metadata = self.column_metadata[col_name]
                    label = ttk.Label(inner_frame, text=f"{col_name}:")
                    label.grid(row=0, column=col_index, sticky=tk.W, padx=15, pady=10)
                    self.filter_widgets.append(label)
                    col_index += 1
                    
                    var = tk.StringVar(value="全部")
                    values = ["全部"] + list(metadata['unique_values'])
                    if len(values) > 10:
                        values = values[:10] + ["..."]
                    
                    combo = ttk.Combobox(inner_frame, textvariable=var, values=values, width=10)
                    combo.grid(row=0, column=col_index, sticky=tk.W, padx=5, pady=10)
                    self.filter_widgets.append(combo)
                    self.filter_vars[col_name] = var
                    col_index += 1
        else:
            hint_label = ttk.Label(self.filter_frame, text="点击'选择筛选字段'按钮添加筛选条件")
            hint_label.pack(anchor=tk.W, padx=15, pady=15)
            self.filter_widgets.append(hint_label)
    
    def _is_suitable_filter_column(self, metadata):
        """判断列是否适合作为筛选条件"""
        unique_count = len(metadata['unique_values'])
        non_null_ratio = metadata['non_null_count'] / metadata['total_count']
        return 2 <= unique_count <= 20 and non_null_ratio > 0.8
    
    def update_column_metadata(self, column_metadata):
        """更新列元数据并重新生成筛选组件"""
        self.column_metadata = column_metadata
        self._generate_filter_widgets()
    
    def delete(self):
        """删除当前规则"""
        self.delete_callback(self.index)
    
    def copy(self):
        """复制当前规则"""
        self.copy_callback(self.index)
    
    def update_index(self, new_index):
        """更新规则索引和标题"""
        self.index = new_index
        self.frame.config(text=f"规则 {new_index+1}")
    
    def get_rule(self):
        """获取规则数据"""
        rule = {
            'count': int(self.count_var.get()),
            'filters': {}
        }
        
        for col_name, var in self.filter_vars.items():
            value = var.get()
            if value != "全部":
                rule['filters'][col_name] = value
        
        return rule
    
    def destroy(self):
        """销毁框架"""
        self.frame.destroy()
