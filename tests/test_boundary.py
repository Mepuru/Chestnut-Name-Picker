#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试边界条件处理功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_handler import DataHandler
from src.selector import StudentSelector

def test_single_rule_insufficient_candidates():
    """
    测试单个规则下候选人数不足的情况
    """
    print("=== 测试单个规则下候选人数不足 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 获取实际班委人数
        班委_df = data_handler.filter_data(filters={'是否班委': '是'})
        actual_班委_count = len(班委_df)
        print(f"实际班委人数: {actual_班委_count}人")
        
        # 测试抽选人数超过实际班委人数的情况
        target_count = actual_班委_count + 1
        print(f"尝试抽取{target_count}个班委...")
        
        rules = [{
            'count': target_count,
            'filters': {'是否班委': '是'}
        }]
        
        try:
            result = selector.select_by_rules(rules)
            print(f"✗ 测试失败: 应该抛出异常，但返回了结果")
            return False
        except ValueError as e:
            print(f"✓ 正确抛出异常: {e}")
            # 验证错误信息是否包含正确的实际人数
            if f"仅有{actual_班委_count}人符合条件" in str(e):
                print("✓ 错误信息包含正确的实际人数")
            else:
                print(f"✗ 错误信息未包含正确的实际人数: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_single_rule_sufficient_candidates():
    """
    测试单个规则下候选人数充足的情况
    """
    print("\n=== 测试单个规则下候选人数充足 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 获取实际班委人数
        班委_df = data_handler.filter_data(filters={'是否班委': '是'})
        actual_班委_count = len(班委_df)
        print(f"实际班委人数: {actual_班委_count}人")
        
        # 测试抽选人数小于实际班委人数的情况
        if actual_班委_count > 0:
            target_count = min(actual_班委_count, 3)
            print(f"尝试抽取{target_count}个班委...")
            
            rules = [{
                'count': target_count,
                'filters': {'是否班委': '是'}
            }]
            
            result = selector.select_by_rules(rules)
            selected_count = result['stats']['selected_count']
            print(f"✓ 成功抽取{selected_count}个班委")
            
            # 验证抽取人数是否正确
            if selected_count == target_count:
                print("✓ 抽取人数正确")
            else:
                print(f"✗ 抽取人数错误: 期望{target_count}人，实际{selected_count}人")
                return False
        else:
            print("✓ 无班委数据，跳过测试")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_multiple_rules_some_insufficient():
    """
    测试多个规则下部分规则候选人数不足的情况
    """
    print("\n=== 测试多个规则下部分规则候选人数不足 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 创建多个规则，其中一个规则候选人数不足
        rules = [
            # 规则1: 抽选1个班委（应该成功）
            {
                'count': 1,
                'filters': {'是否班委': '是'}
            },
            # 规则2: 抽选非常多的女生班委（应该失败）
            {
                'count': 100,
                'filters': {
                    '性别': '女',
                    '是否班委': '是'
                }
            },
            # 规则3: 抽选1个男生（应该成功）
            {
                'count': 1,
                'filters': {'性别': '男'}
            }
        ]
        
        result = selector.select_by_rules(rules)
        selected_count = result['stats']['selected_count']
        print(f"✓ 部分规则执行成功，共抽取{selected_count}人")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_all_rules_insufficient():
    """
    测试所有规则候选人数都不足的情况
    """
    print("\n=== 测试所有规则候选人数都不足 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 创建所有规则都候选人数不足的情况
        rules = [
            {
                'count': 100,
                'filters': {'是否班委': '是'}
            },
            {
                'count': 100,
                'filters': {
                    '性别': '女',
                    '是否团员': '是'
                }
            }
        ]
        
        try:
            result = selector.select_by_rules(rules)
            print(f"✗ 测试失败: 应该抛出异常，但返回了结果")
            return False
        except ValueError as e:
            print(f"✓ 正确抛出异常: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("ChestNut名单抽选工具 - 边界条件处理测试\n")
    
    tests = [
        test_single_rule_insufficient_candidates,
        test_single_rule_sufficient_candidates,
        test_multiple_rules_some_insufficient,
        test_all_rules_insufficient
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"共{len(tests)}个测试，通过{passed}个，失败{len(tests)-passed}个")
    
    if passed == len(tests):
        print("✓ 所有边界条件测试通过！")
    else:
        print("✗ 边界条件测试失败！")

if __name__ == "__main__":
    main()
