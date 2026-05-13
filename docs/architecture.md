# 架构概览

## 项目结构

```
Chestnut-Name-Picker/
├── assets/                  # 资源文件
│   └── LS20260513150828.png # 应用图标
├── data/                    # 数据文件
│   └── test_data.xlsx       # 测试数据
├── src/                     # 源代码
│   ├── ui/                  # UI 组件
│   │   ├── __init__.py
│   │   ├── main_window.py   # 主窗口
│   │   ├── rule_frame.py    # 规则框架
│   │   └── preview_window.py # 数据预览窗口
│   ├── __init__.py
│   ├── data_handler.py      # 数据处理
│   ├── selector.py          # 抽选逻辑
│   ├── styles.py            # 样式配置
│   └── utils.py             # 工具函数
├── tests/                   # 测试文件
├── docs/                    # 文档
├── main.py                  # 主入口
├── pyproject.toml           # 项目配置
└── README.md
```

## 模块依赖关系

```
main.py
  └── src/ui/main_window.py (ClassSelectorUI)
        ├── src/ui/rule_frame.py (RuleFrame)
        ├── src/ui/preview_window.py (DataPreviewWindow)
        ├── src/data_handler.py (DataHandler)
        ├── src/selector.py (StudentSelector)
        ├── src/styles.py (configure_styles)
        └── src/utils.py (format_datetime, format_stats, create_scrollable_frame)
```

## 数据流

1. 用户选择 Excel 文件
2. DataHandler 读取并解析数据
3. 用户设置筛选规则（RuleFrame）
4. StudentSelector 执行抽选
5. 结果显示在界面上
