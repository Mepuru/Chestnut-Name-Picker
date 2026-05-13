#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# 读取Excel文件
file_path = "../data/test_data.xlsx"
df = pd.read_excel(file_path)

# 显示文件基本信息
print(f"文件路径: {file_path}")
print(f"行数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"\n列名: {list(df.columns)}")

# 显示数据类型
print(f"\n数据类型:")
print(df.dtypes)

# 显示前5行数据
print(f"\n前5行数据:")
print(df.head())

# 显示各列的唯一值数量
print(f"\n各列唯一值数量:")
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count}")

# 显示各列的具体唯一值（如果数量不多）
print(f"\n各列唯一值（数量<=10）:")
for col in df.columns:
    unique_values = df[col].unique()
    if len(unique_values) <= 10:
        print(f"{col}: {unique_values}")
    else:
        print(f"{col}: 包含{len(unique_values)}个唯一值")
