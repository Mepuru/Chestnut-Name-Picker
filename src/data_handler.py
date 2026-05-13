#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理模块，负责读取和处理Excel文件中的班级名册数据
"""

import pandas as pd
from typing import Dict, List, Optional, Any


class DataHandler:
    """数据处理类"""
    
    def __init__(self, file_path):
        """
        初始化数据处理器
        
        Args:
            file_path: Excel文件路径
        """
        self.file_path = file_path
        self.df = None
        self.columns = None
        self.column_metadata = None
        self.load_data()
    
    def load_data(self):
        """读取Excel文件数据"""
        try:
            # 读取数据
            self.df = pd.read_excel(self.file_path)
            
            # 确保数据不为空
            if self.df.empty:
                raise ValueError("数据源文件为空")
            
            # 获取列信息
            self.columns = list(self.df.columns)
            
            # 生成列元数据
            self._generate_column_metadata()
            
            print(f"成功读取数据，共{len(self.df)}条记录，包含{len(self.columns)}列")
        except FileNotFoundError:
            raise FileNotFoundError(f"数据源文件不存在: {self.file_path}")
        except PermissionError:
            raise PermissionError(f"无权限访问数据源文件: {self.file_path}")
        except Exception as e:
            raise ValueError(f"读取数据失败: {str(e)}. 请检查文件格式和内容是否正确")
    
    def reload_data(self):
        """重新加载数据，用于刷新数据源"""
        print("正在刷新数据...")
        self.load_data()
    
    def _generate_column_metadata(self):
        """生成列元数据，包括列名、类型和唯一值"""
        self.column_metadata = {}
        for col in self.columns:
            col_data = self.df[col].dropna()
            unique_values = list(col_data.unique())
            # 只保留前20个唯一值，避免过多数据
            if len(unique_values) > 20:
                unique_values = unique_values[:20] + ["..."]
            
            self.column_metadata[col] = {
                'name': col,
                'type': str(self.df[col].dtype),
                'unique_values': unique_values,
                'non_null_count': len(col_data),
                'total_count': len(self.df)
            }
    
    def get_all_data(self):
        """获取所有数据"""
        return self.df.copy()
    
    def get_columns(self):
        """获取列名列表"""
        return self.columns.copy()
    
    def get_column_metadata(self):
        """获取列元数据
        
        Returns:
            列元数据字典，包含每个列的详细信息
        """
        return self.column_metadata.copy()
    
    def filter_data(self, filters: Optional[Dict[str, Any]] = None, **kwargs):
        """
        根据条件筛选数据（动态适配版）
        
        Args:
            filters: 筛选条件字典，键为列名，值为筛选值
            **kwargs: 兼容原有接口的参数
            
        Returns:
            筛选后的数据DataFrame
        """
        filtered_df = self.df.copy()
        
        # 处理filters字典 - 主筛选逻辑
        if filters:
            for col, value in filters.items():
                if col in self.columns and value is not None:
                    # 检查值是否在列的有效值中，不在则返回空结果
                    col_values = self.df[col].dropna().unique()
                    if value in col_values:
                        filtered_df = filtered_df[filtered_df[col] == value]
                    else:
                        # 无效值，返回空结果
                        filtered_df = filtered_df[filtered_df[col] == value]  # 这会返回空DataFrame
        
        return filtered_df
    
    def validate_filters(self, filters: Dict[str, Any], strict: bool = False) -> List[str]:
        """
        验证筛选条件的有效性
        
        Args:
            filters: 筛选条件字典
            strict: 是否严格验证，True时检查值是否在有效值列表中，False时只检查列是否存在
            
        Returns:
            错误信息列表，为空表示验证通过
        """
        errors = []
        
        for col, value in filters.items():
            if col not in self.columns:
                errors.append(f"列 '{col}' 不存在于当前数据源中")
            elif strict:
                # 严格模式下，检查值是否在列的有效值中
                col_values = self.df[col].dropna().unique()
                if value not in col_values:
                    errors.append(f"值 '{value}' 不在列 '{col}' 的有效值列表中")
        
        return errors
    
    def get_statistics(self):
        """
        获取数据统计信息
        
        Returns:
            统计信息字典，包含总人数和各分类列的统计信息
        """
        stats = {'总人数': len(self.df)}
        
        # 遍历所有列，生成统计信息
        for col in self.columns:
            # 计算非空值数量
            non_null_count = self.df[col].notna().sum()
            stats[f'{col}_非空数量'] = non_null_count
            
            # 对分类列生成值分布统计
            unique_values = self.df[col].dropna().unique()
            if len(unique_values) <= 10:  # 只对分类列生成统计
                value_counts = self.df[col].value_counts().to_dict()
                for value, count in value_counts.items():
                    stats[f'{col}_{value}'] = count
        
        return stats
