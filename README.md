<div align="center">
    <img alt="Chestnut Name Picker" src="assets/LS20260513150828.png" width=180 height=180/>

# Chestnut Name Picker

名单随机抽选工具 - 基于 ttkbootstrap 的多规则筛选抽选器

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 简介

Chestnut Name Picker 是一款名单随机抽选工具，支持从 Excel 文件导入数据，通过多规则筛选进行随机抽选。

## 核心特性

- **多规则抽选** - 支持同时设置多组抽选规则
- **动态筛选** - 根据数据列自动识别可筛选字段
- **随机种子** - 支持设置种子值，确保结果可复现
- **数据预览** - 导入前可预览 Excel 数据
- **结果导出** - 一键复制抽选结果到剪贴板

## 快速开始

### 环境要求

- Python 3.11+

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/chestnut-name-picker.git
cd chestnut-name-picker

# 使用 uv 安装依赖
uv sync
```

### 运行

```bash
# 运行应用
uv run main.py
```

### 测试

```bash
# 运行测试
uv run python tests/test_selector.py
```

## 数据格式

### 必需字段

| 字段名 | 说明 | 示例 |
|--------|------|------|
| 学号 | 学生唯一标识 | 2023001 |
| 姓名 | 学生姓名 | 张三 |

### 可选筛选字段

可添加任意列作为筛选条件，程序会自动识别：

| 字段名 | 说明 | 示例 |
|--------|------|------|
| 性别 | 男/女 | 男 |
| 班级 | 班级名称 | 1班 |
| 是否班委 | 是/否 | 是 |
| 是否团员 | 是/否 | 否 |

### Excel 示例

| 学号 | 姓名 | 性别 | 班级 | 是否班委 | 是否团员 |
|------|------|------|------|----------|----------|
| 2023001 | 张三 | 男 | 1班 | 是 | 是 |
| 2023002 | 李四 | 女 | 1班 | 否 | 是 |
| 2023003 | 王五 | 男 | 2班 | 否 | 否 |

> **提示**: 列名可自定义，程序会动态识别所有列作为可选筛选条件。

## 使用说明

1. 点击 **选择 Excel 文件** 加载名单数据
2. 点击 **选择筛选字段** 设置筛选条件（如性别、班级等）
3. 设置抽选人数
4. 点击 **开始抽选** 查看结果
5. 点击 **复制学号及姓名** 或 **复制全部** 导出结果

## 项目结构

```
Chestnut-Name-Picker/
├── assets/                  # 资源文件
│   └── LS20260513150828.png # 应用图标
├── data/                    # 数据文件
│   └── test_data.xlsx       # 测试数据
├── src/                     # 源代码
│   ├── ui/                  # UI 组件
│   │   ├── main_window.py   # 主窗口
│   │   ├── rule_frame.py    # 规则框架
│   │   └── preview_window.py # 数据预览窗口
│   ├── data_handler.py      # 数据处理
│   ├── selector.py          # 抽选逻辑
│   ├── styles.py            # 样式配置
│   └── utils.py             # 工具函数
├── tests/                   # 测试文件
├── docs/                    # 文档
├── main.py                  # 主入口
├── pyproject.toml           # 项目配置
├── LICENSE                  # MIT 协议
└── README.md
```

## 技术栈

- **UI 框架**: ttkbootstrap (Tkinter)
- **数据处理**: pandas + openpyxl
- **图像处理**: Pillow
- **包管理**: uv

## 协议

本项目使用 MIT 协议。
