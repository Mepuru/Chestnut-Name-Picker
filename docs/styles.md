# 样式配置模块

## configure_styles(style)

配置应用程序的所有 UI 样式。

### 参数

- `style`: ttkbootstrap 样式对象（ttk.Style）

### 使用

```python
import ttkbootstrap as ttk
from src.styles import configure_styles

root = ttk.Window(themename="litera")
style = ttk.Style()
configure_styles(style)
```

### 配置的样式

#### 基础组件

| 样式名 | 说明 |
|--------|------|
| TLabel | 标签 |
| TButton | 按钮 |
| TEntry | 输入框 |
| TCombobox | 下拉框 |
| TCheckbutton | 复选框 |

#### 容器组件

| 样式名 | 说明 |
|--------|------|
| TLabelframe | 标签框架 |
| TLabelframe.Label | 标签框架标题 |

#### 滚动条

| 样式名 | 说明 |
|--------|------|
| Vertical.TScrollbar | 垂直滚动条 |
| Horizontal.TScrollbar | 水平滚动条 |

#### 表格

| 样式名 | 说明 |
|--------|------|
| Treeview | 表格 |
| Treeview.Heading | 表头 |

#### 选项卡

| 样式名 | 说明 |
|--------|------|
| Tab.TNotebook | 选项卡容器 |
| TNotebook.Tab | 选项卡标签 |

#### 按钮变体

| 样式名 | 说明 |
|--------|------|
| Primary.TButton | 主要按钮（蓝色） |
| Secondary.TButton | 次要按钮（灰色） |
| Success.TButton | 成功按钮（绿色） |
| Danger.TButton | 危险按钮（红色） |
| Warning.TButton | 警告按钮（黄色） |

### 自定义样式

如需修改样式，可直接调用 style.configure()：

```python
style.configure("TLabel", font=("Microsoft YaHei", 12))
```
