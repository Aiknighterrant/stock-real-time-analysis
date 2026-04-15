# 📈 股票实时分析技能 (Stock Real-Time Analysis Skill)

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个功能强大的OpenClaw股票实时分析技能，支持自动触发、实时数据获取、完整基本面分析、风险评估和投资建议。

## ✨ 核心特性

### 🎯 智能触发机制
- **自动识别**: 单独输入股票名称或代码即触发分析
- **多格式支持**: 支持股票名称、代码、简称
- **精准识别**: 避免误触发，确保准确性

### 📊 完整分析功能
- **实时行情**: 获取最新价格、涨跌幅、成交量等
- **财务指标**: 每股收益、ROE、毛利率、净利率等
- **估值分析**: PE、PB、PS、PEG等估值指标
- **风险评估**: 多维度风险评估体系
- **投资建议**: 可操作的投资建议和信心指数

### 🚀 性能优化
- **精准搜索**: 只搜索指定股票的实时信息，不获取全部股票
- **智能缓存**: 5分钟TTL缓存，减少重复请求
- **多级降级**: 三级数据获取策略，确保可用性
- **秒级响应**: 优化算法，实现秒级分析报告

## 📋 支持的股票

### A股 (24只核心股票)
| 股票名称 | 股票代码 | 行业分类 | 备注 |
|---------|---------|---------|------|
| 贵州茅台 | 600519 | 食品饮料 | 白酒龙头 |
| 五粮液 | 000858 | 食品饮料 | 白酒龙头 |
| 中芯国际 | 688981 | 半导体制造 | 科创板龙头 |
| 宁德时代 | 300750 | 新能源 | 动力电池龙头 |
| 比亚迪 | 002594 | 新能源汽车 | 新能源汽车龙头 |
| 中国平安 | 601318 | 金融保险 | 保险龙头 |
| 招商银行 | 600036 | 银行 | 零售银行龙头 |
| 中信证券 | 600030 | 证券 | 券商龙头 |
| 东方财富 | 300059 | 互联网券商 | 互联网券商龙头 |
| 长飞光纤 | 601869 | 通信设备 | 光纤光缆龙头 |
| 万科A | 000002 | 房地产 | 地产龙头 |
| 格力电器 | 000651 | 家电 | 空调龙头 |
| 美的集团 | 000333 | 家电 | 家电龙头 |
| 海康威视 | 002415 | 安防 | 安防龙头 |
| 恒瑞医药 | 600276 | 医药 | 创新药龙头 |
| 药明康德 | 603259 | 医药研发 | CRO龙头 |
| 隆基绿能 | 601012 | 新能源 | 光伏龙头 |
| 通威股份 | 600438 | 新能源 | 光伏+农业 |
| 韦尔股份 | 603501 | 半导体设计 | CIS芯片龙头 |
| 中信证券 | 600030 | 证券 | 券商龙头 |
| 东方财富 | 300059 | 互联网券商 | 互联网券商龙头 |
| 长飞光纤 | 601869 | 通信设备 | 光纤光缆龙头 |
| 万科A | 000002 | 房地产 | 地产龙头 |
| 格力电器 | 000651 | 家电 | 空调龙头 |

### 港股 (5只核心股票)
| 股票名称 | 股票代码 | 行业分类 | 备注 |
|---------|---------|---------|------|
| 腾讯控股 | 00700 | 互联网 | 社交+游戏龙头 |
| 阿里巴巴 | 09988 | 电商 | 电商龙头 |
| 美团 | 03690 | 本地生活 | 外卖+到店龙头 |
| 京东 | 09618 | 电商 | 自营电商龙头 |
| 小米集团 | 01810 | 消费电子 | 手机+IoT龙头 |

## 🚀 快速开始

### 安装方式

#### 1. 通过OpenClaw安装
```bash
# 如果技能已发布到技能市场
openclaw skill install stock-real-time-analysis
```

#### 2. 手动安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/stock-real-time-analysis.git
cd stock-real-time-analysis

# 安装依赖
pip install -r requirements.txt

# 复制到OpenClaw技能目录
cp -r stock-real-time-analysis /path/to/openclaw/skills/
```

### 使用方法

#### 在OpenClaw中直接使用
```
# 输入股票名称
中芯国际

