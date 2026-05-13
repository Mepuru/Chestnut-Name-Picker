# 抽选逻辑模块

## StudentSelector 类

负责根据条件进行随机抽选。

### 初始化

```python
from src.data_handler import DataHandler
from src.selector import StudentSelector

handler = DataHandler("data/test_data.xlsx")
selector = StudentSelector(handler)
```

### 主要方法

#### `select_by_rules(rules, seed=None)`

根据多组规则随机抽选学生。

**参数**:
- `rules`: 抽选规则列表
- `seed`: 随机种子，None 则使用当前时间戳

**返回**: Dict

```python
{
    'selected_students': DataFrame,  # 所有规则合并后的学生列表
    'rule_results': List[Dict],      # 每个规则单独的结果
    'seed': int,                     # 随机种子
    'total_candidates': int,         # 总候选人数
    'stats': Dict,                   # 统计信息
    'rules': List[Dict]              # 抽选规则列表
}
```

**规则格式**:
```python
rules = [
    {
        'count': 3,  # 抽选人数
        'filters': {  # 筛选条件（可选）
            '性别': '男',
            '班级': '1班'
        }
    },
    {
        'count': 2,
        'filters': {
            '性别': '女'
        }
    }
]
```

**示例**:
```python
result = selector.select_by_rules(rules, seed=12345)
print(f"抽取了 {result['stats']['selected_count']} 人")
```

#### `select_students(count, gender=None, is_class_leader=None, is_member=None, seed=None)`

根据条件随机抽选学生（兼容接口）。

**参数**:
- `count`: 抽选人数
- `gender`: 性别筛选（男/女/None）
- `is_class_leader`: 是否班委（是/否/None）
- `is_member`: 是否团员（是/否/None）
- `seed`: 随机种子

**返回**: Dict

**示例**:
```python
result = selector.select_students(3, gender='女', seed=12345)
```

### 错误处理

- `ValueError`: 规则无效或候选人数不足

```python
try:
    result = selector.select_by_rules(rules)
except ValueError as e:
    print(f"抽选失败: {e}")
```

### 去重机制

当多个规则可能选中同一学生时，自动去重，保留第一次选中的结果。
