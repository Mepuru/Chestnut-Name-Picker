#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本，验证各个模块的功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_handler import DataHandler
from src.selector import StudentSelector
from src.utils import format_stats, format_datetime

def test_data_handler():
    """测试数据处理器"""
    print("=== 测试数据处理器 ===")
    try:
        # 使用实际存在的Excel文件
        data_handler = DataHandler("../data/test_data.xlsx")
        print(f"✓ 成功读取文件，共{len(data_handler.get_all_data())}条记录")
        
        # 测试筛选功能 - 使用新的filters格式
        filtered_df = data_handler.filter_data(filters={'性别': '男', '是否班委': '是'})
        print(f"✓ 按性别和班委筛选成功，共{len(filtered_df)}条记录")
        
        # 测试统计功能
        stats = data_handler.get_statistics()
        print(f"✓ 统计功能正常: 总人数{stats['总人数']}")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_selector():
    """测试抽选器"""
    print("\n=== 测试抽选器 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 测试基本抽选
        result = selector.select_students(3)
        print(f"✓ 基本抽选成功，抽取了{result['stats']['selected_count']}人")
        
        # 测试带条件抽选 - 使用新的接口格式
        result = selector.select_students(2, gender='女', is_member='是')
        print(f"✓ 带条件抽选成功，抽取了{result['stats']['selected_count']}名女生团员")
        
        # 测试指定种子抽选
        seed = 12345
        result1 = selector.select_students(2, seed=seed)
        result2 = selector.select_students(2, seed=seed)
        # 验证相同种子得到相同结果
        same_result = result1['selected_students'].equals(result2['selected_students'])
        print(f"✓ 指定种子抽选 {'成功' if same_result else '失败'}，相同种子得到{'相同' if same_result else '不同'}结果")
        
        # 测试结果格式化
        stats_info = format_stats(result1['stats'])
        print(f"✓ 结果格式化正常: {stats_info.split('\n')[0]}")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    try:
        data_handler = DataHandler("../data/test_data.xlsx")
        selector = StudentSelector(data_handler)
        
        # 测试抽选人数等于候选人数
        total = len(data_handler.get_all_data())
        result = selector.select_students(total)
        print(f"✓ 抽选人数等于候选人数成功，抽取了{result['stats']['selected_count']}人")
        
        # 测试无效条件（应该返回空结果）
        result = selector.select_students(1, gender='未知')
        print(f"✓ 无效条件处理成功，返回{result['stats']['selected_count']}人")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("ChestNut名单抽选工具测试开始\n")
    
    tests = [
        test_data_handler,
        test_selector,
        test_edge_cases
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"共{len(tests)}个测试，通过{passed}个，失败{len(tests)-passed}个")
    
    if passed == len(tests):
        print("✓ 所有测试通过！程序功能正常")
    else:
        print("✗ 部分测试失败，请检查代码")

if __name__ == "__main__":
    main()
