# ChestNut 名单抽选工具

基于 ttkbootstrap 的名单随机抽选工具，支持多规则筛选。

## 功能特性

- 支持从 Excel 文件导入名单数据
- 支持多规则同时抽选
- 支持按字段动态筛选（性别、班级、是否班委等）
- 支持设置随机种子，确保可复现
- 支持复制抽选结果到剪贴板

## 项目结构

```
Chestnut-Name-Picker/
├── assets/              # 资源文件（图标等）
├── data/                # 数据文件（Excel）
├── src/                 # 源代码
│   ├── ui/              # UI 组件
│   │   ├── main_window.py    # 主窗口
│   │   ├── rule_frame.py     # 规则框架
│   │   └── preview_window.py # 数据预览窗口
│   ├── data_handler.py  # 数据处理
│   ├── selector.py      # 抽选逻辑
│   ├── styles.py        # 样式配置
│   └── utils.py         # 工具函数
├── tests/               # 测试文件
└── main.py              # 主入口
```

## 安装依赖

```bash
uv sync
```

## 运行

```bash
uv run main.py
```

## 运行测试

```bash
uv run python tests/test_selector.py
```

## 使用说明

1. 点击"选择Excel文件"加载名单数据
2. 点击"选择筛选字段"设置筛选条件
3. 设置抽选人数
4. 点击"开始抽选"查看结果
5. 可点击"复制学号及姓名"或"复制全部"导出结果

## 环境要求

- Python >= 3.11
- pandas >= 3.0.3
- openpyxl >= 3.1.5
- ttkbootstrap >= 1.20.3
- Pillow >= 12.2.0
