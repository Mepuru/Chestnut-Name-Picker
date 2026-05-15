#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抽选逻辑模块，负责根据条件进行随机抽选
使用纯 Python 实现，无 pandas 依赖
"""

import random
import time
from typing import List, Dict, Optional, Any
from src.data_handler import _DataFrameProxy


class StudentSelector:
    """学生抽选类"""

    def __init__(self, data_handler):
        self.data_handler = data_handler

    def select_students(self, count: int, gender: Optional[str] = None,
                        is_class_leader: Optional[str] = None,
                        is_member: Optional[str] = None,
                        seed: Optional[int] = None) -> Dict:
        """
        根据条件随机抽选学生（兼容原有接口）
        """
        filters = {}
        if gender is not None:
            filters['性别'] = gender
        if is_class_leader is not None:
            filters['是否班委'] = is_class_leader
        if is_member is not None:
            filters['是否团员'] = is_member

        rules = [{'count': count, 'filters': filters}]
        return self.select_by_rules(rules, seed)

    def select_by_rules(self, rules: List[Dict], seed: Optional[int] = None) -> Dict:
        """
        根据多组规则随机抽选学生（动态适配版）
        """
        if not rules:
            raise ValueError("抽选规则不能为空")

        self._validate_rules(rules)

        if seed is None:
            seed = int(time.time())
        random.seed(seed)

        all_selected: List[Dict[str, Any]] = []
        all_candidates = 0
        skipped_rules = 0
        rule_results = []

        for rule in rules:
            filters = self._parse_rule_filters(rule)
            count = rule.get('count', 0)

            rule_result = {
                'rule': rule,
                'selected_students': [],
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

            filtered_data = self.data_handler.filter_data(filters=filters)
            total_candidates = len(filtered_data)
            all_candidates += total_candidates
            rule_result['total_candidates'] = total_candidates

            if total_candidates < count:
                rule_desc = self._format_rule(rule)

                is_invalid_value = False
                for col, value in filters.items():
                    if col in self.data_handler.columns:
                        col_values = set(row[col] for row in self.data_handler._data if row[col] is not None)
                        if value not in col_values:
                            is_invalid_value = True
                            break

                if len(rules) == 1:
                    if is_invalid_value:
                        print(f"提示: 规则 '{rule_desc}' 包含无效筛选值，返回空结果")
                        stats = {'selected_count': 0, 'selection_ratio': 0}
                        return {
                            'selected_students': [],
                            'rule_results': [rule_result],
                            'seed': seed,
                            'total_candidates': 0,
                            'stats': stats,
                            'rules': rules
                        }
                    else:
                        raise ValueError(f"候选人数不足，仅有{total_candidates}人符合条件，无法抽取{count}人")

                print(f"警告: 规则 '{rule_desc}' 候选人数不足，仅有{total_candidates}人符合条件，无法抽取{count}人，已跳过该规则")
                skipped_rules += 1
                rule_result['skipped'] = True
                rule_result['skip_reason'] = f'候选人数不足，仅有{total_candidates}人符合条件'
                rule_results.append(rule_result)
                continue

            selected_indices = random.sample(range(total_candidates), count)
            selected_students = [filtered_data[i].copy() for i in selected_indices]

            rule_result['selected_students'] = selected_students
            rule_result['actual_count'] = len(selected_students)
            rule_results.append(rule_result)

            all_selected.extend(selected_students)

        if skipped_rules == len(rules):
            raise ValueError("所有抽选规则均无法执行，候选人数不足")

        if all_selected:
            primary_key = '学号' if '学号' in self.data_handler.columns else self.data_handler.columns[0]
            seen = set()
            deduped = []
            for row in all_selected:
                key = row.get(primary_key)
                if key not in seen:
                    seen.add(key)
                    deduped.append(row)
            all_selected = deduped

        stats = self._calculate_stats(all_selected, all_candidates)

        for rule_result in rule_results:
            if not rule_result['skipped'] and rule_result['selected_students'] and all_selected:
                primary_key = '学号' if '学号' in self.data_handler.columns else self.data_handler.columns[0]
                rule_ids = {s.get(primary_key) for s in rule_result['selected_students']}
                actual = [s for s in all_selected if s.get(primary_key) in rule_ids]
                rule_result['actual_count'] = len(actual)

        columns = self.data_handler.columns
        return {
            'selected_students': _DataFrameProxy(all_selected, columns),
            'rule_results': [
                {
                    **rr,
                    'selected_students': _DataFrameProxy(rr['selected_students'], columns) if rr['selected_students'] else _DataFrameProxy([], columns)
                }
                for rr in rule_results
            ],
            'seed': seed,
            'total_candidates': all_candidates,
            'stats': stats,
            'rules': rules
        }

    def _parse_rule_filters(self, rule: Dict) -> Dict:
        """解析规则中的筛选条件"""
        filters = rule.get('filters', {})
        legacy_keys = {'gender': '性别', 'is_class_leader': '是否班委', 'is_member': '是否团员'}
        for eng_key, cn_key in legacy_keys.items():
            if eng_key in rule and cn_key not in filters:
                filters[cn_key] = rule[eng_key]
        return filters

    def _validate_rules(self, rules: List[Dict]):
        """验证抽选规则的有效性"""
        for i, rule in enumerate(rules):
            if 'count' not in rule:
                raise ValueError(f"规则 {i+1} 缺少必填字段 'count'")

            count = rule.get('count', 0)
            if not isinstance(count, int) or count <= 0:
                raise ValueError(f"规则 {i+1} 的 'count' 必须是正整数，当前值: {count}")

            filters = self._parse_rule_filters(rule)
            if filters:
                errors = self.data_handler.validate_filters(filters, strict=False)
                if errors:
                    error_msg = f"规则 {i+1} 的筛选条件无效: " + "; ".join(errors)
                    raise ValueError(error_msg)

    def _format_rule(self, rule: Dict) -> str:
        """格式化规则为可读字符串"""
        count = rule.get('count', 0)
        filters = self._parse_rule_filters(rule)

        if filters:
            conditions = [f"{k}={v}" for k, v in filters.items()]
            return f"抽取{count}人 ({', '.join(conditions)})"
        else:
            return f"抽取{count}人 (无条件)"

    def _calculate_stats(self, selected_students: List[Dict], total_candidates: int) -> Dict:
        """计算抽选结果统计信息"""
        selected_count = len(selected_students)
        return {
            'selected_count': selected_count,
            'selection_ratio': round(selected_count / total_candidates * 100, 1) if total_candidates > 0 else 0
        }
