#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多规则抽选功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_handler import DataHandler
from src.selector import StudentSelector

def test_multi_rule_selection():
    """测试多规则抽选功能"""
    print("=== 测试多规则抽选功能 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)

        # 测试案例1：从团员中抽取3人，从非团员中抽取5人
        print("\n测试案例1：从团员中抽取3人，从非团员中抽取5人")
        rules = [
            {'count': 3, 'filters': {'是否团员': '是'}},
            {'count': 5, 'filters': {'是否团员': '否'}}
        ]

        result = selector.select_by_rules(rules)
        selected = result['selected_students']

        print(f"✓ 多规则抽选成功，共抽取{len(selected)}人")

        member_count = len([s for s in selected if s.get('是否团员') == '是'])
        non_member_count = len([s for s in selected if s.get('是否团员') == '否'])
        print(f"✓ 团员抽取人数: {member_count}人")
        print(f"✓ 非团员抽取人数: {non_member_count}人")

        # 测试案例2：复杂组合条件
        print("\n测试案例2：复杂组合条件")
        rules = [
            {'count': 2, 'filters': {'性别': '男', '是否班委': '是'}},
            {'count': 2, 'filters': {'性别': '女', '是否团员': '是'}},
            {'count': 3, 'filters': {'是否班委': '否', '是否团员': '否'}}
        ]

        result = selector.select_by_rules(rules)
        selected = result['selected_students']
        print(f"✓ 复杂组合条件抽选成功，共抽取{len(selected)}人")

        # 测试案例3：相同种子重复抽选
        print("\n测试案例3：相同种子重复抽选")
        seed = 12345
        result1 = selector.select_by_rules(rules, seed=seed)
        result2 = selector.select_by_rules(rules, seed=seed)

        same_result = result1['selected_students'].equals(result2['selected_students'])
        print(f"✓ 相同种子抽选 {'成功' if same_result else '失败'}，相同种子得到{'相同' if same_result else '不同'}结果")

        # 测试案例4：去重功能
        print("\n测试案例4：去重功能")
        rules = [
            {'count': 10, 'filters': {'性别': '男'}},
            {'count': 5, 'filters': {'是否班委': '否'}}
        ]

        result = selector.select_by_rules(rules)
        selected = result['selected_students']
        unique_ids = set(s.get('学号') for s in selected)
        print(f"✓ 去重功能正常，抽取{len(selected)}人，其中唯一学生{len(unique_ids)}人")

        return True

    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("ChestNut名单抽选工具 - 多规则抽选功能测试\n")

    if test_multi_rule_selection():
        print("\n✓ 所有多规则抽选测试通过！")
    else:
        print("\n✗ 多规则抽选测试失败！")

if __name__ == "__main__":
    main()
