#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级分析示例
演示如何使用股票实时分析技能进行高级分析
"""

import sys
import os
import json
from datetime import datetime, timedelta

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_real_time_analyzer import OptimizedRealTimeStockAnalyzer



class AdvancedStockAnalyzer:
    """高级股票分析器"""
    
    def __init__(self):
        self.analyzer = OptimizedRealTimeStockAnalyzer(cache_ttl=300)
        self.analysis_history = {}
    
    def analyze_multiple_stocks(self, stock_list):
        """分析多只股票"""
        print("📊 多股票分析")
        print("=" * 50)
        
        results = []
        
        for stock in stock_list:
            print(f"\n🔍 分析 {stock}:")
            
            result = self.analyzer.analyze_stock_efficient(stock)
            
            if 'error' in result:
                print(f"   ❌ 分析失败: {result['error'][:50]}...")
                continue
            
            # 记录分析结果
            stock_info = {
                'name': result.get('stock_name', stock),
                'code': result.get('stock_code', ''),
                'price': result.get('valuation', {}).get('current_price', 0),
                'pe': result.get('valuation', {}).get('pe', 0),
                'pb': result.get('valuation', {}).get('pb', 0),
                'roe': result.get('valuation', {}).get('roe', 0),
                'timestamp': result.get('timestamp', ''),
            }
            
            results.append(stock_info)
            
            print(f"   ✅ 分析成功")
            print(f"      价格: ¥{stock_info['price']:.2f}")
            print(f"      PE: {stock_info['pe']:.1f}倍")
            print(f"      PB: {stock_info['pb']:.1f}倍")
            print(f"      ROE: {stock_info['roe']:.1f}%")
        
        # 保存分析结果
        self.analysis_history[datetime.now().strftime('%Y%m%d_%H%M%S')] = {
            'stocks': stock_list,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def compare_stocks(self, stock_list):
        """比较多只股票"""
        print("\n" + "=" * 50)
        print("📈 股票比较分析")
        print("=" * 50)
        
        results = self.analyze_multiple_stocks(stock_list)
        
        if not results:
            print("❌ 没有有效分析结果")
            return
        
        # 按PE排序
        sorted_by_pe = sorted(results, key=lambda x: x['pe'])
        
        print("\n🏆 PE排名 (低到高):")
        print("-" * 40)
        for i, stock in enumerate(sorted_by_pe, 1):
            print(f"  {i}. {stock['name']} ({stock['code']}): {stock['pe']:.1f}倍")
        
        # 按ROE排序
        sorted_by_roe = sorted(results, key=lambda x: x['roe'], reverse=True)
        
        print("\n🏆 ROE排名 (高到低):")
        print("-" * 40)
        for i, stock in enumerate(sorted_by_roe, 1):
            print(f"  {i}. {stock['name']} ({stock['code']}): {stock['roe']:.1f}%")
        
        # 计算平均指标
        avg_pe = sum(s['pe'] for s in results) / len(results)
        avg_pb = sum(s['pb'] for s in results) / len(results)
        avg_roe = sum(s['roe'] for s in results) / len(results)
        
        print("\n📊 平均指标:")
        print("-" * 40)
        print(f"  • 平均PE: {avg_pe:.1f}倍")
        print(f"  • 平均PB: {avg_pb:.1f}倍")
        print(f"  • 平均ROE: {avg_roe:.1f}%")
        
        # 找出最便宜和最贵的股票
        cheapest = min(results, key=lambda x: x['price'])
        most_expensive = max(results, key=lambda x: x['price'])
        
        print("\n💰 价格分析:")
        print("-" * 40)
        print(f"  • 最便宜: {cheapest['name']} - ¥{cheapest['price']:.2f}")
        print(f"  • 最贵: {most_expensive['name']} - ¥{most_expensive['price']:.2f}")
        print(f"  • 价格比: {most_expensive['price']/cheapest['price']:.1f}倍")
        
        return results
    
    def generate_analysis_report(self, stock_list):
        """生成分析报告"""
        print("\n" + "=" * 50)
        print("📋 生成详细分析报告")
        print("=" * 50)
        
        results = self.analyze_multiple_stocks(stock_list)
        
        if not results:
            print("❌ 没有有效分析结果")
            return
        
        # 创建报告
        report = {
            'report_id': f"stock_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'analyzed_stocks': len(results),
            'analysis_date': datetime.now().strftime('%Y年%m月%d日'),
            'stocks': results,
            'summary': {
                'total_stocks': len(results),
                'avg_pe': sum(s['pe'] for s in results) / len(results),
                'avg_pb': sum(s['pb'] for s in results) / len(results),
                'avg_roe': sum(s['roe'] for s in results) / len(results),
                'cheapest': min(results, key=lambda x: x['price'])['name'],
                'most_expensive': max(results, key=lambda x: x['price'])['name'],
            }
        }
        
        # 保存报告到文件
        report_file = f"stock_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 分析报告已生成: {report_file}")
        print(f"   分析股票数: {len(results)}")
        print(f"   报告ID: {report['report_id']}")
        
        # 显示报告摘要
        print("\n📌 报告摘要:")
        print("-" * 40)
        print(f"  • 分析时间: {report['analysis_date']}")
        print(f"  • 股票数量: {report['summary']['total_stocks']}")
        print(f"  • 平均PE: {report['summary']['avg_pe']:.1f}倍")
        print(f"  • 平均PB: {report['summary']['avg_pb']:.1f}倍")
        print(f"  • 平均ROE: {report['summary']['avg_roe']:.1f}%")
        print(f"  • 最便宜股票: {report['summary']['cheapest']}")
        print(f"  • 最贵股票: {report['summary']['most_expensive']}")
        
        return report
    
    def save_analysis_history(self):
        """保存分析历史"""
        if not self.analysis_history:
            print("❌ 没有分析历史")
            return
        
        history_file = f"stock_analysis_history_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_history, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 分析历史已保存: {history_file}")
        print(f"   分析记录数: {len(self.analysis_history)}")
        
        return history_file



def main():
    """主函数"""
    print("🚀 股票实时分析技能 - 高级使用示例")
    print("=" * 50)
    
    # 创建高级分析器
    advanced_analyzer = AdvancedStockAnalyzer()
    
    # 定义要分析的股票列表
    stock_list = [
        "中芯国际",
        "贵州茅台",
        "五粮液",
        "长飞光纤",
        "宁德时代",
        "比亚迪",
        "中国平安",
        "招商银行",
    ]
    
    print(f"📋 分析股票列表 ({len(stock_list)} 只):")
    print("-" * 40)
    for i, stock in enumerate(stock_list, 1):
        print(f"  {i}. {stock}")
    
    # 1. 多股票分析
    print("\n" + "=" * 50)
    print("1️⃣ 多股票分析")
    print("=" * 50)
    
    advanced_analyzer.analyze_multiple_stocks(stock_list)
    
    # 2. 股票比较分析

    print("\n" + "=" * 50)
    print("2️⃣ 股票比较分析")
    print("=" * 50)
    
    advanced_analyzer.compare_stocks(stock_list)
    
    # 3. 生成分析报告

    print("\n" + "=" * 50)
    print("3️⃣ 生成分析报告")
    print("=" * 50)
    
    advanced_analyzer.generate_analysis_report(stock_list)
    
    # 4. 保存分析历史

    print("\n" + "=" * 50)
    print("4️⃣ 保存分析历史")
    print("=" * 50)
    
    advanced_analyzer.save_analysis_history()
    
    print("\n" + "=" * 50)
    print("✅ 高级分析示例完成")
    print("=" * 50)
    
    print("\n🎯 高级功能总结:")
    print("-" * 40)
    print("1. 多股票批量分析")
    print("2. 股票间比较和排名")
    print("3. 详细报告生成")
    print("4. 分析历史保存")
    print("5. 数据导出和持久化")
    
    print("\n🔧 扩展应用:")
    print("-" * 40)
    print("• 投资组合分析")
    print("• 行业对比研究")
    print("• 历史数据分析")
    print("• 实时监控和预警")
    print("• 自动化交易策略")



if __name__ == "__main__":
    main()