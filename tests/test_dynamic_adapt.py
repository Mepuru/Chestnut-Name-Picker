#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试动态数据适配功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_handler import DataHandler
from src.selector import StudentSelector

def test_dynamic_column_handling():
    """测试动态列处理功能"""
    print("=== 测试动态列处理功能 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        
        # 获取列元数据
        column_metadata = data_handler.get_column_metadata()
        print(f"✓ 成功获取列元数据，共{len(column_metadata)}列")
        
        # 打印列信息
        for col_name, metadata in column_metadata.items():
            print(f"  - {col_name}: 类型={metadata['type']}, 有效值={metadata['unique_values']}")
        
        # 测试动态筛选
        selector = StudentSelector(data_handler)
        
        # 使用动态筛选规则（新格式）
        rules = [
            {
                'count': 2,
                'filters': {
                    '性别': '男',
                    '是否班委': '是'
                }
            },
            {
                'count': 2,
                'filters': {
                    '性别': '女',
                    '是否团员': '是'
                }
            }
        ]
        
        result = selector.select_by_rules(rules)
        print(f"✓ 动态筛选规则测试成功，共抽取{result['stats']['selected_count']}人")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_data_refresh():
    """测试数据刷新功能"""
    print("\n=== 测试数据刷新功能 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        
        # 获取初始数据数量
        initial_count = len(data_handler.get_all_data())
        print(f"✓ 初始数据数量: {initial_count}人")
        
        # 执行数据刷新
        data_handler.reload_data()
        refreshed_count = len(data_handler.get_all_data())
        print(f"✓ 数据刷新成功，刷新后数据数量: {refreshed_count}人")
        
        # 验证数据一致性
        assert initial_count == refreshed_count, "刷新前后数据数量不一致"
        print("✓ 刷新前后数据数量一致")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_dynamic_rule_validation():
    """测试动态规则验证"""
    print("\n=== 测试动态规则验证 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 测试不存在的列
        rules = [
            {
                'count': 2,
                'filters': {
                    '不存在的列': '值'
                }
            }
        ]
        
        try:
            result = selector.select_by_rules(rules)
            print(f"✗ 测试失败: 应该拒绝不存在的列")
            return False
        except ValueError as e:
            print(f"✓ 正确拒绝了不存在的列: {e}")
        
        # 测试无效值但存在的列（应该跳过该规则，返回空结果）
        rules = [
            {
                'count': 2,
                'filters': {
                    '性别': '无效性别值'
                }
            }
        ]
        
        result = selector.select_by_rules(rules)
        print(f"✓ 无效值处理成功，返回{result['stats']['selected_count']}人")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_backward_compatibility():
    """
    测试向后兼容性，确保原有代码无需修改即可正常工作
    """
    print("\n=== 测试向后兼容性 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 使用原有API格式进行抽选
        result = selector.select_students(3, gender='男', is_class_leader='是')
        print(f"✓ 原有API格式测试成功，抽取了{result['stats']['selected_count']}人")
        
        # 使用原有多规则格式（旧格式）
        rules = [
            {
                'count': 2,
                'gender': '女',
                'is_member': '是'
            }
        ]
        
        result = selector.select_by_rules(rules)
        print(f"✓ 原有多规则格式测试成功，抽取了{result['stats']['selected_count']}人")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("ChestNut名单抽选工具 - 动态数据适配功能测试\n")
    
    tests = [
        test_dynamic_column_handling,
        test_data_refresh,
        test_dynamic_rule_validation,
        test_backward_compatibility
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"共{len(tests)}个测试，通过{passed}个，失败{len(tests)-passed}个")
    
    if passed == len(tests):
        print("✓ 所有动态数据适配测试通过！")
    else:
        print("✗ 动态数据适配测试失败！")

if __name__ == "__main__":
    main()
