#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抽选逻辑模块，负责根据条件进行随机抽选
"""

import random
import time
import pandas as pd
from typing import List, Dict, Optional


class StudentSelector:
    """学生抽选类"""
    
    def __init__(self, data_handler):
        """
        初始化抽选器
        
        Args:
            data_handler: 数据处理器实例
        """
        self.data_handler = data_handler
        
    def select_students(self, count: int, gender: Optional[str] = None, 
                       is_class_leader: Optional[str] = None, 
                       is_member: Optional[str] = None, 
                       seed: Optional[int] = None) -> Dict:
        """
        根据条件随机抽选学生（兼容原有接口）
        
        Args:
            count: 抽选人数
            gender: 性别筛选条件（男/女/None）
            is_class_leader: 是否班委筛选条件（是/否/None）
            is_member: 是否团员筛选条件（是/否/None）
            seed: 随机种子，None则使用当前时间戳
            
        Returns:
            抽选结果字典，包含选中的学生和统计信息
        """
        # 构建新格式的规则，使用filters字段
        filters = {}
        if gender is not None:
            filters['性别'] = gender
        if is_class_leader is not None:
            filters['是否班委'] = is_class_leader
        if is_member is not None:
            filters['是否团员'] = is_member
        
        rules = [{
            'count': count,
            'filters': filters
        }]
        return self.select_by_rules(rules, seed)
    
    def select_by_rules(self, rules: List[Dict], seed: Optional[int] = None) -> Dict:
        """
        根据多组规则随机抽选学生（动态适配版）
        
        Args:
            rules: 抽选规则列表，每个规则包含：
                  - count: 抽选人数
                  - filters: 筛选条件字典（可选）
            seed: 随机种子，None则使用当前时间戳
            
        Returns:
            抽选结果字典，包含选中的学生和统计信息
            - selected_students: 所有规则合并后的学生列表
            - rule_results: 每个规则单独的结果列表
            - seed: 随机种子
            - total_candidates: 总候选人数
            - stats: 统计信息
            - rules: 抽选规则列表
        
        Raises:
            ValueError: 当抽选规则无效或候选人数不足时
        """
        if not rules:
            raise ValueError("抽选规则不能为空")
        
        # 验证规则有效性
        self._validate_rules(rules)
        
        # 设置随机种子
        if seed is None:
            seed = int(time.time())
        random.seed(seed)
        
        all_selected = pd.DataFrame()
        all_candidates = 0
        skipped_rules = 0
        rule_results = []  # 保存每个规则单独的结果
        
        for rule in rules:
            # 解析规则，仅支持新格式（filters字段）
            filters = self._parse_rule_filters(rule)
            count = rule.get('count', 0)
            
            # 规则结果字典
            rule_result = {
                'rule': rule,
                'selected_students': pd.DataFrame(),
                'actual_count': 0,
                'total_candidates': 0,
                'skipped': False,
                'skip_reason': None
            }
            
            if count <= 0:
                skipped_rules += 1
                rule_result['skipped'] = True
                rule_result['skip_reason'] = '抽选人数无效'
                rule_results.append(rule_result)
                continue
            
            # 获取筛选后的数据
            filtered_df = self.data_handler.filter_data(filters=filters)
            total_candidates = len(filtered_df)
            all_candidates += total_candidates
            rule_result['total_candidates'] = total_candidates
            
            if total_candidates < count:
                # 构建规则描述
                rule_desc = self._format_rule(rule)
                
                # 检查是否是无效筛选值导致的候选人数不足
                is_invalid_value = False
                for col, value in filters.items():
                    if col in self.data_handler.columns:
                        col_values = self.data_handler.df[col].dropna().unique()
                        if value not in col_values:
                            is_invalid_value = True
                            break
                
                # 单个规则时
                if len(rules) == 1:
                    # 无效筛选值情况，返回空结果（保持向后兼容）
                    if is_invalid_value:
                        print(f"提示: 规则 '{rule_desc}' 包含无效筛选值，返回空结果")
                        # 创建空结果并返回
                        stats = {
                            'selected_count': 0,
                            'selection_ratio': 0
                        }
                        return {
                            'selected_students': pd.DataFrame(),
                            'rule_results': [rule_result],
                            'seed': seed,
                            'total_candidates': 0,
                            'stats': stats,
                            'rules': rules
                        }
                    # 有效条件但候选人数不足的情况，抛出异常
                    else:
                        # 通用情况，移除硬编码字段检查
                        raise ValueError(f"候选人数不足，仅有{total_candidates}人符合条件，无法抽取{count}人")
                
                # 多个规则时，跳过该规则并记录
                print(f"警告: 规则 '{rule_desc}' 候选人数不足，仅有{total_candidates}人符合条件，无法抽取{count}人，已跳过该规则")
                skipped_rules += 1
                rule_result['skipped'] = True
                rule_result['skip_reason'] = f'候选人数不足，仅有{total_candidates}人符合条件'
                rule_results.append(rule_result)
                continue
            
            # 随机抽选
            selected_indices = random.sample(range(total_candidates), count)
            selected_students = filtered_df.iloc[selected_indices]
            
            # 添加到规则结果
            rule_result['selected_students'] = selected_students.copy()
            rule_result['actual_count'] = len(selected_students)
            rule_results.append(rule_result)
            
            # 添加到总结果
            all_selected = pd.concat([all_selected, selected_students], ignore_index=True)
        
        # 检查是否所有规则都被跳过
        if skipped_rules == len(rules):
            raise ValueError("所有抽选规则均无法执行，候选人数不足")
        
        # 去重处理（防止同一学生被多个规则选中）
        if not all_selected.empty:
            # 动态确定主键列，优先使用'学号'，如果不存在则使用第一个列
            primary_key = '学号' if '学号' in all_selected.columns else all_selected.columns[0]
            all_selected = all_selected.drop_duplicates(subset=[primary_key], keep='first')
        
        # 计算统计信息
        stats = self._calculate_stats(all_selected, all_candidates)
        
        # 更新规则结果中的实际选中人数（考虑去重影响）
        for i, rule_result in enumerate(rule_results):
            if not rule_result['skipped']:
                # 计算该规则实际选中的人数（去重后）
                if not rule_result['selected_students'].empty and not all_selected.empty:
                    primary_key = '学号' if '学号' in all_selected.columns else all_selected.columns[0]
                    # 获取该规则选中的学生ID
                    rule_student_ids = set(rule_result['selected_students'][primary_key])
                    # 获取去重后总结果中属于该规则的学生
                    actual_selected = all_selected[all_selected[primary_key].isin(rule_student_ids)]
                    rule_result['actual_count'] = len(actual_selected)
        
        return {
            'selected_students': all_selected,
            'rule_results': rule_results,
            'seed': seed,
            'total_candidates': all_candidates,
            'stats': stats,
            'rules': rules
        }
    
    def _parse_rule_filters(self, rule: Dict) -> Dict:
        """
        解析规则中的筛选条件，仅支持新格式（filters字段）
        
        Args:
            rule: 单个抽选规则
            
        Returns:
            标准格式的筛选条件字典
        """
        # 仅支持包含filters字段的新格式
        return rule.get('filters', {})
    
    def _validate_rules(self, rules: List[Dict]):
        """
        验证抽选规则的有效性
        
        Args:
            rules: 抽选规则列表
            
        Raises:
            ValueError: 当规则无效时
        """
        for i, rule in enumerate(rules):
            # 检查count字段
            if 'count' not in rule:
                raise ValueError(f"规则 {i+1} 缺少必填字段 'count'")
            
            count = rule.get('count', 0)
            if not isinstance(count, int) or count <= 0:
                raise ValueError(f"规则 {i+1} 的 'count' 必须是正整数，当前值: {count}")
            
            # 验证筛选条件（非严格模式，只检查列是否存在）
            filters = self._parse_rule_filters(rule)
            if filters:
                # 只检查列是否存在，不检查值是否有效
                errors = self.data_handler.validate_filters(filters, strict=False)
                if errors:
                    error_msg = f"规则 {i+1} 的筛选条件无效: " + "; ".join(errors)
                    raise ValueError(error_msg)
    
    def _format_rule(self, rule: Dict) -> str:
        """
        格式化规则为可读字符串（支持动态格式）
        
        Args:
            rule: 规则字典
            
        Returns:
            格式化后的规则字符串
        """
        count = rule.get('count', 0)
        filters = self._parse_rule_filters(rule)
        
        if filters:
            conditions = [f"{k}={v}" for k, v in filters.items()]
            return f"抽取{count}人 ({', '.join(conditions)})"
        else:
            return f"抽取{count}人 (无条件)"
    
    def _calculate_stats(self, selected_students, total_candidates) -> Dict:
        """
        计算抽选结果统计信息
        
        Args:
            selected_students: 选中的学生DataFrame
            total_candidates: 候选总人数
            
        Returns:
            统计信息字典，仅包含基础统计
        """
        selected_count = len(selected_students)
        
        # 仅保留基础统计信息
        stats = {
            'selected_count': selected_count,
            'selection_ratio': round(selected_count / total_candidates * 100, 1) if total_candidates > 0 else 0
        }
        
        return stats
