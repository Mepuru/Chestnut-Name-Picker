#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI界面模块，负责设计和实现现代化选项卡式操作界面
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from src.data_handler import DataHandler
from src.selector import StudentSelector
from src.utils import format_datetime, format_stats
from src.styles import configure_styles

BASE_DIR = Path(__file__).parent.parent


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
        self.selected_fields = []  # 存储用户选择的筛选字段
        
        # 创建第一行容器，使用pack布局替代grid，便于右侧对齐
        top_row = ttk.Frame(self.frame)
        top_row.pack(fill=tk.X, padx=5, pady=5)
        
        # 抽选人数（左侧）
        count_frame = ttk.Frame(top_row)
        count_frame.pack(side=tk.LEFT, padx=5)
        ttk.Label(count_frame, text="抽选人数:").pack(side=tk.LEFT, padx=5, pady=5)
        self.count_var = tk.StringVar(value="1")
        ttk.Entry(count_frame, textvariable=self.count_var, width=8).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 右侧按钮区域（字段选择和删除按钮挨在一起）
        right_buttons = ttk.Frame(top_row)
        right_buttons.pack(side=tk.RIGHT, padx=5)
        
        # 删除按钮
        self.delete_btn = ttk.Button(right_buttons, text="删除", command=self.delete, bootstyle="danger")
        self.delete_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 复制按钮
        self.copy_btn = ttk.Button(right_buttons, text="复制", command=self.copy, bootstyle="warning")
        self.copy_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 字段选择按钮
        self.field_select_btn = ttk.Button(right_buttons, text="选择筛选字段", command=self._show_field_selection, bootstyle="secondary")
        self.field_select_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 动态生成筛选条件区域（使用pack布局，确保填满宽度）
        self.filter_frame = ttk.Frame(self.frame)
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.frame.pack(fill=tk.X, pady=5, padx=5)
        
        # 初始化筛选条件
        self._generate_filter_widgets()
    
    def _show_field_selection(self):
        """显示字段选择窗口"""
        # 创建字段选择窗口 - 使用ttkbootstrap的窗口
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
        
        # 创建字段复选框
        ttk.Label(field_frame, text="请选择需要筛选的字段（未选择的字段默认为'全部'）", style="Header.TLabel").pack(anchor=tk.W, pady=10)
        
        for col_name, metadata in self.column_metadata.items():
            if self._is_suitable_filter_column(metadata):
                var = tk.BooleanVar(value=col_name in self.selected_fields)
                self.field_vars[col_name] = var
                ttk.Checkbutton(field_frame, text=col_name, variable=var).pack(anchor=tk.W, padx=10, pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(self.field_window)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # 确认按钮
        confirm_btn = ttk.Button(btn_frame, text="确认", command=self._apply_field_selection, bootstyle="success")
        confirm_btn.pack(side=tk.RIGHT, padx=5)
        
        # 取消按钮
        cancel_btn = ttk.Button(btn_frame, text="取消", command=self.field_window.destroy, bootstyle="secondary")
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def _apply_field_selection(self):
        """应用字段选择"""
        # 更新选中的字段
        self.selected_fields = [col for col, var in self.field_vars.items() if var.get()]
        
        # 重新生成筛选条件
        self._generate_filter_widgets()
        
        # 关闭字段选择窗口
        self.field_window.destroy()
    
    def _generate_filter_widgets(self):
        """动态生成筛选条件组件"""
        # 清空filter_frame中的所有子组件，包括滚动框架和提示标签
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
        
        # 清空现有筛选组件列表和变量
        self.filter_widgets = []
        self.filter_vars.clear()
        
        # 只有在用户手动选择了字段时才生成筛选组件
        if self.selected_fields:
            # 创建一个frame作为筛选条件的容器，使用pack布局确保填满宽度
            filter_container = ttk.Frame(self.filter_frame)
            filter_container.pack(fill=tk.X, pady=5)
            
            # 创建一个水平滚动条，用于在筛选条件过多时滚动查看
            h_scrollbar = ttk.Scrollbar(filter_container, orient=tk.HORIZONTAL)
            h_scrollbar.pack(fill=tk.X, side=tk.BOTTOM)
            
            # 创建画布用于放置筛选组件
            canvas = tk.Canvas(filter_container, xscrollcommand=h_scrollbar.set, background="#f0f0f0")
            canvas.pack(fill=tk.X, side=tk.TOP, pady=5)
            h_scrollbar.config(command=canvas.xview)
            
            # 创建内部框架放置实际的筛选组件
            inner_frame = ttk.Frame(canvas)
            # 使用画布窗口放置内部框架，不设置固定宽度，让内部框架根据内容自由扩展
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")
            
            # 绑定内部框架大小变化事件，更新画布滚动区域
            def update_scroll_region(event):
                # 确保画布滚动区域包含内部框架的所有内容
                canvas.configure(scrollregion=canvas.bbox("all"))
                # 动态调整画布高度，确保内容完整显示
                canvas.configure(height=max(60, inner_frame.winfo_reqheight()))
            
            # 绑定内部框架大小变化事件
            inner_frame.bind("<Configure>", update_scroll_region)
            
            # 遍历选中的字段，生成筛选组件
            col_index = 0
            for col_name in self.selected_fields:
                if col_name in self.column_metadata:
                    metadata = self.column_metadata[col_name]
                    # 筛选条件标签
                    label = ttk.Label(inner_frame, text=f"{col_name}:")
                    label.grid(row=0, column=col_index, sticky=tk.W, padx=15, pady=10)
                    self.filter_widgets.append(label)
                    col_index += 1
                    
                    # 筛选条件下拉框
                    var = tk.StringVar(value="全部")
                    # 生成下拉框选项：全部 + 唯一值
                    values = ["全部"] + list(metadata['unique_values'])
                    # 限制选项数量，避免下拉框过长
                    if len(values) > 10:
                        values = values[:10] + ["..."]
                    
                    combo = ttk.Combobox(inner_frame, textvariable=var, values=values, width=10)
                    combo.grid(row=0, column=col_index, sticky=tk.W, padx=5, pady=10)
                    self.filter_widgets.append(combo)
                    self.filter_vars[col_name] = var
                    col_index += 1
        else:
            # 如果没有选择字段，显示提示信息
            hint_label = ttk.Label(self.filter_frame, text="点击'选择筛选字段'按钮添加筛选条件")
            hint_label.pack(anchor=tk.W, padx=15, pady=15)
            self.filter_widgets.append(hint_label)
    
    def _is_suitable_filter_column(self, metadata):
        """判断列是否适合作为筛选条件"""
        # 适合作为筛选条件的列：
        # 1. 唯一值数量适中（2-20个）
        # 2. 非空值比例较高
        unique_count = len(metadata['unique_values'])
        non_null_ratio = metadata['non_null_count'] / metadata['total_count']
        
        return 2 <= unique_count <= 20 and non_null_ratio > 0.8
    
    def update_column_metadata(self, column_metadata):
        """更新列元数据并重新生成筛选组件"""
        self.column_metadata = column_metadata
        # 重新生成筛选组件，但保持当前选中的字段不变
        self._generate_filter_widgets()
        
        # 优化删除按钮位置 - 删除按钮固定在右侧，不随筛选字段数量变化而移动
        # 这样可以保持界面布局的稳定性
    
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
        
        # 收集所有筛选条件
        for col_name, var in self.filter_vars.items():
            value = var.get()
            if value != "全部":
                rule['filters'][col_name] = value
        
        return rule
    
    def destroy(self):
        """销毁框架"""
        self.frame.destroy()


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
        
        # 创建预览窗口
        self.window = ttk.Toplevel(parent)
        self.window.title("数据预览")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        self.window.transient(parent)  # 设置为父窗口的子窗口
        self.window.grab_set()  # 模态窗口
        

        
        # 创建主容器
        main_container = ttk.Frame(self.window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 文件信息
        file_info_frame = ttk.Frame(main_container)
        file_info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_info_frame, text=f"文件路径: {file_path}").pack(anchor=tk.W)
        
        # 数据统计
        stats_frame = ttk.LabelFrame(main_container, text="数据统计")
        stats_frame.pack(fill=tk.X, pady=10, padx=10, ipady=10)
        
        stats = data_handler.get_statistics()
        stats_text = f"总行数: {len(data_handler.df)}\n"
        stats_text += f"总列数: {len(data_handler.columns)}\n"
        stats_text += f"列名: {', '.join(data_handler.columns)}\n"
        
        ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT).pack(anchor=tk.W, padx=5, pady=5)
        
        # 数据表格
        table_frame = ttk.LabelFrame(main_container, text="数据预览（前20行）")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10, ipady=10)
        
        # 创建表格
        columns = data_handler.columns
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # 添加滚动条
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # 布局
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 添加数据到表格（前20行）
        preview_data = data_handler.df.head(20)
        for _, row in preview_data.iterrows():
            values = [str(row[col]) for col in columns]
            self.tree.insert("", tk.END, values=values)
        
        # 按钮区域
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 确认按钮 - 使用ttkbootstrap样式
        confirm_btn = ttk.Button(
            button_frame, 
            text="确认", 
            command=self.confirm, 
            width=10,
            bootstyle="success"
        )
        confirm_btn.pack(side=tk.RIGHT, padx=5)
        
        # 取消按钮 - 使用ttkbootstrap样式
        cancel_btn = ttk.Button(
            button_frame, 
            text="取消", 
            command=self.cancel, 
            width=10,
            bootstyle="secondary"
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
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


class ClassSelectorUI:
    """ChestNut名单抽选工具GUI界面"""
    
    def __init__(self):
        """初始化GUI界面"""
        # 使用ttkbootstrap创建应用程序实例，应用现代化主题
        self.root = ttk.Window(themename="litera")  # 升级为更现代的litera主题
        self.root.title("ChestNut名单抽选工具V1.0")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # 全面设置窗口图标，确保在Windows任务栏和所有窗口上正确显示
        try:
            # 保存原始图片路径，用于后续可能的Windows API调用
            self.icon_path = str(BASE_DIR / "assets" / "chestnut_2153101.png")
            
            # 使用PIL库处理图片
            img = Image.open(self.icon_path)
            
            # 创建不同大小的图标，适应不同的显示需求
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
            self.app_icons = []
            
            for size in icon_sizes:
                resized_img = img.resize(size, Image.Resampling.LANCZOS)
                self.app_icons.append(ImageTk.PhotoImage(resized_img))
            
            # 同时设置所有大小的图标，增加在不同场景下显示的概率
            self.root.iconphoto(True, *self.app_icons)
            print("使用PIL+iconphoto成功设置主窗口图标")
            
            # 尝试使用不同的方法再次设置，确保兼容性
            try:
                # 尝试使用第一个图标作为单独设置
                self.root.iconphoto(False, self.app_icons[0])
                print("使用单个图标再次设置成功")
            except Exception as e:
                print(f"使用单个图标再次设置失败: {e}")
        except Exception as e:
            print(f"全面设置图标失败: {e}")
        
        # 设置字体样式
        self.style = ttk.Style()
        
        # 使用styles模块配置所有样式
        configure_styles(self.style)
        
        # 初始化数据处理器和抽选器为None
        self.data_handler = None
        self.selector = None
        self.current_file_path = None
        
        # 规则列表
        self.rule_frames = []
        
        # 创建主要组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建GUI组件"""
        # 创建选项卡控件
        self.notebook = ttk.Notebook(self.root, style="Tab.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建抽选条件选项卡
        self.condition_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.condition_frame, text="抽选条件")
        
        # 创建抽选结果选项卡
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="抽选结果")
        
        # 初始化抽选条件界面
        self.init_condition_tab()
        
        # 初始化抽选结果界面
        self.init_result_tab()
        
    def init_condition_tab(self):
        """初始化抽选条件选项卡"""
        # 创建主容器
        main_container = ttk.Frame(self.condition_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 文件选择区域
        self.add_file_selection_buttons(main_container)
        
        # 种子设置（移到抽选规则上方）
        seed_frame = ttk.LabelFrame(main_container, text="随机种子")
        seed_frame.pack(fill=tk.X, pady=15, padx=10, ipady=10)
        
        seed_container = ttk.Frame(seed_frame)
        seed_container.pack(fill=tk.X)
        
        ttk.Label(seed_container, text="种子值（留空则使用当前时间）:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.seed_var = tk.StringVar(value="")
        self.seed_entry = ttk.Entry(seed_container, textvariable=self.seed_var, width=30)
        self.seed_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 规则管理区域（整体）
        self.rules_section = ttk.Frame(main_container)
        
        # 规则标题和操作按钮
        rules_header = ttk.Frame(self.rules_section)
        rules_header.pack(fill=tk.X, pady=10)
        
        rules_label = ttk.Label(rules_header, text="抽选规则设置", style="Header.TLabel")
        rules_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # 抽选按钮（放在添加规则按钮左侧）
        self.select_button = ttk.Button(
            rules_header, 
            text="开始抽选", 
            command=self.perform_selection, 
            width=12, 
            state=tk.DISABLED,  # 初始禁用
            bootstyle="success"
        )
        self.select_button.pack(side=tk.RIGHT, padx=5)
        
        # 添加规则按钮
        add_rule_btn = ttk.Button(
            rules_header, 
            text="添加规则", 
            command=self.add_rule,
            bootstyle="primary"
        )
        add_rule_btn.pack(side=tk.RIGHT, padx=5)
        
        # 规则容器（带滚动条）
        rules_scroll_frame = ttk.Frame(self.rules_section)
        rules_scroll_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建画布和滚动条
        canvas = tk.Canvas(rules_scroll_frame)
        scrollbar = ttk.Scrollbar(rules_scroll_frame, orient="vertical", command=canvas.yview)
        self.rules_container = ttk.Frame(canvas)
        
        # 配置画布
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 将规则容器添加到画布
        def update_canvas_width():
            # 计算画布可用宽度，减去滚动条的宽度
            scrollbar_width = scrollbar.winfo_width()
            canvas_width = rules_scroll_frame.winfo_width() - scrollbar_width
            # 更新规则容器的宽度
            canvas.itemconfig("rules_container", width=canvas_width)
            # 更新画布滚动区域
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # 创建规则容器窗口，设置初始宽度
        canvas.create_window((0, 0), window=self.rules_container, anchor="nw", tags="rules_container")
        
        # 绑定规则容器大小变化事件，更新画布滚动区域
        def on_configure(event):
            update_canvas_width()
        
        # 绑定滚动框架大小变化事件，动态调整画布宽度
        rules_scroll_frame.bind("<Configure>", on_configure)
        self.rules_container.bind("<Configure>", on_configure)
        
        # 初始化时更新一次宽度
        update_canvas_width()
        
        # 初始状态：隐藏抽选规则区域
        self.show_rule_section(False)
        
    def add_rule(self, existing_rule_data=None):
        """添加一个抽选规则，可接受现有规则数据进行复制"""
        index = len(self.rule_frames)
        # 获取列元数据，如果未加载数据则为空
        column_metadata = self.data_handler.get_column_metadata() if self.data_handler else {}
        rule_frame = RuleFrame(self.rules_container, index, self.remove_rule, self.copy_rule, column_metadata)
        
        # 如果有现有规则数据，复制其配置
        if existing_rule_data:
            # 设置抽选人数
            rule_frame.count_var.set(str(existing_rule_data['count']))
            # 设置选中的字段
            rule_frame.selected_fields = existing_rule_data['selected_fields'].copy()
            # 重新生成筛选组件
            rule_frame._generate_filter_widgets()
            # 设置筛选值
            for col_name, value in existing_rule_data['filters'].items():
                if col_name in rule_frame.filter_vars:
                    rule_frame.filter_vars[col_name].set(value)
        
        self.rule_frames.append(rule_frame)
    
    def copy_rule(self, index):
        """复制指定索引的规则"""
        if 0 <= index < len(self.rule_frames):
            # 获取要复制的规则数据
            original_rule = self.rule_frames[index]
            # 获取完整的规则配置，包括选中的字段
            rule_data = original_rule.get_rule()
            # 添加选中的字段信息
            rule_data['selected_fields'] = original_rule.selected_fields.copy()
            # 创建新的规则框架，传入现有规则数据
            self.add_rule(rule_data)
        
    def remove_rule(self, index):
        """删除指定索引的抽选规则"""
        if len(self.rule_frames) > 1:
            rule_frame = self.rule_frames.pop(index)
            rule_frame.destroy()
            # 更新剩余规则的标题和索引
            for i, frame in enumerate(self.rule_frames):
                frame.update_index(i)
        else:
            messagebox.showinfo("提示", "至少需要保留一个抽选规则")
    
    def update_rule_frames(self):
        """更新所有规则框架的列元数据"""
        if self.data_handler:
            column_metadata = self.data_handler.get_column_metadata()
            # 清空现有规则框架
            for frame in self.rule_frames:
                frame.destroy()
            self.rule_frames.clear()
            # 添加新的规则框架
            self.add_rule()
        
    def show_rule_section(self, show=True):
        """显示或隐藏抽选规则区域"""
        if show:
            # 使用fill=tk.BOTH和expand=True确保规则区域能垂直扩展，跟随窗口大小调整
            self.rules_section.pack(fill=tk.BOTH, expand=True, pady=10)
        else:
            self.rules_section.pack_forget()
        
        # 更新抽选按钮状态
        if self.select_button:
            if show and self.data_handler:
                self.select_button.config(state=tk.NORMAL)
            else:
                self.select_button.config(state=tk.DISABLED)
        
    def remove_last_rule(self):
        """删除最后一个抽选规则"""
        if len(self.rule_frames) > 1:
            self.remove_rule(len(self.rule_frames) - 1)
        else:
            messagebox.showinfo("提示", "至少需要保留一个抽选规则")
        
    def get_rules(self):
        """获取所有抽选规则"""
        rules = []
        for frame in self.rule_frames:
            rule = frame.get_rule()
            if rule['count'] > 0:
                rules.append(rule)
        return rules
    
    def add_file_selection_buttons(self, container):
        """添加文件选择按钮"""
        file_section = ttk.LabelFrame(container, text="文件管理")
        file_section.pack(fill=tk.X, pady=15, padx=10, ipady=10)
        
        # 文件选择按钮 - 使用primary样式
        self.select_file_btn = ttk.Button(
            file_section, 
            text="选择Excel文件", 
            command=self.select_file,
            width=15,
            bootstyle="primary"
        )
        self.select_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 预览数据按钮 - 使用secondary样式
        self.preview_btn = ttk.Button(
            file_section, 
            text="预览数据", 
            command=self.preview_data,
            width=15,
            bootstyle="secondary"
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        # 数据状态标签 - 使用ttkbootstrap的样式
        self.data_status_var = tk.StringVar(value="未加载数据")
        self.data_status_label = ttk.Label(
            file_section, 
            textvariable=self.data_status_var,
            bootstyle="danger"
        )
        self.data_status_label.pack(side=tk.RIGHT, padx=5)
        
    def select_file(self):
        """选择Excel文件"""
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls")],
            initialdir=str(BASE_DIR / "data")
        )
        
        if file_path:
            try:
                # 创建临时数据处理器用于预览
                temp_handler = DataHandler(file_path)
                
                # 显示数据预览窗口
                preview_window = DataPreviewWindow(self.root, temp_handler, file_path)
                self.root.wait_window(preview_window.window)
                
                # 如果用户确认，使用该数据处理器
                if preview_window.get_result():
                    self.load_data(temp_handler, file_path)
                else:
                    # 用户取消，不加载数据
                    messagebox.showinfo("提示", "已取消数据加载")
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {e}")
    
    def preview_data(self):
        """预览当前数据"""
        if self.data_handler:
            preview_window = DataPreviewWindow(self.root, self.data_handler, self.current_file_path)
            self.root.wait_window(preview_window.window)
        else:
            messagebox.showwarning("提示", "请先选择并加载Excel文件")
    
    def load_data(self, data_handler, file_path):
        """加载数据并初始化抽选器"""
        self.data_handler = data_handler
        self.current_file_path = file_path
        self.selector = StudentSelector(self.data_handler)
        
        # 更新状态标签
        self.data_status_var.set(f"已加载数据: {file_path}")
        self.data_status_label.config(foreground="green")
        
        # 显示抽选规则区域
        self.show_rule_section(True)
        
        # 更新规则框架
        self.update_rule_frames()
        
        # 显示成功信息
        messagebox.showinfo("提示", f"成功加载数据，共{len(data_handler.df)}条记录")
        
    def init_result_tab(self):
        """初始化抽选结果选项卡"""
        # 创建主容器
        main_container = ttk.Frame(self.result_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 抽选信息区域 - 使用ttkbootstrap样式
        info_frame = ttk.LabelFrame(main_container, text="抽选基本信息")
        info_frame.pack(fill=tk.X, pady=10, padx=10, ipady=10)
        
        self.info_text = tk.Text(info_frame, height=8, font=("Microsoft YaHei", 10), bg="#f0f8ff", fg="#000000", relief="flat")
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.info_text.config(state=tk.DISABLED)
        
        # 抽选名单区域 - 使用ttkbootstrap样式
        self.result_frame_container = ttk.LabelFrame(main_container, text="抽选名单")
        self.result_frame_container.pack(fill=tk.BOTH, expand=True, pady=10, padx=10, ipady=10)
        
        # 创建带垂直滚动条的画布，用于解决多规则结果过长问题
        scrollable_container = ttk.Frame(self.result_frame_container)
        scrollable_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(scrollable_container, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建画布
        canvas = tk.Canvas(scrollable_container, yscrollcommand=v_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.config(command=canvas.yview)
        
        # 创建内部框架放置所有结果内容
        self.results_inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.results_inner_frame, anchor=tk.NW, tags="results_content")
        
        # 绑定内部框架大小变化事件，更新滚动区域
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.results_inner_frame.bind("<Configure>", update_scroll_region)
        
        # 绑定画布大小变化事件，更新内部框架宽度，确保规则容器能自适应边框
        def update_canvas_window_width(event):
            # 获取画布当前宽度，减去右边框宽度（约2像素）
            canvas_width = event.width - 2
            # 更新内部框架宽度，使其与画布宽度一致
            canvas.itemconfig("results_content", width=canvas_width)
        
        canvas.bind("<Configure>", update_canvas_window_width)
        
        # 初始化表格容器，表格将在display_result中动态创建
        self.tree_container = ttk.Frame(self.results_inner_frame)
        self.tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 初始化滚动条容器
        self.scrollbar_y = ttk.Scrollbar(self.tree_container, orient=tk.VERTICAL)
        self.scrollbar_x = ttk.Scrollbar(self.tree_container, orient=tk.HORIZONTAL)
        
    def perform_selection(self):
        """执行抽选操作"""
        # 检查是否已加载数据
        if not self.data_handler or not self.selector:
            messagebox.showwarning("提示", "请先选择并加载Excel文件")
            return
            
        try:
            # 获取抽选规则
            rules = self.get_rules()
            if not rules:
                messagebox.showwarning("提示", "请至少设置一个有效的抽选规则")
                return
            
            # 验证每个规则的抽选人数
            for i, rule in enumerate(rules):
                if rule['count'] <= 0:
                    messagebox.showwarning("提示", f"规则 {i+1} 的抽选人数必须大于0")
                    return
                if rule['count'] > 100:  # 设置合理的最大值限制
                    messagebox.showwarning("提示", f"规则 {i+1} 的抽选人数建议不超过100")
            
            # 检测重复规则
            duplicate_rules = self._detect_duplicate_rules(rules)
            if duplicate_rules:
                # 构建重复规则提示信息
                msg = "检测到重复抽选规则，请调整后重试：\n\n"
                for i, duplicate in enumerate(duplicate_rules):
                    # 格式化重复规则
                    rule_nums = [str(num+1) for num in duplicate['rule_nums']]
                    filters_desc = ", ".join([f"{k}={v}" for k, v in duplicate['filters'].items()])
                    msg += f"{i+1}. 规则 {', '.join(rule_nums)}：筛选条件重复\n"
                    msg += f"   重复条件：{filters_desc}\n"
                    msg += f"   修改建议：合并或修改这些规则的筛选条件\n\n"
                messagebox.showwarning("规则重复提示", msg)
                return
            
            # 获取种子
            seed_str = self.seed_var.get().strip()
            seed = None
            if seed_str:
                try:
                    seed = int(seed_str)
                except ValueError:
                    messagebox.showwarning("提示", "种子值必须是整数")
                    return
            
            # 执行抽选
            result = self.selector.select_by_rules(rules, seed)
            
            # 显示结果
            self.display_result(result)
            
            # 切换到结果选项卡
            self.notebook.select(self.result_frame)
            
        except ValueError as e:
            # 显示友好的错误信息
            messagebox.showerror("抽选失败", str(e))
        except Exception as e:
            # 显示更通用的错误信息
            error_msg = str(e)
            # 优化错误信息显示
            if "班委人数不足" in error_msg:
                messagebox.showerror("抽选失败", error_msg)
            elif "候选人数不足" in error_msg:
                messagebox.showerror("抽选失败", error_msg)
            else:
                messagebox.showerror("抽选失败", f"抽选过程中发生错误: {error_msg}")
    
    def _detect_duplicate_rules(self, rules):
        """
        检测重复的抽选规则
        
        Args:
            rules: 抽选规则列表
            
        Returns:
            重复规则列表，每个元素包含重复的规则编号和重复的筛选条件
        """
        # 按筛选条件分组规则
        rule_groups = {}
        
        for i, rule in enumerate(rules):
            # 提取筛选条件，作为分组键
            filters = tuple(sorted(rule.get('filters', {}).items()))
            if filters not in rule_groups:
                rule_groups[filters] = []
            rule_groups[filters].append(i)
        
        # 提取重复规则组（包含2个或以上规则的组）
        duplicate_rules = []
        for filters, rule_nums in rule_groups.items():
            if len(rule_nums) > 1:
                # 转换为字典格式的筛选条件
                filters_dict = dict(filters)
                duplicate_rules.append({
                    'rule_nums': rule_nums,
                    'filters': filters_dict
                })
        
        return duplicate_rules
    
    def display_result(self, result):
        """显示抽选结果"""
        # 清空之前的结果
        self.clear_result()
        
        # 显示抽选信息
        info = f"抽选时间: {format_datetime(result['seed'])}\n"
        info += f"随机种子: {result['seed']}\n\n"
        
        # 显示抽选规则
        info += "抽选规则:\n"
        for i, rule in enumerate(result['rules'], 1):
            rule_desc = f"规则{i}: 抽取{rule['count']}人"
            conditions = []
            
            # 处理新格式规则（包含filters字段）
            if 'filters' in rule and rule['filters']:
                for col, value in rule['filters'].items():
                    conditions.append(f"{col}={value}")
            
            if conditions:
                rule_desc += f" ({', '.join(conditions)})"
            info += f"{rule_desc}\n"
        info += "\n"
        
        # 添加统计信息
        stats = result['stats'].copy()
        stats['total_candidates'] = result['total_candidates']
        info += format_stats(stats)
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)
        
        # 检查是否有规则结果
        if 'rule_results' not in result or not result['rule_results']:
            return
        
        # 创建一个主容器用于存放所有规则结果
        rules_container = ttk.Frame(self.results_inner_frame)
        rules_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 顶部添加合并结果汇总（移到最上层）
        summary_frame = ttk.LabelFrame(rules_container, text="抽选结果汇总")
        summary_frame.pack(fill=tk.X, pady=10, padx=5, ipady=5)
        
        # 显示所有规则合并后的完整名单
        if not result['selected_students'].empty:
            # 获取数据列，添加序号列
            data_columns = list(result['selected_students'].columns)
            columns = ["序号"] + data_columns
            
            # 创建统计信息框架，将文本和按钮放在同一行，与文字平齐
            stats_frame = ttk.Frame(summary_frame)
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # 左侧文本区域
            text_frame = ttk.Frame(stats_frame)
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 显示候选人数和总抽取人数
            total_candidates = result['total_candidates']
            total_selected = len(result['selected_students'])
            ttk.Label(text_frame, text=f"候选人数: {total_candidates}人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            ttk.Label(text_frame, text=f"实际抽取: {total_selected}人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            
            # 右侧按钮区域，与文本平齐
            btn_frame = ttk.Frame(stats_frame)
            btn_frame.pack(side=tk.RIGHT, padx=5, pady=2)
            
            # 复制学号及姓名按钮
            def copy_summary_id_name():
                # 构建复制内容
                copy_text = ""
                for j, (_, student) in enumerate(result['selected_students'].iterrows(), 1):
                    # 检查是否有学号和姓名字段
                    student_id = student.get('学号', '')
                    name = student.get('姓名', '')
                    copy_text += f"{student_id} {name}\n"
                # 复制到剪贴板
                self.root.clipboard_clear()
                self.root.clipboard_append(copy_text.strip())
                messagebox.showinfo("提示", "学号及姓名已复制到剪贴板")
            
            # 复制全部按钮
            def copy_summary_all():
                # 构建复制内容
                copy_text = ""
                # 添加表头
                copy_text += "\t".join(data_columns) + "\n"
                # 添加数据行
                for _, student in result['selected_students'].iterrows():
                    row_data = [str(student[col]) for col in data_columns]
                    copy_text += "\t".join(row_data) + "\n"
                # 复制到剪贴板
                self.root.clipboard_clear()
                self.root.clipboard_append(copy_text.strip())
                messagebox.showinfo("提示", "全部数据已复制到剪贴板")
            
            # 添加按钮，与文本平齐
            ttk.Button(btn_frame, text="复制学号及姓名", command=copy_summary_id_name, bootstyle="primary").pack(side=tk.RIGHT, padx=5)
            ttk.Button(btn_frame, text="复制全部", command=copy_summary_all, bootstyle="secondary").pack(side=tk.RIGHT, padx=5)
            
            # 创建汇总表格容器
            summary_table_frame = ttk.Frame(summary_frame)
            summary_table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # 创建树视图
            summary_tree = ttk.Treeview(summary_table_frame, columns=columns, show="headings")
            
            # 创建滚动条
            summary_y_scrollbar = ttk.Scrollbar(summary_table_frame, orient=tk.VERTICAL, command=summary_tree.yview)
            summary_x_scrollbar = ttk.Scrollbar(summary_table_frame, orient=tk.HORIZONTAL, command=summary_tree.xview)
            summary_tree.configure(yscrollcommand=summary_y_scrollbar.set, xscrollcommand=summary_x_scrollbar.set)
            
            # 设置列宽和标题
            for col in columns:
                summary_tree.heading(col, text=col, anchor=tk.CENTER)
                summary_tree.column(col, width=100, anchor=tk.CENTER)
            
            # 布局
            summary_tree.grid(row=0, column=0, sticky=tk.NSEW)
            summary_y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
            summary_x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
            
            # 设置网格权重
            summary_table_frame.grid_rowconfigure(0, weight=1)
            summary_table_frame.grid_columnconfigure(0, weight=1)
            
            # 显示合并后的抽选名单
            for j, (_, student) in enumerate(result['selected_students'].iterrows(), 1):
                # 动态生成行数据，确保只包含表格列中有的字段
                row_values = [j] + [student[col] for col in data_columns]
                summary_tree.insert("", tk.END, values=row_values)
        else:
            # 没有选中学生的情况
            # 创建统计信息框架，显示候选人数
            stats_frame = ttk.Frame(summary_frame)
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # 显示候选人数
            total_candidates = result['total_candidates']
            ttk.Label(stats_frame, text=f"候选人数: {total_candidates}人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            ttk.Label(stats_frame, text="实际抽取: 0人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            
            # 显示未抽选到学生的提示
            ttk.Label(summary_frame, text="未抽选到符合条件的学生", foreground='gray').pack(fill=tk.BOTH, expand=True, pady=20)
        
        # 遍历每个规则结果，创建独立的展示模块
        for i, rule_result in enumerate(result['rule_results'], 1):
            rule = rule_result['rule']
            selected_students = rule_result['selected_students']
            actual_count = rule_result['actual_count']
            total_candidates = rule_result['total_candidates']
            skipped = rule_result['skipped']
            skip_reason = rule_result['skip_reason']
            
            # 创建规则结果模块容器
            rule_frame = ttk.LabelFrame(rules_container, text=f"规则 {i} 结果")
            rule_frame.pack(fill=tk.X, pady=10, padx=5, ipady=5)
            
            # 创建规则描述标签
            rule_desc = f"抽取{rule['count']}人"
            conditions = []
            if 'filters' in rule and rule['filters']:
                for col, value in rule['filters'].items():
                    conditions.append(f"{col}={value}")
            if conditions:
                rule_desc += f" ({', '.join(conditions)})"
            
            # 创建统计信息框架，将文本和按钮放在同一行
            stats_frame = ttk.Frame(rule_frame)
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # 左侧文本区域
            text_frame = ttk.Frame(stats_frame)
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 规则描述
            ttk.Label(text_frame, text=f"规则描述: {rule_desc}", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            
            if skipped:
                # 如果规则被跳过，显示跳过原因
                ttk.Label(text_frame, text=f"状态: 跳过 - {skip_reason}", foreground='red').pack(anchor=tk.W, padx=5, pady=2)
            else:
                # 显示抽选统计
                ttk.Label(text_frame, text=f"候选人数: {total_candidates}人").pack(anchor=tk.W, padx=5, pady=2)
                ttk.Label(text_frame, text=f"实际抽取: {actual_count}人").pack(anchor=tk.W, padx=5, pady=2)
            
            # 右侧按钮区域，与文本平齐
            if not skipped and not selected_students.empty:
                btn_frame = ttk.Frame(stats_frame)
                btn_frame.pack(side=tk.RIGHT, padx=5, pady=2)
                
                # 获取数据列，添加序号列
                data_columns = list(selected_students.columns)
                columns = ["序号"] + data_columns
                
                # 修复闭包问题：使用lambda函数传递参数，确保每个按钮引用正确的selected_students和data_columns
                # 复制学号及姓名按钮
                def create_copy_id_name_func(students):
                    def copy_rule_id_name():
                        # 构建复制内容
                        copy_text = ""
                        for j, (_, student) in enumerate(students.iterrows(), 1):
                            # 检查是否有学号和姓名字段
                            student_id = student.get('学号', '')
                            name = student.get('姓名', '')
                            copy_text += f"{student_id} {name}\n"
                        # 复制到剪贴板
                        self.root.clipboard_clear()
                        self.root.clipboard_append(copy_text.strip())
                        messagebox.showinfo("提示", "学号及姓名已复制到剪贴板")
                    return copy_rule_id_name
                
                # 复制全部按钮
                def create_copy_all_func(students, cols):
                    def copy_rule_all():
                        # 构建复制内容
                        copy_text = ""
                        # 添加表头
                        copy_text += "\t".join(cols) + "\n"
                        # 添加数据行
                        for _, student in students.iterrows():
                            row_data = [str(student[col]) for col in cols]
                            copy_text += "\t".join(row_data) + "\n"
                        # 复制到剪贴板
                        self.root.clipboard_clear()
                        self.root.clipboard_append(copy_text.strip())
                        messagebox.showinfo("提示", "全部数据已复制到剪贴板")
                    return copy_rule_all
                
                # 添加按钮，使用工厂函数创建闭包，与文本平齐
                ttk.Button(btn_frame, text="复制学号及姓名", command=create_copy_id_name_func(selected_students), bootstyle="primary").pack(side=tk.RIGHT, padx=5)
                ttk.Button(btn_frame, text="复制全部", command=create_copy_all_func(selected_students, data_columns), bootstyle="secondary").pack(side=tk.RIGHT, padx=5)
            
            # 创建表格容器
            table_frame = ttk.Frame(rule_frame)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # 如果规则没有被跳过且有选中的学生，创建表格
            if not skipped and not selected_students.empty:
                # 获取数据列，添加序号列
                data_columns = list(selected_students.columns)
                columns = ["序号"] + data_columns
                
                # 创建树视图
                tree = ttk.Treeview(table_frame, columns=columns, show="headings")
                
                # 创建滚动条
                y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
                x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
                tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
                
                # 设置列宽和标题
                for col in columns:
                    tree.heading(col, text=col, anchor=tk.CENTER)
                    tree.column(col, width=100, anchor=tk.CENTER)
                
                # 布局
                tree.grid(row=0, column=0, sticky=tk.NSEW)
                y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
                x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
                
                # 设置网格权重
                table_frame.grid_rowconfigure(0, weight=1)
                table_frame.grid_columnconfigure(0, weight=1)
                
                # 显示抽选名单
                for j, (_, student) in enumerate(selected_students.iterrows(), 1):
                    # 动态生成行数据，确保只包含表格列中有的字段
                    row_values = [j] + [student[col] for col in data_columns]
                    tree.insert("", tk.END, values=row_values)
            elif not skipped:
                # 没有选中学生的情况
                ttk.Label(table_frame, text="未抽选到符合条件的学生", foreground='gray').pack(fill=tk.BOTH, expand=True, pady=20)
            else:
                # 规则被跳过的情况
                ttk.Label(table_frame, text=f"规则被跳过: {skip_reason}", foreground='red').pack(fill=tk.BOTH, expand=True, pady=20)
    
    def clear_result(self):
        """清空结果显示"""
        # 清空信息文本
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)
        
        # 清空抽选名单区域的所有子组件
        for widget in self.result_frame_container.winfo_children():
            widget.destroy()
        
        # 重新创建完整的滚动画布结构
        # 创建带垂直滚动条的画布，用于解决多规则结果过长问题
        scrollable_container = ttk.Frame(self.result_frame_container)
        scrollable_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(scrollable_container, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建画布
        canvas = tk.Canvas(scrollable_container, yscrollcommand=v_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.config(command=canvas.yview)
        
        # 创建内部框架放置所有结果内容
        self.results_inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.results_inner_frame, anchor=tk.NW, tags="results_content")
        
        # 绑定内部框架大小变化事件，更新滚动区域
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.results_inner_frame.bind("<Configure>", update_scroll_region)
        
        # 绑定画布大小变化事件，更新内部框架宽度，确保规则容器能自适应边框
        def update_canvas_window_width(event):
            # 获取画布当前宽度，减去右边框宽度（约2像素）
            canvas_width = event.width - 2
            # 更新内部框架宽度，使其与画布宽度一致
            canvas.itemconfig("results_content", width=canvas_width)
        
        canvas.bind("<Configure>", update_canvas_window_width)
        
        # 重新添加表格容器，注意添加到results_inner_frame中
        self.tree_container = ttk.Frame(self.results_inner_frame)
        self.tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 重新添加滚动条容器
        self.scrollbar_y = ttk.Scrollbar(self.tree_container, orient=tk.VERTICAL)
        self.scrollbar_x = ttk.Scrollbar(self.tree_container, orient=tk.HORIZONTAL)
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()
