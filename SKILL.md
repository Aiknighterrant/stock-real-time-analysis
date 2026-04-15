# 实时股票基本面分析技能

## 概述

这是一个基于实时数据的股票基本面分析技能，每次分析都获取最新市场数据，不存储旧信息。系统使用akshare作为主要数据源，整合多个API获取实时行情、财务数据和估值指标。

## 特性

- 🔄 **完全实时**: 每次分析都获取最新数据，不依赖缓存
- 📊 **多数据源**: 整合多个数据源，提高数据准确性
- ⚡ **智能缓存**: 5分钟缓存，平衡实时性和性能
- 📈 **完整分析链**: 行情、财务、估值、风险、建议
- 🛡️ **健壮性**: 错误处理和重试机制
- 📋 **专业报告**: 格式化输出，易于阅读

## 支持的股票

当前支持以下A股核心股票：

| 股票名称 | 股票代码 | 板块 |
|---------|---------|------|
| 贵州茅台 | 600519 | 食品饮料 |
| 五粮液 | 000858 | 食品饮料 |
| 宁德时代 | 300750 | 新能源 |
| 比亚迪 | 002594 | 新能源汽车 |
| 中国平安 | 601318 | 金融保险 |
| 长飞光纤 | 601869 | 通信设备 |
| 招商银行 | 600036 | 银行 |
| 中信证券 | 600030 | 证券 |
| 东方财富 | 300059 | 互联网券商 |

## 分析指标

### 1. 实时行情
- 当前价格、涨跌幅
- 开盘价、最高价、最低价
- 成交量、成交额、换手率
- 总市值、流通市值

### 2. 估值指标
- **PE（市盈率）**: 股价/每股收益
- **PB（市净率）**: 股价/每股净资产
- **PS（市销率）**: 总市值/营收
- **PEG**: PE/利润增长率

### 3. 盈利能力
- **ROE（净资产收益率）**: 净利润/净资产
- **毛利率**: 毛利/营收
- **净利率**: 净利润/营收
- **每股收益（EPS）**: 净利润/总股本

### 4. 成长性
- 营收增长率
- 利润增长率
- 资产增长率

### 5. 风险评估
- PE风险等级
- PB风险等级
- ROE质量评估
- 总体风险评级

## 使用方法

### 在OpenClaw中直接使用

```
分析股票 长飞光纤
分析股票 601869
分析股票 贵州茅台
分析股票 五粮液
```

### 命令行使用

```bash
python stock_real_time_analyzer.py 601869
python stock_real_time_analyzer.py 长飞光纤
```

### Python代码调用

```python
from stock_real_time_analyzer import RealTimeStockAnalyzer

analyzer = RealTimeStockAnalyzer()
result = analyzer.analyze_stock("长飞光纤")
report = analyzer.format_report(result)
print(report)
```

## 安装依赖

```bash
pip install akshare pandas numpy
```

## 文件结构

```
stock-real-time-analysis/
├── SKILL.md                    # 技能文档
├── stock_real_time_analyzer.py # 核心分析器
├── skill_interface.py          # OpenClaw接口
├── requirements.txt            # 依赖包
├── test_analyzer.py           # 测试文件
└── examples/                  # 使用示例
    ├── basic_usage.py
    └── batch_analysis.py
```

## 快速开始

### 1. 安装依赖

```bash
pip install akshare pandas numpy
```

### 2. 运行示例

```bash
python test_analyzer.py
```

### 3. 分析单只股票

```bash
python stock_real_time_analyzer.py 601869
```

### 4. 批量分析

```bash
python examples/batch_analysis.py
```

## 分析报告示例

