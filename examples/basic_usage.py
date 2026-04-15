#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础使用示例
演示如何使用股票实时分析技能
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_real_time_analyzer import OptimizedRealTimeStockAnalyzer


def example_basic_analysis():
    """基础分析示例"""
    print("📈 股票实时分析 - 基础使用示例")
    print("=" * 50)
    
    # 创建分析器实例
    analyzer = OptimizedRealTimeStockAnalyzer(cache_ttl=300)
    
    # 分析中芯国际
    print("\n🔍 分析中芯国际:")
    result = analyzer.analyze_stock_efficient("中芯国际")
    
    if 'error' in result:
        print(f"❌ 分析失败: {result['error']}")
    else:
        print(f"✅ 分析成功")
        print(f"   股票: {result.get('stock_name')} ({result.get('stock_code')})")
        print(f"   分析时间: {result.get('timestamp', '未知')}")
        
        # 显示估值指标
        valuation = result.get('valuation', {})
        if valuation:
            print(f"   PE: {valuation.get('pe', 0):.1f}倍")
            print(f"   PB: {valuation.get('pb', 0):.1f}倍")
            print(f"   ROE: {valuation.get('roe', 0):.1f}%")
    
    # 分析贵州茅台
    print("\n🔍 分析贵州茅台:")
    result = analyzer.analyze_stock_efficient("贵州茅台")
    
    if 'error' in result:
        print(f"❌ 分析失败: {result['error']}")
    else:
        print(f"✅ 分析成功")
        print(f"   股票: {result.get('stock_name')} ({result.get('stock_code')})")
        
        # 显示估值指标
        valuation = result.get('valuation', {})
        if valuation:
            print(f"   当前价格: ¥{valuation.get('current_price', 0):.2f}")
            print(f"   PE: {valuation.get('pe', 0):.1f}倍")
            print(f"   PB: {valuation.get('pb', 0):.1f}倍")
    
    # 使用股票代码分析
    print("\n🔍 使用股票代码分析 (601869):")
    result = analyzer.analyze_stock_efficient("601869")
    
    if 'error' in result:
        print(f"❌ 分析失败: {result['error']}")
    else:
        print(f"✅ 分析成功")
        print(f"   股票: {result.get('stock_name')} ({result.get('stock_code')})")
    
    return True



def example_detailed_analysis():
    """详细分析示例"""
    print("\n" + "=" * 50)
    print("📊 详细分析示例")
    print("=" * 50)
    
    analyzer = OptimizedRealTimeStockAnalyzer()
    
    # 分析长飞光纤
    print("\n🔍 详细分析长飞光纤:")
    result = analyzer.analyze_stock_efficient("长飞光纤")
    
    if 'error' in result:
        print(f"❌ 分析失败: {result['error']}")
        return False
    
    # 生成详细报告
    report = analyzer.format_analysis_report_efficient(result)
    
    # 显示报告前10行
    print("📋 分析报告 (前10行):")
    print("-" * 40)
    lines = report.split('\n')
    for i, line in enumerate(lines[:10]):
        print(f"  {line}")
    
    # 显示关键指标
    print("\n📊 关键指标:")
    print("-" * 40)
    
    valuation = result.get('valuation', {})
    if valuation:
        print(f"  • 当前价格: ¥{valuation.get('current_price', 0):.2f}")
        print(f"  • 涨跌幅: {valuation.get('change_percent', 0):+.2f}%")
        print(f"  • PE: {valuation.get('pe', 0):.1f}倍")
        print(f"  • PB: {valuation.get('pb', 0):.1f}倍")
        print(f"  • ROE: {valuation.get('roe', 0):.1f}%")
        print(f"  • 毛利率: {valuation.get('gross_margin', 0):.1f}%")
        print(f"  • 净利率: {valuation.get('net_margin', 0):.1f}%")
    
    return True



def example_error_handling():
    """错误处理示例"""
    print("\n" + "=" * 50)
    print("⚠️ 错误处理示例")
    print("=" * 50)
    
    analyzer = OptimizedRealTimeStockAnalyzer()
    
    # 测试无效输入
    invalid_inputs = [
        ("不是股票", "无效股票名称"),
        ("1234567", "7位数字代码"),
        ("", "空输入"),
        ("今天天气不错", "普通文本"),
    ]
    
    print("\n🔍 测试无效输入:")
    for text, description in invalid_inputs:
        print(f"\n  输入: '{text}' ({description})")
        result = analyzer.analyze_stock_efficient(text)
        
        if 'error' in result:
            print(f"  结果: ❌ 正确识别为无效输入")
            print(f"  错误信息: {result['error'][:50]}...")
        else:
            print(f"  结果: ⚠️ 错误地识别为有效输入")
    
    return True



def main():
    """主函数"""
    print("🚀 股票实时分析技能 - 使用示例")
    print("=" * 50)
    
    # 运行所有示例
    examples = [
        ("基础分析示例", example_basic_analysis),
        ("详细分析示例", example_detailed_analysis),
        ("错误处理示例", example_error_handling),
    ]
    
    for name, func in examples:
        print(f"\n▶️ 运行: {name}")
        try:
            success = func()
            if success:
                print(f"✅ {name} 执行成功")
            else:
                print(f"❌ {name} 执行失败")
        except Exception as e:
            print(f"❌ {name} 执行异常: {str(e)[:50]}...")
    
    print("\n" + "=" * 50)
    print("✅ 所有示例执行完成")
    print("=" * 50)
    
    print("\n📋 使用总结:")
    print("-" * 40)
    print("1. 创建分析器: analyzer = OptimizedRealTimeStockAnalyzer()")
    print("2. 分析股票: result = analyzer.analyze_stock_efficient('股票名称/代码')")
    print("3. 生成报告: report = analyzer.format_analysis_report_efficient(result)")
    print("4. 支持多种输入: 名称、代码、简称")
    print("5. 自动触发: 单独输入股票信息即可")
    
    print("\n🎯 支持的股票:")
    print("-" * 40)
    print("• 中芯国际 (688981)")
    print("• 贵州茅台 (600519)")
    print("• 五粮液 (000858)")
    print("• 长飞光纤 (601869)")
    print("• 宁德时代 (300750)")
    print("• 比亚迪 (002594)")
    print("• 中国平安 (601318)")
    print("• 招商银行 (600036)")
    print("• 中信证券 (600030)")
    print("• 东方财富 (300059)")
    
    print("\n🔧 更多功能:")
    print("-" * 40)
    print("• 实时行情获取")
    print("• 财务指标分析")
    print("• 估值计算")
    print("• 风险评估")
    print("• 投资建议")
    print("• 格式化报告")



if __name__ == "__main__":
    main()