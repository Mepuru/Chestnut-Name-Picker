#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块，负责应用程序主界面
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from src.data_handler import DataHandler
from src.selector import StudentSelector
from src.utils import format_datetime, format_stats, create_scrollable_frame
from src.styles import configure_styles
from src.ui.rule_frame import RuleFrame
from src.ui.preview_window import DataPreviewWindow

BASE_DIR = Path(__file__).parent.parent.parent


class ClassSelectorUI:
    """ChestNut名单抽选工具GUI界面"""
    
    def __init__(self):
        """初始化GUI界面"""
        self.root = ttk.Window(themename="litera")
        self.root.title("ChestNut名单抽选工具V1.0")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        self._setup_icon()
        self._setup_styles()
        self._init_state()
        self.create_widgets()
    
    def _setup_icon(self):
        """设置窗口图标"""
        try:
            self.icon_path = str(BASE_DIR / "assets" / "LS20260513150828.png")
            img = Image.open(self.icon_path)
            
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
            self.app_icons = [ImageTk.PhotoImage(img.resize(s, Image.Resampling.LANCZOS)) for s in icon_sizes]
            
            self.root.iconphoto(True, *self.app_icons)
        except Exception as e:
            print(f"设置图标失败: {e}")
    
    def _setup_styles(self):
        """设置样式"""
        self.style = ttk.Style()
        configure_styles(self.style)
    
    def _init_state(self):
        """初始化状态变量"""
        self.data_handler = None
        self.selector = None
        self.current_file_path = None
        self.rule_frames = []
    
    def create_widgets(self):
        """创建GUI组件"""
        self.notebook = ttk.Notebook(self.root, style="Tab.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.condition_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.condition_frame, text="抽选条件")
        
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="抽选结果")
        
        self.init_condition_tab()
        self.init_result_tab()
    
    def init_condition_tab(self):
        """初始化抽选条件选项卡"""
        main_container = ttk.Frame(self.condition_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._add_file_selection_buttons(main_container)
        self._add_seed_section(main_container)
        self._add_rules_section(main_container)
        
        self.show_rule_section(False)
    
    def _add_file_selection_buttons(self, container):
        """添加文件选择按钮"""
        file_section = ttk.LabelFrame(container, text="文件管理")
        file_section.pack(fill=tk.X, pady=15, padx=10, ipady=10)
        
        self.select_file_btn = ttk.Button(
            file_section, text="选择Excel文件", command=self.select_file,
            width=15, bootstyle="primary"
        )
        self.select_file_btn.pack(side=tk.LEFT, padx=5)
        
        self.preview_btn = ttk.Button(
            file_section, text="预览数据", command=self.preview_data,
            width=15, bootstyle="secondary"
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.data_status_var = tk.StringVar(value="未加载数据")
        self.data_status_label = ttk.Label(file_section, textvariable=self.data_status_var, bootstyle="danger")
        self.data_status_label.pack(side=tk.RIGHT, padx=5)
    
    def _add_seed_section(self, container):
        """添加种子设置区域"""
        seed_frame = ttk.LabelFrame(container, text="随机种子")
        seed_frame.pack(fill=tk.X, pady=15, padx=10, ipady=10)
        
        seed_container = ttk.Frame(seed_frame)
        seed_container.pack(fill=tk.X)
        
        ttk.Label(seed_container, text="种子值（留空则使用当前时间）:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.seed_var = tk.StringVar(value="")
        self.seed_entry = ttk.Entry(seed_container, textvariable=self.seed_var, width=30)
        self.seed_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
    
    def _add_rules_section(self, container):
        """添加规则管理区域"""
        self.rules_section = ttk.Frame(container)
        
        rules_header = ttk.Frame(self.rules_section)
        rules_header.pack(fill=tk.X, pady=10)
        
        ttk.Label(rules_header, text="抽选规则设置", style="Header.TLabel").pack(side=tk.LEFT, anchor=tk.W)
        
        self.select_button = ttk.Button(
            rules_header, text="开始抽选", command=self.perform_selection,
            width=12, state=tk.DISABLED, bootstyle="success"
        )
        self.select_button.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            rules_header, text="添加规则", command=self.add_rule, bootstyle="primary"
        ).pack(side=tk.RIGHT, padx=5)
        
        # 规则容器（带滚动条）
        rules_scroll_frame = ttk.Frame(self.rules_section)
        rules_scroll_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        canvas = tk.Canvas(rules_scroll_frame)
        scrollbar = ttk.Scrollbar(rules_scroll_frame, orient="vertical", command=canvas.yview)
        self.rules_container = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def update_canvas_width():
            scrollbar_width = scrollbar.winfo_width()
            canvas_width = rules_scroll_frame.winfo_width() - scrollbar_width
            canvas.itemconfig("rules_container", width=canvas_width)
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas.create_window((0, 0), window=self.rules_container, anchor="nw", tags="rules_container")
        
        def on_configure(event):
            update_canvas_width()
        
        rules_scroll_frame.bind("<Configure>", on_configure)
        self.rules_container.bind("<Configure>", on_configure)
        update_canvas_width()
    
    def add_rule(self, existing_rule_data=None):
        """添加一个抽选规则"""
        index = len(self.rule_frames)
        column_metadata = self.data_handler.get_column_metadata() if self.data_handler else {}
        rule_frame = RuleFrame(self.rules_container, index, self.remove_rule, self.copy_rule, column_metadata)
        
        if existing_rule_data:
            rule_frame.count_var.set(str(existing_rule_data['count']))
            rule_frame.selected_fields = existing_rule_data['selected_fields'].copy()
            rule_frame._generate_filter_widgets()
            for col_name, value in existing_rule_data['filters'].items():
                if col_name in rule_frame.filter_vars:
                    rule_frame.filter_vars[col_name].set(value)
        
        self.rule_frames.append(rule_frame)
    
    def copy_rule(self, index):
        """复制指定索引的规则"""
        if 0 <= index < len(self.rule_frames):
            original_rule = self.rule_frames[index]
            rule_data = original_rule.get_rule()
            rule_data['selected_fields'] = original_rule.selected_fields.copy()
            self.add_rule(rule_data)
    
    def remove_rule(self, index):
        """删除指定索引的抽选规则"""
        if len(self.rule_frames) > 1:
            rule_frame = self.rule_frames.pop(index)
            rule_frame.destroy()
            for i, frame in enumerate(self.rule_frames):
                frame.update_index(i)
        else:
            messagebox.showinfo("提示", "至少需要保留一个抽选规则")
    
    def update_rule_frames(self):
        """更新所有规则框架的列元数据"""
        if self.data_handler:
            for frame in self.rule_frames:
                frame.destroy()
            self.rule_frames.clear()
            self.add_rule()
    
    def show_rule_section(self, show=True):
        """显示或隐藏抽选规则区域"""
        if show:
            self.rules_section.pack(fill=tk.BOTH, expand=True, pady=10)
        else:
            self.rules_section.pack_forget()
        
        if self.select_button:
            if show and self.data_handler:
                self.select_button.config(state=tk.NORMAL)
            else:
                self.select_button.config(state=tk.DISABLED)
    
    def get_rules(self):
        """获取所有抽选规则"""
        return [frame.get_rule() for frame in self.rule_frames if frame.get_rule()['count'] > 0]
    
    def select_file(self):
        """选择Excel文件"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls")],
            initialdir=str(BASE_DIR / "data")
        )
        
        if file_path:
            try:
                temp_handler = DataHandler(file_path)
                preview_window = DataPreviewWindow(self.root, temp_handler, file_path)
                self.root.wait_window(preview_window.window)
                
                if preview_window.get_result():
                    self.load_data(temp_handler, file_path)
                else:
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
        
        self.data_status_var.set(f"已加载数据: {file_path}")
        self.data_status_label.config(foreground="green")
        
        self.show_rule_section(True)
        self.update_rule_frames()
        
        messagebox.showinfo("提示", f"成功加载数据，共{len(data_handler.df)}条记录")
    
    def init_result_tab(self):
        """初始化抽选结果选项卡"""
        main_container = ttk.Frame(self.result_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_frame = ttk.LabelFrame(main_container, text="抽选基本信息")
        info_frame.pack(fill=tk.X, pady=10, padx=10, ipady=10)
        
        self.info_text = tk.Text(info_frame, height=8, font=("Microsoft YaHei", 10), bg="#f0f8ff", fg="#000000", relief="flat")
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.info_text.config(state=tk.DISABLED)
        
        self.result_frame_container = ttk.LabelFrame(main_container, text="抽选名单")
        self.result_frame_container.pack(fill=tk.BOTH, expand=True, pady=10, padx=10, ipady=10)
        
        canvas, inner_frame = create_scrollable_frame(self.result_frame_container, "results_content")
        self.results_inner_frame = inner_frame
        
        self.tree_container = ttk.Frame(self.results_inner_frame)
        self.tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.scrollbar_y = ttk.Scrollbar(self.tree_container, orient=tk.VERTICAL)
        self.scrollbar_x = ttk.Scrollbar(self.tree_container, orient=tk.HORIZONTAL)
    
    def perform_selection(self):
        """执行抽选操作"""
        if not self.data_handler or not self.selector:
            messagebox.showwarning("提示", "请先选择并加载Excel文件")
            return
        
        try:
            rules = self.get_rules()
            if not rules:
                messagebox.showwarning("提示", "请至少设置一个有效的抽选规则")
                return
            
            for i, rule in enumerate(rules):
                if rule['count'] <= 0:
                    messagebox.showwarning("提示", f"规则 {i+1} 的抽选人数必须大于0")
                    return
                if rule['count'] > 100:
                    messagebox.showwarning("提示", f"规则 {i+1} 的抽选人数建议不超过100")
            
            duplicate_rules = self._detect_duplicate_rules(rules)
            if duplicate_rules:
                msg = "检测到重复抽选规则，请调整后重试：\n\n"
                for i, duplicate in enumerate(duplicate_rules):
                    rule_nums = [str(num+1) for num in duplicate['rule_nums']]
                    filters_desc = ", ".join([f"{k}={v}" for k, v in duplicate['filters'].items()])
                    msg += f"{i+1}. 规则 {', '.join(rule_nums)}：筛选条件重复\n"
                    msg += f"   重复条件：{filters_desc}\n"
                    msg += f"   修改建议：合并或修改这些规则的筛选条件\n\n"
                messagebox.showwarning("规则重复提示", msg)
                return
            
            seed_str = self.seed_var.get().strip()
            seed = None
            if seed_str:
                try:
                    seed = int(seed_str)
                except ValueError:
                    messagebox.showwarning("提示", "种子值必须是整数")
                    return
            
            result = self.selector.select_by_rules(rules, seed)
            self.display_result(result)
            self.notebook.select(self.result_frame)
            
        except ValueError as e:
            messagebox.showerror("抽选失败", str(e))
        except Exception as e:
            messagebox.showerror("抽选失败", f"抽选过程中发生错误: {str(e)}")
    
    def _detect_duplicate_rules(self, rules):
        """检测重复的抽选规则"""
        rule_groups = {}
        for i, rule in enumerate(rules):
            filters = tuple(sorted(rule.get('filters', {}).items()))
            if filters not in rule_groups:
                rule_groups[filters] = []
            rule_groups[filters].append(i)
        
        return [{'rule_nums': nums, 'filters': dict(filters)} 
                for filters, nums in rule_groups.items() if len(nums) > 1]
    
    def display_result(self, result):
        """显示抽选结果"""
        self.clear_result()
        
        info = f"抽选时间: {format_datetime(result['seed'])}\n"
        info += f"随机种子: {result['seed']}\n\n"
        info += "抽选规则:\n"
        
        for i, rule in enumerate(result['rules'], 1):
            rule_desc = f"规则{i}: 抽取{rule['count']}人"
            conditions = [f"{col}={val}" for col, val in rule.get('filters', {}).items()]
            if conditions:
                rule_desc += f" ({', '.join(conditions)})"
            info += f"{rule_desc}\n"
        
        info += "\n"
        stats = result['stats'].copy()
        stats['total_candidates'] = result['total_candidates']
        info += format_stats(stats)
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)
        
        if 'rule_results' not in result or not result['rule_results']:
            return
        
        rules_container = ttk.Frame(self.results_inner_frame)
        rules_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._display_summary(rules_container, result)
        self._display_rule_results(rules_container, result)
    
    def _display_summary(self, container, result):
        """显示汇总结果"""
        summary_frame = ttk.LabelFrame(container, text="抽选结果汇总")
        summary_frame.pack(fill=tk.X, pady=10, padx=5, ipady=5)
        
        if not result['selected_students'].empty:
            data_columns = list(result['selected_students'].columns)
            columns = ["序号"] + data_columns
            
            stats_frame = ttk.Frame(summary_frame)
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            text_frame = ttk.Frame(stats_frame)
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            ttk.Label(text_frame, text=f"候选人数: {result['total_candidates']}人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            ttk.Label(text_frame, text=f"实际抽取: {len(result['selected_students'])}人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            
            btn_frame = ttk.Frame(stats_frame)
            btn_frame.pack(side=tk.RIGHT, padx=5, pady=2)
            
            ttk.Button(btn_frame, text="复制学号及姓名", command=lambda: self._copy_id_name(result['selected_students']), bootstyle="primary").pack(side=tk.RIGHT, padx=5)
            ttk.Button(btn_frame, text="复制全部", command=lambda: self._copy_all(result['selected_students'], data_columns), bootstyle="secondary").pack(side=tk.RIGHT, padx=5)
            
            summary_table_frame = ttk.Frame(summary_frame)
            summary_table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            summary_tree = ttk.Treeview(summary_table_frame, columns=columns, show="headings")
            summary_y_scrollbar = ttk.Scrollbar(summary_table_frame, orient=tk.VERTICAL, command=summary_tree.yview)
            summary_x_scrollbar = ttk.Scrollbar(summary_table_frame, orient=tk.HORIZONTAL, command=summary_tree.xview)
            summary_tree.configure(yscrollcommand=summary_y_scrollbar.set, xscrollcommand=summary_x_scrollbar.set)
            
            for col in columns:
                summary_tree.heading(col, text=col, anchor=tk.CENTER)
                summary_tree.column(col, width=100, anchor=tk.CENTER)
            
            summary_tree.grid(row=0, column=0, sticky=tk.NSEW)
            summary_y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
            summary_x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
            
            summary_table_frame.grid_rowconfigure(0, weight=1)
            summary_table_frame.grid_columnconfigure(0, weight=1)
            
            for j, (_, student) in enumerate(result['selected_students'].iterrows(), 1):
                row_values = [j] + [student[col] for col in data_columns]
                summary_tree.insert("", tk.END, values=row_values)
        else:
            stats_frame = ttk.Frame(summary_frame)
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(stats_frame, text=f"候选人数: {result['total_candidates']}人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            ttk.Label(stats_frame, text="实际抽取: 0人", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            ttk.Label(summary_frame, text="未抽选到符合条件的学生", foreground='gray').pack(fill=tk.BOTH, expand=True, pady=20)
    
    def _display_rule_results(self, container, result):
        """显示各规则结果"""
        for i, rule_result in enumerate(result['rule_results'], 1):
            rule = rule_result['rule']
            selected_students = rule_result['selected_students']
            skipped = rule_result['skipped']
            
            rule_frame = ttk.LabelFrame(container, text=f"规则 {i} 结果")
            rule_frame.pack(fill=tk.X, pady=10, padx=5, ipady=5)
            
            rule_desc = f"抽取{rule['count']}人"
            conditions = [f"{col}={val}" for col, val in rule.get('filters', {}).items()]
            if conditions:
                rule_desc += f" ({', '.join(conditions)})"
            
            stats_frame = ttk.Frame(rule_frame)
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            text_frame = ttk.Frame(stats_frame)
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            ttk.Label(text_frame, text=f"规则描述: {rule_desc}", font=('Microsoft YaHei', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=2)
            
            if skipped:
                ttk.Label(text_frame, text=f"状态: 跳过 - {rule_result['skip_reason']}", foreground='red').pack(anchor=tk.W, padx=5, pady=2)
            else:
                ttk.Label(text_frame, text=f"候选人数: {rule_result['total_candidates']}人").pack(anchor=tk.W, padx=5, pady=2)
                ttk.Label(text_frame, text=f"实际抽取: {rule_result['actual_count']}人").pack(anchor=tk.W, padx=5, pady=2)
            
            if not skipped and not selected_students.empty:
                btn_frame = ttk.Frame(stats_frame)
                btn_frame.pack(side=tk.RIGHT, padx=5, pady=2)
                
                data_columns = list(selected_students.columns)
                ttk.Button(btn_frame, text="复制学号及姓名", command=lambda s=selected_students: self._copy_id_name(s), bootstyle="primary").pack(side=tk.RIGHT, padx=5)
                ttk.Button(btn_frame, text="复制全部", command=lambda s=selected_students, c=data_columns: self._copy_all(s, c), bootstyle="secondary").pack(side=tk.RIGHT, padx=5)
            
            table_frame = ttk.Frame(rule_frame)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            if not skipped and not selected_students.empty:
                data_columns = list(selected_students.columns)
                columns = ["序号"] + data_columns
                
                tree = ttk.Treeview(table_frame, columns=columns, show="headings")
                y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
                x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
                tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
                
                for col in columns:
                    tree.heading(col, text=col, anchor=tk.CENTER)
                    tree.column(col, width=100, anchor=tk.CENTER)
                
                tree.grid(row=0, column=0, sticky=tk.NSEW)
                y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
                x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
                
                table_frame.grid_rowconfigure(0, weight=1)
                table_frame.grid_columnconfigure(0, weight=1)
                
                for j, (_, student) in enumerate(selected_students.iterrows(), 1):
                    row_values = [j] + [student[col] for col in data_columns]
                    tree.insert("", tk.END, values=row_values)
            elif not skipped:
                ttk.Label(table_frame, text="未抽选到符合条件的学生", foreground='gray').pack(fill=tk.BOTH, expand=True, pady=20)
            else:
                ttk.Label(table_frame, text=f"规则被跳过: {rule_result['skip_reason']}", foreground='red').pack(fill=tk.BOTH, expand=True, pady=20)
    
    def _copy_id_name(self, students):
        """复制学号及姓名"""
        copy_text = ""
        for _, student in students.iterrows():
            student_id = student.get('学号', '')
            name = student.get('姓名', '')
            copy_text += f"{student_id} {name}\n"
        self.root.clipboard_clear()
        self.root.clipboard_append(copy_text.strip())
        messagebox.showinfo("提示", "学号及姓名已复制到剪贴板")
    
    def _copy_all(self, students, columns):
        """复制全部数据"""
        copy_text = "\t".join(columns) + "\n"
        for _, student in students.iterrows():
            row_data = [str(student[col]) for col in columns]
            copy_text += "\t".join(row_data) + "\n"
        self.root.clipboard_clear()
        self.root.clipboard_append(copy_text.strip())
        messagebox.showinfo("提示", "全部数据已复制到剪贴板")
    
    def clear_result(self):
        """清空结果显示"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)
        
        for widget in self.result_frame_container.winfo_children():
            widget.destroy()
        
        canvas, inner_frame = create_scrollable_frame(self.result_frame_container, "results_content")
        self.results_inner_frame = inner_frame
        
        self.tree_container = ttk.Frame(self.results_inner_frame)
        self.tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.scrollbar_y = ttk.Scrollbar(self.tree_container, orient=tk.VERTICAL)
        self.scrollbar_x = ttk.Scrollbar(self.tree_container, orient=tk.HORIZONTAL)
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()
