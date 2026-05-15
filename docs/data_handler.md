# 数据处理模块

## DataHandler 类

负责读取和处理 Excel 文件中的数据。使用 openpyxl 直接读取 Excel，无 pandas 依赖。

### 初始化

```python
from src.data_handler import DataHandler

handler = DataHandler("data/test_data.xlsx")
```

### 主要方法

#### `get_all_data()`

获取所有数据。

**返回**: List[Dict[str, Any]] — 每个 Dict 代表一行，键为列名

#### `get_columns()`

获取列名列表。

**返回**: List[str]

#### `get_column_metadata()`

获取列元数据，包括列名、类型和唯一值。

**返回**: Dict[str, Dict]

示例：
```python
{
    '姓名': {
        'name': '姓名',
        'type': 'object',
        'unique_values': ['张三', '李四', ...],
        'non_null_count': 5,
        'total_count': 5
    },
    ...
}
```

#### `filter_data(filters=None)`

根据条件筛选数据。

**参数**:
- `filters`: 筛选条件字典，键为列名，值为筛选值

**返回**: List[Dict[str, Any]]

示例：
```python
filtered = handler.filter_data(filters={'性别': '男', '班级': '1班'})
```

#### `validate_filters(filters, strict=False)`

验证筛选条件的有效性。

**参数**:
- `filters`: 筛选条件字典
- `strict`: 是否严格验证

**返回**: List[str] 错误信息列表

#### `get_statistics()`

获取数据统计信息。

**返回**: Dict

#### `reload_data()`

重新加载数据。

#### `df` (属性)

兼容旧接口的 DataFrame 代理对象，提供 `iterrows()`、`columns`、`empty`、`head()` 等方法。

**返回**: _DataFrameProxy

## 数据格式要求

### 必需字段

| 字段名 | 说明 |
|--------|------|
| 学号 | 学生唯一标识 |
| 姓名 | 学生姓名 |

### 可选字段

可添加任意列作为筛选条件，程序会自动识别。

### 示例

| 学号 | 姓名 | 性别 | 班级 | 是否班委 |
|------|------|------|------|----------|
| 2023001 | 张三 | 男 | 1班 | 是 |
| 2023002 | 李四 | 女 | 1班 | 否 |
