#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票实时分析技能接口
自动触发机制：单独输入股票名称或股票代码即触发分析
"""

import re
import sys
import os
from typing import Optional, Dict, Any

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stock_real_time_analyzer import OptimizedRealTimeStockAnalyzer


class StockAnalysisSkill:
    """
    股票分析技能接口
    支持自动触发：单独输入股票名称或股票代码即触发分析
    """
    
    def __init__(self):
        """初始化技能"""
        self.analyzer = OptimizedRealTimeStockAnalyzer(cache_ttl=300)
        self.stock_patterns = self._init_stock_patterns()
        
    def _init_stock_patterns(self) -> Dict[str, str]:
        """初始化股票模式识别"""
        # 股票代码模式
        patterns = {
            # A股代码模式
            r'^[0-9]{6}$': 'stock_code',  # 6位数字代码
            r'^[0-9]{5}$': 'stock_code',  # 5位数字代码（港股）
            
            # 股票名称模式（支持的核心股票）
            r'^(长飞光纤|贵州茅台|五粮液|宁德时代|比亚迪|中国平安|'
            r'招商银行|中信证券|东方财富|中芯国际|万科A|格力电器|'
            r'美的集团|海康威视|恒瑞医药|药明康德|隆基绿能|通威股份|'
            r'韦尔股份|腾讯控股|阿里巴巴|美团|京东|小米集团)$': 'stock_name',
            
            # 简写或别名
            r'^(茅台|平安|招行|中信|东财|中芯|腾讯|阿里|小米)$': 'stock_alias',
        }
        
        # 编译正则表达式
        compiled_patterns = {}
        for pattern, pattern_type in patterns.items():
            compiled_patterns[re.compile(pattern)] = pattern_type
            
        return compiled_patterns
    
    def is_stock_input(self, text: str) -> bool:
        """
        判断输入是否为股票名称或代码
        
        Args:
            text: 用户输入的文本
            
        Returns:
            是否为股票输入
        """
        if not text or not isinstance(text, str):
            return False
        
        text = text.strip()
        
        # 检查是否匹配股票模式
        for pattern, pattern_type in self.stock_patterns.items():
            if pattern.match(text):
                return True
        
        # 检查是否在股票映射表中
        stock_code = self.analyzer.get_stock_code(text)
        if stock_code:
            return True
        
        return False
    
    def get_stock_info(self, text: str) -> Optional[Dict[str, Any]]:
        """
        获取股票信息
        
        Args:
            text: 股票名称或代码
            
        Returns:
            股票信息字典
        """
        text = text.strip()
        
        # 获取股票代码
        stock_code = self.analyzer.get_stock_code(text)
        if not stock_code:
            # 尝试直接作为代码
            if text.isdigit() and len(text) in [5, 6]:
                stock_code = text
            else:
                return None
        
        # 获取股票名称
        stock_name = self.analyzer.get_stock_name(stock_code)
        if not stock_name:
            stock_name = text  # 使用输入作为名称
        
        return {
            'code': stock_code,
            'name': stock_name,
            'input': text
        }
    
    def analyze_stock(self, text: str) -> Dict[str, Any]:
        """
        分析股票
        
        Args:
            text: 股票名称或代码
            
        Returns:
            分析结果
        """
        try:
            print(f"🔍 检测到股票输入: {text}")
            print("📊 开始实时分析...")
            
            # 使用分析器进行分析
            result = self.analyzer.analyze_stock_efficient(text)
            
            if 'error' in result:
                return {
                    'success': False,
                    'error': result['error'],
                    'input': text
                }
            
            # 生成格式化报告
            report = self.analyzer.format_analysis_report_efficient(result)
            
            return {
                'success': True,
                'input': text,
                'stock_code': result.get('stock_code'),
                'stock_name': result.get('stock_name'),
                'report': report,
                'raw_data': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"分析失败: {str(e)}",
                'input': text
            }
    
    def format_response(self, analysis_result: Dict[str, Any]) -> str:
        """
        格式化响应
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            格式化响应文本
        """
        if not analysis_result.get('success'):
            error_msg = analysis_result.get('error', '未知错误')
            return f"❌ 股票分析失败: {error_msg}\n\n输入: {analysis_result.get('input', '未知')}"
        
        # 直接返回分析报告
        report = analysis_result.get('report', '')
        
        # 添加简短说明
        response = f"📈 已为您分析: {analysis_result.get('stock_name')} ({analysis_result.get('stock_code')})\n\n"
        response += report
        
        return response
    
    def process_input(self, text: str) -> Optional[str]:
        """
        处理用户输入
        
        Args:
            text: 用户输入的文本
            
        Returns:
            分析报告或None（如果不是股票输入）
        """
        # 清理输入
        text = text.strip()
        
        # 检查是否为股票输入
        if not self.is_stock_input(text):
            return None
        
        # 分析股票
        result = self.analyze_stock(text)
        
        # 格式化响应
        return self.format_response(result)


# 全局技能实例
_skill_instance = None

def get_skill() -> StockAnalysisSkill:
    """获取技能实例（单例）"""
    global _skill_instance
    if _skill_instance is None:
        _skill_instance = StockAnalysisSkill()
    return _skill_instance


def should_trigger(text: str) -> bool:
    """
    判断是否应该触发股票分析技能
    
    Args:
        text: 用户输入的文本
        
    Returns:
        是否触发
    """
    skill = get_skill()
    return skill.is_stock_input(text)


def trigger_analysis(text: str) -> str:
    """
    触发股票分析
    
    Args:
        text: 股票名称或代码
        
    Returns:
        分析报告
    """
    skill = get_skill()
    return skill.process_input(text) or "❌ 无法分析该股票"


# 测试函数
def test_skill():
    """测试技能接口"""
    print("🧪 测试股票分析技能接口")
    print("=" * 50)
    
    skill = StockAnalysisSkill()
    
    test_cases = [
        "中芯国际",
        "688981",
        "贵州茅台",
        "600519",
        "五粮液", 
        "000858",
        "长飞光纤",
        "601869",
        "不是股票",
        "随机文本"
    ]
    
    for test_input in test_cases:
        print(f"\n📋 测试输入: '{test_input}'")
        
        # 测试是否为股票输入
        is_stock = skill.is_stock_input(test_input)
        print(f"   是否为股票输入: {'✅ 是' if is_stock else '❌ 否'}")
        
        if is_stock:
            # 测试分析
            result = skill.analyze_stock(test_input)
            if result.get('success'):
                print(f"   分析结果: ✅ 成功")
                print(f"   股票: {result.get('stock_name')} ({result.get('stock_code')})")
            else:
                print(f"   分析结果: ❌ 失败")
                print(f"   错误: {result.get('error')}")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")


if __name__ == "__main__":
    # 运行测试
    test_skill()