# 输入股票代码
688981

# 输入股票简称
茅台
```

#### 命令行使用
```bash
# 直接运行分析器
python stock_real_time_analyzer.py 中芯国际
python stock_real_time_analyzer.py 688981
python stock_real_time_analyzer.py 贵州茅台
```

#### Python代码中使用
```python
from stock_real_time_analyzer import OptimizedRealTimeStockAnalyzer

analyzer = OptimizedRealTimeStockAnalyzer()
result = analyzer.analyze_stock_efficient("中芯国际")

if 'error' not in result:
    report = analyzer.format_analysis_report_efficient(result)
    print(report)
```

## 📁 文件结构

```
stock-real-time-analysis/
├── README.md                    # 本文档
├── SKILL.md                     # OpenClaw技能文档
├── openclaw.skill.json          # OpenClaw技能配置
├── requirements.txt             # Python依赖包
├── stock_real_time_analyzer.py  # 核心分析器
├── skill_interface.py           # 技能接口
├── test_efficient_analyzer.py   # 测试套件
└── examples/                    # 使用示例
    ├── basic_usage.py           # 基础使用示例
    └── advanced_analysis.py     # 高级分析示例
```

## 🔧 技术架构

### 核心组件

#### 1. OptimizedRealTimeStockAnalyzer (核心分析器)
- **数据获取**: 多级数据获取策略
- **缓存机制**: 智能缓存，减少重复请求
- **分析计算**: 完整的估值和风险评估
- **报告生成**: 格式化报告输出

#### 2. StockAnalysisSkill (技能接口)
- **输入识别**: 自动识别股票输入
- **触发逻辑**: 智能触发机制
- **错误处理**: 健壮的错误处理
- **响应格式化**: 用户友好的输出

#### 3. 数据源
- **akshare**: 主要的股票数据源
- **多级降级**: 三级数据获取策略确保可用性
- **实时更新**: 基于最新市场数据

### 触发机制
```python
# 触发逻辑流程
用户输入 → 输入清理 → 模式匹配 → 股票识别 → 触发分析 → 生成报告

# 支持的输入模式
- 股票名称: "中芯国际", "贵州茅台"
- 股票代码: "688981", "600519"
- 股票简称: "茅台", "平安", "腾讯"
```

## 📊 功能详解

### 1. 实时行情分析
- **当前价格**: 最新成交价
- **涨跌幅**: 当日涨跌百分比
- **成交量**: 当日成交量
- **成交额**: 当日成交金额
- **换手率**: 当日换手率
- **振幅**: 当日价格波动幅度

### 2. 财务指标分析
- **每股收益 (EPS)**: 每股盈利能力
- **每股净资产**: 每股账面价值
- **净资产收益率 (ROE)**: 股东权益回报率
- **毛利率**: 产品盈利能力
- **净利率**: 整体盈利能力
- **营收增长率**: 收入增长速度
- **利润增长率**: 利润增长速度

### 3. 估值分析
- **PE (市盈率)**: 价格与每股收益比率
- **PB (市净率)**: 价格与每股净资产比率
- **PS (市销率)**: 价格与销售收入比率
- **PEG**: 市盈率相对盈利增长比率

### 4. 风险评估
- **PE风险**: 基于市盈率的估值风险
- **PB风险**: 基于市净率的估值风险
- **ROE质量**: 盈利能力质量评估
- **总体风险**: 综合风险评估

### 5. 投资建议
- **短期策略**: 1-3天操作建议
- **中期策略**: 1-3个月操作建议
- **长期策略**: 6个月以上操作建议
- **信心指数**: 建议的置信度
- **操作建议**: 具体的买卖建议

## 🧪 测试

### 运行测试套件
```bash
# 运行完整测试
python test_efficient_analyzer.py