```
📈 长飞光纤 (601869) 实时基本面分析报告
====================================================
📅 分析时间: 2026-04-16 01:45:23

💰 实时行情
• 当前价格: ¥358.61
• 涨跌幅: -1.62%
• 成交量: 170,900股
• 成交额: ¥6.19亿元
• 换手率: 4.21%

📊 估值指标
• PE(市盈率): 335.15倍
• PB(市净率): 21.50倍
• PS(市销率): 20.83倍
• PEG: 6.57倍

💹 盈利能力
• ROE(净资产收益率): 5.89%
• 毛利率: 29.93%
• 净利率: 7.62%
• 每股收益: ¥1.07

🚀 成长性指标
• 营收增长率: +16.85%
• 利润增长率: +20.40%

⚠️ 风险分析
• PE风险: 极高风险
• PB风险: 极高风险
• ROE质量: 较差
• 总体风险: 高风险

🎯 投资建议
• 短期策略: 估值过高，存在重大回调风险
• 中期策略: 等待估值回归合理区间（PE<30，PB<3）
• 长期策略: 基本面良好可长期关注，但需等待合适入场时机
• 操作建议: 卖出或观望
• 信心指数: 75%

📌 总结
长飞光纤 (601869) 综合分析总结
========================================
• 估值水平: PE=335.15倍, PB=21.50倍
• 盈利能力: ROE=5.89%
• 风险等级: 高风险
• 操作建议: 卖出或观望

====================================================
⚠️ 免责声明: 以上分析基于实时数据，仅供参考，不构成投资建议。
   投资有风险，入市需谨慎。
```

## 配置选项

### 缓存设置

```python
analyzer = RealTimeStockAnalyzer(
    cache_ttl=300,      # 缓存时间（秒），默认5分钟
    max_cache_size=100  # 最大缓存条目数
)
```

### 数据源配置

```python
analyzer = RealTimeStockAnalyzer(
    use_fallback=True,    # 启用备用数据源
    retry_attempts=3,     # 重试次数
    timeout=30           # 请求超时时间（秒）
)
```

## 高级功能

### 1. 批量分析

```python
stocks = ['601869', '600519', '000858', '300750']
results = analyzer.batch_analyze(stocks)
```

### 2. 自定义分析

```python
# 只获取实时行情
quote = analyzer.get_real_time_quote('601869')

# 只获取财务数据
financials = analyzer.get_financial_data('601869')

# 只计算估值指标
valuation = analyzer.calculate_valuation('601869')
```

### 3. 数据导出

```python
# 导出为JSON
import json
with open('analysis.json', 'w') as f:
    json.dump(result, f, indent=2)

# 导出为CSV
import pandas as pd
df = pd.DataFrame([result])
df.to_csv('analysis.csv', index=False)
```

## 故障排除

### 常见问题

1. **网络连接失败**
   - 检查网络连接
   - 尝试使用备用数据源
   - 增加重试次数

2. **数据获取超时**
   - 增加超时时间
   - 减少请求数据量
   - 使用缓存数据


3. **字段缺失**
   - 检查数据源更新
   - 使用备用字段
   - 手动计算缺失指标

### 错误处理

系统内置错误处理和重试机制：

```python
try:
    result = analyzer.analyze_stock('601869')
except Exception as e:
    print(f"分析失败: {e}")
    # 使用备用数据或返回默认值
```

## 性能优化

### 1. 缓存策略

- 实时数据：5分钟缓存
- 财务数据：24小时缓存
- 静态信息：永久缓存

### 2. 并发处理

```python
# 使用多线程批量获取
results = analyzer.concurrent_analyze(stocks, max_workers=5)
```

### 3. 数据压缩

- 压缩历史数据
- 增量更新
- 智能缓存清理

## 安全考虑

### 数据安全

- 仅使用公开数据
- 不存储敏感信息
- 遵循数据源使用条款

### 隐私保护

- 不收集用户信息
- 数据匿名处理
- 符合隐私法规

## 免责声明

1. **数据准确性**: 分析基于公开数据，不保证数据准确性
2. **投资建议**: 分析结果仅供参考，不构成投资建议
3. **风险提示**: 投资有风险，入市需谨慎
4. **责任限制**: 不对分析结果导致的投资损失负责

## 更新日志

### v1.0.0 (2026-04-16)
- 初始版本发布
- 支持6只核心A股分析
- 实时数据获取
- 完整分析报告

### v1.1.0 (计划中)
- 支持更多A股股票
- 添加技术分析指标
- 优化缓存策略
- 添加错误处理

## 支持与反馈

如有问题或建议，请通过以下方式联系：

1. **问题报告**: 提交GitHub Issue
2. **功能建议**: 提交GitHub Pull Request
3. **技术支持**: 通过OpenClaw社区获取帮助

## 许可证

MIT License

Copyright (c) 2026 OpenClaw Community

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.