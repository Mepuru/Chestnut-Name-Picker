<div align="center">
    <img alt="Chestnut Name Picker" src="assets/LS20260513150828.png" width=180 height=180/>

# Chestnut Name Picker

名单随机抽选工具 - 基于 ttkbootstrap 的多规则筛选抽选器

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

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
├── main.py                  # 主入口
├── pyproject.toml           # 项目配置
└── README.md
```

## 技术栈

- **UI 框架**: ttkbootstrap (Tkinter)
- **数据处理**: pandas + openpyxl
- **图像处理**: Pillow
- **包管理**: uv

## 协议

本项目使用 MIT 协议。