# 测试特定股票
python -c "from stock_real_time_analyzer import OptimizedRealTimeStockAnalyzer; analyzer = OptimizedRealTimeStockAnalyzer(); result = analyzer.analyze_stock_efficient('中芯国际'); print(result.get('stock_name'), result.get('stock_code'))"
```

### 测试覆盖率
- ✅ 股票识别测试
- ✅ 数据获取测试
- ✅ 分析计算测试
- ✅ 报告生成测试
- ✅ 触发机制测试
- ✅ 错误处理测试

## 🔄 扩展和定制

### 添加新股票
```python
# 在 stock_real_time_analyzer.py 中添加
stock_mapping = {
    # 现有股票...
    '新股票名称': '股票代码',
    # 更多股票...
}
```

### 自定义分析逻辑
```python
class CustomStockAnalyzer(OptimizedRealTimeStockAnalyzer):
    def custom_analysis_method(self, stock_code):
        # 自定义分析逻辑
        pass
    
    def generate_custom_report(self, analysis_result):
        # 自定义报告格式
        pass
```

### 添加技术指标
```python
def add_technical_indicators(self, stock_code):
    # 添加MACD、KDJ、RSI等技术指标
    pass
```

## 📈 性能优化

### 1. 数据获取优化
- **精准搜索**: 只获取指定股票数据
- **智能缓存**: 5分钟TTL缓存
- **多级降级**: 三级数据获取策略
- **并发处理**: 支持并发数据获取

### 2. 计算优化
- **向量化计算**: 使用numpy进行向量化计算
- **缓存结果**: 缓存中间计算结果
- **懒加载**: 按需加载数据

### 3. 内存优化
- **及时释放**: 及时释放不再使用的数据
- **数据压缩**: 压缩存储的数据
- **分批处理**: 大数据分批处理

## 🛡️ 安全性

### 输入验证
- **格式验证**: 验证输入格式
- **内容验证**: 验证输入内容
- **长度限制**: 限制输入长度
- **字符过滤**: 过滤特殊字符

### 数据安全
- **数据源验证**: 验证数据源可靠性
- **计算结果验证**: 验证计算准确性
- **缓存安全**: 缓存数据安全存储

### 错误处理
- **异常捕获**: 捕获并处理各种异常
- **降级策略**: 优雅降级处理
- **用户提示**: 友好的错误提示

## 📚 API文档

### 核心类: OptimizedRealTimeStockAnalyzer

#### 初始化
```python
analyzer = OptimizedRealTimeStockAnalyzer(cache_ttl=300)
```

#### 主要方法
```python
# 分析股票
result = analyzer.analyze_stock_efficient("股票名称或代码")

# 获取实时行情
quote = analyzer.get_real_time_quote_single("股票代码")

# 获取财务数据
financial = analyzer.get_financial_data_efficient("股票代码")

# 计算估值指标
valuation = analyzer.calculate_valuation_efficient("股票代码")

# 格式化报告
report = analyzer.format_analysis_report_efficient(result)
```

### 技能接口: StockAnalysisSkill

```python
from skill_interface import StockAnalysisSkill

skill = StockAnalysisSkill()

# 检查是否为股票输入
if skill.is_stock_input("中芯国际"):
    # 分析股票
    result = skill.analyze_stock("中芯国际")
    
    # 格式化响应
    response = skill.format_response(result)
    print(response)
```

## 🤝 贡献指南

### 提交问题
1. 在GitHub Issues中描述问题
2. 提供复现步骤
3. 提供相关日志和截图

### 提交代码
1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 开发规范
- 遵循PEP 8代码规范
- 添加适当的注释
- 编写单元测试
- 更新相关文档

## 📄 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

**重要提示**: 本技能提供的分析结果仅供参考，不构成投资建议。股票投资有风险，入市需谨慎。使用者应自行承担投资风险，开发者不对任何投资损失负责。

## 🙏 致谢

- [akshare](https://github.com/akfamily/akshare) - 提供优秀的股票数据接口
- [OpenClaw](https://openclaw.ai) - 优秀的AI助手平台
- 所有贡献者和用户

## 📞 支持与联系

- **GitHub Issues**: [提交问题](https://github.com/yourusername/stock-real-time-analysis/issues)
- **文档**: [查看完整文档](https://github.com/yourusername/stock-real-time-analysis/wiki)
- **讨论**: [加入讨论](https://github.com/yourusername/stock-real-time-analysis/discussions)

---

**如果这个技能对你有帮助，请给个⭐星标支持！**

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/stock-real-time-analysis&type=Date)](https://star-history.com/#yourusername/stock-real-time-analysis&Date)