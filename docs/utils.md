# 工具函数模块

## 函数列表

### format_datetime(timestamp)

格式化时间戳为可读日期时间字符串。

**参数**:
- `timestamp`: 时间戳（int）

**返回**: str

**示例**:
```python
from src.utils import format_datetime

time_str = format_datetime(1234567890)
# 输出: "2009-02-14 07:31:30"
```

### format_stats(stats)

格式式化统计信息为可读字符串。

**参数**:
- `stats`: 统计信息字典

**返回**: str

**示例**:
```python
from src.utils import format_stats

stats = {
    'selected_count': 5,
    'selection_ratio': 50.0,
    'total_candidates': 10
}
info = format_stats(stats)
# 输出:
# 本次抽选总人数: 5人
# 抽选比例: 50.0% (总候选人数: 10人)
```

### format_student_info(student)

格式化学生信息为可读字符串。

**参数**:
- `student`: 学生数据（Series 对象）

**返回**: str

**示例**:
```python
from src.utils import format_student_info

info = format_student_info(student_series)
# 输出:
# 学号: 2023001
# 姓名: 张三
# 性别: 男
```

### create_scrollable_frame(parent, tag="content")

创建带垂直滚动条的可滚动框架。

**参数**:
- `parent`: 父容器（ttk.Frame）
- `tag`: 画布窗口标签

**返回**: Tuple[tk.Canvas, ttk.Frame]

**示例**:
```python
from src.utils import create_scrollable_frame

canvas, inner_frame = create_scrollable_frame(parent_container, "my_content")
# 在 inner_frame 中添加内容
ttk.Label(inner_frame, text="Hello").pack()
```
