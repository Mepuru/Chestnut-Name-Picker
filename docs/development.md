# 开发指南

## 环境搭建

### 前置要求

- Python 3.11+
- uv (包管理器)

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/Mepuru/Chestnut-Name-Picker.git
cd Chestnut-Name-Picker

# 安装依赖
uv sync
```

### 运行项目

```bash
uv run main.py
```

## 项目结构

```
Chestnut-Name-Picker/
├── assets/              # 资源文件
├── data/                # 数据文件
├── src/                 # 源代码
│   ├── ui/              # UI 组件
│   ├── data_handler.py  # 数据处理
│   ├── selector.py      # 抽选逻辑
│   ├── styles.py        # 样式配置
│   └── utils.py         # 工具函数
├── tests/               # 测试文件
├── docs/                # 文档
└── main.py              # 主入口
```

## 代码规范

### 命名规范

- 类名：PascalCase（如 `DataHandler`）
- 函数名：snake_case（如 `format_datetime`）
- 常量：UPPER_SNAKE_CASE（如 `BASE_DIR`）

### 文档字符串

使用 Google 风格：

```python
def function(param1: str, param2: int) -> bool:
    """
    函数说明
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
        
    Returns:
        返回值说明
        
    Raises:
        ValueError: 异常说明
    """
    pass
```

## 测试

### 运行测试

```bash
# 运行所有测试
uv run python tests/test_selector.py

# 运行特定测试
uv run python tests/test_boundary.py
```

### 编写测试

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_handler import DataHandler
from src.selector import StudentSelector

def test_feature():
    """测试功能说明"""
    try:
        # 测试代码
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        return False
```

## 构建打包

### 生成 exe

```bash
uv run pyinstaller --onefile --windowed --name "ChestnutNamePicker" --icon "assets/LS20260513150828.png" --add-data "assets;assets" main.py
```

### 输出位置

构建产物位于 `dist/` 目录。

## 发布流程

1. 更新 `pyproject.toml` 版本号
2. 更新 `CHANGELOG.md`
3. 提交代码
4. 创建 tag：`git tag -a v1.x.x -m "Release v1.x.x"`
5. 推送：`git push origin master --tags`
6. 创建 Release：`gh release create v1.x.x --title "v1.x.x" --notes-file CHANGELOG.md dist/ChestnutNamePicker.exe`

## 常见问题

### 图标不显示

确保 `assets/` 目录下有图标文件，并检查路径是否正确。

### 导入失败

确保在项目根目录运行，或检查 `sys.path` 配置。
