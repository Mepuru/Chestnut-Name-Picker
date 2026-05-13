# UI 模块

## 模块结构

```
src/ui/
├── __init__.py
├── main_window.py      # 主窗口
├── rule_frame.py       # 规则框架
└── preview_window.py   # 数据预览窗口
```

## ClassSelectorUI 类

主窗口类，负责应用程序主界面。

### 初始化

```python
from src.ui import ClassSelectorUI

app = ClassSelectorUI()
app.run()
```

### 主要方法

#### `run()`

运行应用程序。

#### `select_file()`

选择 Excel 文件。

#### `preview_data()`

预览当前数据。

#### `perform_selection()`

执行抽选操作。

#### `add_rule(existing_rule_data=None)`

添加抽选规则。

#### `remove_rule(index)`

删除指定索引的规则。

#### `copy_rule(index)`

复制指定索引的规则。

## RuleFrame 类

单个抽选规则的 UI 框架。

### 初始化

```python
rule_frame = RuleFrame(parent, index, delete_callback, copy_callback, column_metadata)
```

### 主要方法

#### `get_rule()`

获取规则数据。

**返回**: Dict

```python
{
    'count': 3,
    'filters': {'性别': '男'}
}
```

#### `update_column_metadata(column_metadata)`

更新列元数据并重新生成筛选组件。

#### `destroy()`

销毁框架。

## DataPreviewWindow 类

数据预览窗口。

### 初始化

```python
preview = DataPreviewWindow(parent, data_handler, file_path)
```

### 主要方法

#### `get_result()`

获取用户选择结果。

**返回**: bool

```python
preview = DataPreviewWindow(root, handler, path)
root.wait_window(preview.window)
if preview.get_result():
    # 用户点击了确认
    pass
```
