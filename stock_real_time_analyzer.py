#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版实时股票分析器
只搜索用户输入的股票的实时信息，不获取全部股票
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import sys
import traceback
from typing import Dict, List, Optional, Tuple, Any


class OptimizedRealTimeStockAnalyzer:
    """
    优化版实时股票分析器
    只搜索指定股票的实时信息
    """
    
    def __init__(self, cache_ttl: int = 300):
        """
        初始化分析器
        
        Args:
            cache_ttl: 缓存时间（秒），默认5分钟
        """
        self.cache_ttl = cache_ttl
        self.cache = {}
        self.stock_mapping = self._load_stock_mapping()
        
    def _load_stock_mapping(self) -> Dict[str, str]:
        """加载股票名称-代码映射"""
        mapping = {
            # A股核心股票
            '贵州茅台': '600519',
            '茅台': '600519',
            '五粮液': '000858',
            '宁德时代': '300750',
            '比亚迪': '002594',
            '中国平安': '601318',
            '长飞光纤': '601869',
            '招商银行': '600036',
            '中信证券': '600030',
            '东方财富': '300059',
            '万科A': '000002',
            '格力电器': '000651',
            '美的集团': '000333',
            '海康威视': '002415',
            '恒瑞医药': '600276',
            '药明康德': '603259',
            '隆基绿能': '601012',
            '通威股份': '600438',
            '中芯国际': '688981',
            '韦尔股份': '603501',
            
            # 港股（可选）
            '腾讯控股': '00700',
            '阿里巴巴': '09988',
            '美团': '03690',
            '京东': '09618',
            '小米集团': '01810',
        }
        return mapping
    
    def get_stock_code(self, stock_input: str) -> Optional[str]:
        """
        解析股票代码
        
        Args:
            stock_input: 股票代码或名称
            
        Returns:
            标准化的股票代码
        """
        # 如果输入是纯数字，假设是股票代码
        if stock_input.isdigit():
            if len(stock_input) == 6:  # A股代码
                return stock_input
            elif len(stock_input) == 5 and stock_input.startswith('0'):  # 港股
                return stock_input
        
        # 从映射中查找
        return self.stock_mapping.get(stock_input)
    
    def get_stock_name(self, stock_code: str) -> Optional[str]:
        """获取股票名称"""
        # 反向映射
        reverse_mapping = {v: k for k, v in self.stock_mapping.items()}
        return reverse_mapping.get(stock_code)
    
    def get_real_time_quote_single(self, stock_code: str) -> Dict[str, Any]:
        """
        只获取指定股票的实时行情（不获取全部股票）
        
        Args:
            stock_code: 股票代码
            
        Returns:
            实时行情字典
        """
        cache_key = f"quote_{stock_code}"
        if cache_key in self.cache and time.time() - self.cache[cache_key]['timestamp'] < self.cache_ttl:
            return self.cache[cache_key]['data']
        
        try:
            print(f"🔍 正在获取 {stock_code} 实时行情...")
            
            # 方法1: 使用单只股票接口（如果可用）
            try:
                # 尝试使用单只股票接口
                if stock_code.startswith('6'):
                    market = 'sh'
                elif stock_code.startswith('0') or stock_code.startswith('3'):
                    market = 'sz'
                else:
                    market = ''
                
                # 使用akshare的单只股票接口
                single_stock_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date="20260101", end_date="20260416", adjust="")
                if not single_stock_df.empty:
                    latest = single_stock_df.iloc[-1]
                    result = {
                        'code': stock_code,
                        'name': self.get_stock_name(stock_code) or stock_code,
                        'current_price': float(latest.get('收盘', 0)),
                        'open': float(latest.get('开盘', 0)),
                        'high': float(latest.get('最高', 0)),
                        'low': float(latest.get('最低', 0)),
                        'volume': int(latest.get('成交量', 0)),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # 缓存结果
                    self.cache[cache_key] = {
                        'data': result,
                        'timestamp': time.time()
                    }
                    
                    print(f"✅ 获取 {stock_code} 实时行情成功 (单只股票接口)")
                    return result
            except Exception as e:
                print(f"   ⚠️ 单只股票接口失败: {str(e)[:50]}...")
            
            # 方法2: 使用spot_em接口（更高效）
            try:
                spot_df = ak.stock_zh_a_spot_em()
                if not spot_df.empty:
                    # 查找指定股票
                    target_df = spot_df[spot_df['代码'] == stock_code]
                    if target_df.empty:
                        # 尝试带市场前缀
                        if stock_code.startswith('6'):
                            target_df = spot_df[spot_df['代码'] == f"sh{stock_code}"]
                        elif stock_code.startswith('0') or stock_code.startswith('3'):
                            target_df = spot_df[spot_df['代码'] == f"sz{stock_code}"]
                    
                    if not target_df.empty:
                        row = target_df.iloc[0]
                        result = {
                            'code': stock_code,
                            'name': row.get('名称', self.get_stock_name(stock_code) or stock_code),
                            'current_price': float(row.get('最新价', 0)),
                            'change': float(row.get('涨跌额', 0)),
                            'change_percent': float(row.get('涨跌幅', 0)),
                            'open': float(row.get('今开', 0)),
                            'high': float(row.get('最高', 0)),
                            'low': float(row.get('最低', 0)),
                            'volume': int(row.get('成交量', 0)),
                            'turnover': float(row.get('成交额', 0)),
                            'amplitude': float(row.get('振幅', 0)),
                            'turnover_rate': float(row.get('换手率', 0)),
                            'pe_ttm': float(row.get('市盈率-动态', 0) or row.get('市盈率', 0)),
                            'pb': float(row.get('市净率', 0)),
                            'market_cap': float(row.get('总市值', 0)),
                            'circulating_market_cap': float(row.get('流通市值', 0)),
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # 缓存结果
                        self.cache[cache_key] = {
                            'data': result,
                            'timestamp': time.time()
                        }
                        
                        print(f"✅ 获取 {stock_code} 实时行情成功 (spot_em接口)")
                        return result
            except Exception as e:
                print(f"   ⚠️ spot_em接口失败: {str(e)[:50]}...")
            
            # 方法3: 作为最后手段，使用完整列表但只提取需要的股票
            print("   ⚠️ 使用完整列表接口（最后手段）...")
            stock_zh_a_spot_df = ak.stock_zh_a_spot()
            
            # 查找指定股票
            if stock_code.startswith('6'):
                code_with_prefix = f"sh{stock_code}"
            elif stock_code.startswith('0') or stock_code.startswith('3'):
                code_with_prefix = f"sz{stock_code}"
            else:
                code_with_prefix = stock_code
            
            stock_data = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'] == code_with_prefix]
            
            if stock_data.empty:
                # 尝试不带前缀查找
                stock_data = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'] == stock_code]
            
            if stock_data.empty:
                # 尝试通过名称查找
                stock_name = self.get_stock_name(stock_code)
                if stock_name:
                    stock_data = stock_zh_a_spot_df[stock_zh_a_spot_df['名称'] == stock_name]
            
            if stock_data.empty:
                return {"error": f"未找到股票 {stock_code} 的实时行情"}
            
            # 提取数据
            data = stock_data.iloc[0].to_dict()
            
            result = {
                'code': stock_code,
                'name': data.get('名称', self.get_stock_name(stock_code) or stock_code),
                'current_price': float(data.get('最新价', 0)),
                'change': float(data.get('涨跌额', 0)),
                'change_percent': float(data.get('涨跌幅', 0)),
                'open': float(data.get('今开', 0)),
                'high': float(data.get('最高', 0)),
                'low': float(data.get('最低', 0)),
                'volume': int(data.get('成交量', 0)),
                'turnover': float(data.get('成交额', 0)),
                'amplitude': float(data.get('振幅', 0)),
                'turnover_rate': float(data.get('换手率', 0)),
                'pe_ttm': float(data.get('市盈率-动态', 0) or data.get('市盈率', 0)),
                'pb': float(data.get('市净率', 0)),
                'market_cap': float(data.get('总市值', 0)),
                'circulating_market_cap': float(data.get('流通市值', 0)),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 缓存结果
            self.cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            print(f"✅ 获取 {stock_code} 实时行情成功 (完整列表接口)")
            return result
            
        except Exception as e:
            error_msg = f"获取实时行情失败: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def get_financial_data_efficient(self, stock_code: str) -> Dict[str, Any]:
        """
        高效获取财务数据（只获取必要数据）
        
        Args:
            stock_code: 股票代码
            
        Returns:
            财务数据字典
        """
        cache_key = f"financial_{stock_code}"
        if cache_key in self.cache and time.time() - self.cache[cache_key]['timestamp'] < self.cache_ttl:
            return self.cache[cache_key]['data']
        
        try:
            print(f"📊 正在获取 {stock_code} 财务数据...")
            
            financial_data = {}
            
            # 只获取必要的财务指标
            try:
                # 获取财务指标（最新一期）
                financial_df = ak.stock_financial_analysis_indicator(symbol=stock_code)
                if not financial_df.empty:
                    latest = financial_df.iloc[-1].to_dict()
                    
                    # 只提取关键指标
                    key_indicators = {
                        '基本每股收益': latest.get('基本每股收益', 0),
                        '每股净资产': latest.get('每股净资产', 0),
                        '净资产收益率': latest.get('净资产收益率', 0),
                        '销售毛利率': latest.get('销售毛利率', 0),
                        '销售净利率': latest.get('销售净利率', 0),
                        '营业总收入': latest.get('营业总收入', 0),
                        '净利润': latest.get('净利润', 0),
                        '营业总收入同比增长率': latest.get('营业总收入同比增长率', 0),
                        '净利润同比增长率': latest.get('净利润同比增长率', 0),
                        '报告日期': latest.get('报告日期', '')
                    }
                    
                    financial_data['indicators'] = key_indicators
                    print(f"   ✅ 获取财务指标成功")
            except Exception as e:
                print(f"   ⚠️ 财务指标获取失败: {str(e)[:50]}...")
            
            # 如果财务指标获取失败，尝试获取基本信息
            if not financial_data:
                try:
                    stock_info_df = ak.stock_individual_info_em(symbol=stock_code)
                    if not stock_info_df.empty:
                        info_dict = {}
                        for _, row in stock_info_df.iterrows():
                            key = row['item']
                            value = row['value']
                            # 只存储关键信息
                            if any(kw in key for kw in ['每股收益', '每股净资产', '净资产收益率', '市盈率', '市净率']):
                                info_dict[key] = value
                        
                        if info_dict:
                            financial_data['basic_info'] = info_dict
                            print(f"   ✅ 获取基本信息成功")
                except Exception as e:
                    print(f"   ⚠️ 基本信息获取失败: {str(e)[:50]}...")
            
            if not financial_data:
                return {"error": "无法获取财务数据"}
            
            result = {
                'code': stock_code,
                'data': financial_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 缓存结果（财务数据缓存时间更长）
            self.cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            print(f"✅ 获取 {stock_code} 财务数据成功")
            return result
            
        except Exception as e:
            error_msg = f"获取财务数据失败: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def calculate_valuation_efficient(self, stock_code: str) -> Dict[str, Any]:
        """
        高效计算估值指标
        
        Args:
            stock_code: 股票代码
            
        Returns:
            估值指标字典
        """
        try:
            # 获取实时行情（高效版本）
            quote_data = self.get_real_time_quote_single(stock_code)
            if 'error' in quote_data:
                return quote_data
            
            # 获取财务数据（高效版本）
            financial_data = self.get_financial_data_efficient(stock_code)
            if 'error' in financial_data:
                # 如果财务数据获取失败，使用默认值
                financial_dict = {}
            else:
                financial_dict = financial_data.get('data', {})
            
            # 提取关键数据
            current_price = quote_data.get('current_price', 0)
            market_cap = quote_data.get('market_cap', 0)
            
            # 从财务数据中提取关键指标
            indicators = financial_dict.get('indicators', {})
            basic_info = financial_dict.get('basic_info', {})
            
            # 提取EPS
            eps = indicators.get('基本每股收益', 0)
            if not eps and basic_info:
                for key, value in basic_info.items():
                    if '每股收益' in key:
                        try:
                            eps = float(value) if value else 0
                            break
                        except:
                            pass
            
            # 提取每股净资产
            net_assets_per_share = indicators.get('每股净资产', 0)
            if not net_assets_per_share and basic_info:
                for key, value in basic_info.items():
                    if '每股净资产' in key:
                        try:
                            net_assets_per_share = float(value) if value else 0
                            break
                        except:
                            pass
            
            # 提取其他指标
            revenue = indicators.get('营业总收入', 0)
            net_profit = indicators.get('净利润', 0)
            roe = indicators.get('净资产收益率', 0)
            gross_margin = indicators.get('销售毛利率', 0)
            net_margin = indicators.get('销售净利率', 0)
            revenue_growth = indicators.get('营业总收入同比增长率', 0)
            profit_growth = indicators.get('净利润同比增长率', 0)
            
            # 计算估值比率
            pe = current_price / eps if eps > 0 else 0
            pb = current_price / net_assets_per_share if net_assets_per_share > 0 else 0
            ps = market_cap / revenue if revenue > 0 else 0
            peg = pe / profit_growth if profit_growth > 0 else 0
            
            # 如果从行情数据中获取了PE/PB，优先使用
            pe_ttm = quote_data.get('pe_ttm', 0)
            pb_quote = quote_data.get('pb', 0)
            
            if pe_ttm > 0:
                pe = pe_ttm
            if pb_quote > 0:
                pb = pb_quote
            
            result = {
                'code': stock_code,
                'name': quote_data.get('name', self.get_stock_name(stock_code) or stock_code),
                'current_price': current_price,
                'market_cap': market_cap,
                'pe': round(pe, 2),
                'pb': round(pb, 2),
                'ps': round(ps, 2),
                'peg': round(peg, 2),
                'roe': round(roe, 2),
                'gross_margin': round(gross_margin, 2),
                'net_margin': round(net_margin, 2),
                'eps': round(eps, 2),
                'revenue': round(revenue, 2),
                'net_profit': round(net_profit, 2),
                'revenue_growth': round(revenue_growth, 2),
                'profit_growth': round(profit_growth, 2),
                'net_assets_per_share': round(net_assets_per_share, 2),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
            
        except Exception as e:
            return {"error": f"计算估值指标失败: {str(e)}"}
    
    def analyze_stock_efficient(self, stock_input: str) -> Dict[str, Any]:
        """
        高效分析股票（只搜索指定股票）
        
        Args:
            stock_input: 股票代码或名称
            
        Returns:
            分析结果字典
        """
        try:
            # 解析股票代码
            stock_code = self.get_stock_code(stock_input)
            if not stock_code:
                return {"error": f"无法识别股票: {stock_input}"}
            
            print(f"🔍 开始分析 {stock_input} ({stock_code})")
            print("=" * 50)
            
            # 获取估值指标（高效版本）
            print("📈 计算估值指标...")
            valuation_data = self.calculate_valuation_efficient(stock_code)
            if 'error' in valuation_data:
                return valuation_data
            
            # 获取实时行情（高效版本）
            print("💰 获取实时行情...")
            quote_data = self.get_real_time_quote_single(stock_code)
            
            # 生成分析报告
            print("📊 生成分析报告...")
            analysis = self._generate_efficient_analysis(valuation_data, quote_data)
            
            result = {
                'stock_code': stock_code,
                'stock_name': valuation_data.get('name', ''),
                'valuation': valuation_data,
                'quote': quote_data,
                'analysis': analysis,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print("✅ 分析完成")
            print("=" * 50)
            
            return result
            
        except Exception as e:
            error_msg = f"分析失败: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def _generate_efficient_analysis(self, valuation_data: Dict, quote_data: Dict) -> Dict[str, Any]:
        """生成高效分析报告"""
        # 风险评估
        risk_assessment = self._assess_risk_efficient(valuation_data)
        
        # 投资建议
        investment_advice = self._generate_investment_advice_efficient(valuation_data, risk_assessment)
        
        # 技术分析
        technical_analysis = self._technical_analysis_efficient(quote_data)
        
        # 基本面分析
        fundamental_analysis = self._fundamental_analysis_efficient(valuation_data)
        
        # 生成总结
        summary = self._generate_summary_efficient(valuation_data, risk_assessment, investment_advice)
        
        return {
            'risk_assessment': risk_assessment,
            'investment_advice': investment_advice,
            'technical_analysis': technical_analysis,
            'fundamental_analysis': fundamental_analysis,
            'summary': summary
        }
    
    def _assess_risk_efficient(self, valuation_data: Dict) -> Dict[str, Any]:
        """高效风险评估"""
        pe = valuation_data.get('pe', 0)
        pb = valuation_data.get('pb', 0)
        roe = valuation_data.get('roe', 0)
        
        # PE风险评估
        if pe == 0:
            pe_risk = '数据不足'
        elif pe > 100:
            pe_risk = '极高风险'
        elif pe > 50:
            pe_risk = '高风险'
        elif pe > 30:
            pe_risk = '中等风险'
        elif pe > 15:
            pe_risk = '低风险'
        else:
            pe_risk = '很低风险'
        
        # PB风险评估
        if pb == 0:
            pb_risk = '数据不足'
        elif pb > 10:
            pb_risk = '极高风险'
        elif pb > 5:
            pb_risk = '高风险'
        elif pb > 3:
            pb_risk = '中等风险'
        elif pb > 1:
            pb_risk = '低风险'
        else:
            pb_risk = '很低风险'
        
        # ROE评估
        if roe == 0:
            roe_quality = '数据不足'
        elif roe > 20:
            roe_quality = '优秀'
        elif roe > 15:
            roe_quality = '良好'
        elif roe > 10:
            roe_quality = '中等'
        elif roe > 5:
            roe_quality = '一般'
        else:
            roe_quality = '较差'
        
        # 总体风险评估
        if pe_risk in ['极高风险', '高风险'] or pb_risk in ['极高风险', '高风险']:
            overall_risk = '高风险'
        elif pe_risk == '中等风险' or pb_risk == '中等风险':
            overall_risk = '中等风险'
        else:
            overall_risk = '低风险'
        
        return {
            'pe_risk': pe_risk,
            'pb_risk': pb_risk,
            'roe_quality': roe_quality,
            'overall_risk': overall_risk
        }
    
    def _generate_investment_advice_efficient(self, valuation_data: Dict, risk_assessment: Dict) -> Dict[str, Any]:
        """高效投资建议"""
        pe = valuation_data.get('pe', 0)
        overall_risk = risk_assessment.get('overall_risk', '未知')
        
        advice = {
            'short_term': '',
            'action': '',
            'confidence': 0
        }
        
        if pe == 0:
            advice['short_term'] = '数据不足，建议谨慎'
            advice['action'] = '观望'
            advice['confidence'] = 30
        
        elif overall_risk == '高风险':
            advice['short_term'] = '估值过高，存在回调风险'
            advice['action'] = '卖出或观望'
            advice['confidence'] = 70
        
        elif overall_risk == '中等风险':
            advice['short_term'] = '估值合理，可适当关注'
            advice['action'] = '持有或小幅加仓'
            advice['confidence'] = 60
        
        else:  # 低风险
            advice['short_term'] = '估值较低，存在机会'
            advice['action'] = '买入或加仓'
            advice['confidence'] = 75
        
        return advice
    
    def _technical_analysis_efficient(self, quote_data: Dict) -> Dict[str, Any]:
        """高效技术分析"""
        if 'error' in quote_data:
            return {"error": quote_data['error']}
        
        change_percent = quote_data.get('change_percent', 0)
        turnover_rate = quote_data.get('turnover_rate', 0)
        
        # 趋势分析
        if change_percent > 3:
            trend = '强势上涨'
        elif change_percent > 1:
            trend = '温和上涨'
        elif change_percent > -1:
            trend = '横盘整理'
        elif change_percent > -3:
            trend = '温和下跌'
        else:
            trend = '大幅下跌'
        
        # 流动性分析
        if turnover_rate > 5:
            liquidity = '活跃'
        elif turnover_rate > 2:
            liquidity = '一般'
        else:
            liquidity = '清淡'
        
        return {
            'trend': trend,
            'liquidity': liquidity,
            'change_percent': change_percent,
            'turnover_rate': turnover_rate
        }
    
    def _fundamental_analysis_efficient(self, valuation_data: Dict) -> Dict[str, Any]:
        """高效基本面分析"""
        pe = valuation_data.get('pe', 0)
        roe = valuation_data.get('roe', 0)
        revenue_growth = valuation_data.get('revenue_growth', 0)
        
        # 盈利能力分析
        if roe > 15:
            profitability = '优秀'
        elif roe > 10:
            profitability = '良好'
        elif roe > 5:
            profitability = '一般'
        else:
            profitability = '较差'
        
        # 成长性分析
        if revenue_growth > 20:
            growth = '高速成长'
        elif revenue_growth > 10:
            growth = '稳健成长'
        elif revenue_growth > 0:
            growth = '缓慢成长'
        else:
            growth = '成长停滞'
        
        # 估值合理性
        if pe < 15:
            valuation = '低估'
        elif pe < 30:
            valuation = '合理'
        elif pe < 50:
            valuation = '偏高'
        else:
            valuation = '高估'
        
        return {
            'profitability': profitability,
            'growth': growth,
            'valuation': valuation,
            'roe': roe,
            'revenue_growth': revenue_growth
        }
    
    def _generate_summary_efficient(self, valuation_data: Dict, risk_assessment: Dict, investment_advice: Dict) -> str:
        """高效总结生成"""
        name = valuation_data.get('name', '')
        pe = valuation_data.get('pe', 0)
        pb = valuation_data.get('pb', 0)
        roe = valuation_data.get('roe', 0)
        overall_risk = risk_assessment.get('overall_risk', '未知')
        action = investment_advice.get('action', '')
        
        summary = f"📌 {name} 实时分析总结\n"
        summary += "=" * 40 + "\n"
        summary += f"• 估值: PE={pe:.1f}倍, PB={pb:.1f}倍\n"
        summary += f"• 盈利: ROE={roe:.1f}%\n"
        summary += f"• 风险: {overall_risk}\n"
        summary += f"• 建议: {action}\n"
        
        if pe > 50:
            summary += "⚠️ 估值偏高，建议谨慎\n"
        elif pe < 20:
            summary += "✅ 估值合理偏低，具备投资价值\n"
        
        return summary
    
    def format_analysis_report_efficient(self, analysis_result: Dict) -> str:
        """
        格式化高效分析报告
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            格式化的报告字符串
        """
        if 'error' in analysis_result:
            return f"❌ 错误: {analysis_result['error']}"
        
        stock_code = analysis_result.get('stock_code', '')
        stock_name = analysis_result.get('stock_name', '')
        valuation = analysis_result.get('valuation', {})
        quote = analysis_result.get('quote', {})
        analysis = analysis_result.get('analysis', {})
        timestamp = analysis_result.get('timestamp', '')
        
        report_lines = []
        report_lines.append(f"📈 {stock_name} ({stock_code}) 实时分析报告")
        report_lines.append("=" * 50)
        report_lines.append(f"📅 分析时间: {timestamp}")
        report_lines.append("")
        
        # 实时行情
        if 'error' not in quote:
            report_lines.append("💰 实时行情")
            report_lines.append(f"  • 价格: ¥{quote.get('current_price', 0):.2f}")
            report_lines.append(f"  • 涨跌: {quote.get('change_percent', 0):+.2f}%")
            report_lines.append(f"  • 成交: {quote.get('volume', 0):,}股")
            report_lines.append("")
        
        # 估值指标
        report_lines.append("📊 估值指标")
        report_lines.append(f"  • PE: {valuation.get('pe', 0):.1f}倍")
        report_lines.append(f"  • PB: {valuation.get('pb', 0):.1f}倍")
        report_lines.append(f"  • ROE: {valuation.get('roe', 0):.1f}%")
        report_lines.append("")
        
        # 盈利能力
        report_lines.append("💹 盈利能力")
        report_lines.append(f"  • 毛利率: {valuation.get('gross_margin', 0):.1f}%")
        report_lines.append(f"  • 净利率: {valuation.get('net_margin', 0):.1f}%")
        report_lines.append(f"  • 每股收益: ¥{valuation.get('eps', 0):.2f}")
        report_lines.append("")
        
        # 成长性
        report_lines.append("🚀 成长性")
        report_lines.append(f"  • 营收增长: {valuation.get('revenue_growth', 0):+.1f}%")
        report_lines.append(f"  • 利润增长: {valuation.get('profit_growth', 0):+.1f}%")
        report_lines.append("")
        
        # 风险分析
        risk_assessment = analysis.get('risk_assessment', {})
        report_lines.append("⚠️ 风险分析")
        report_lines.append(f"  • PE风险: {risk_assessment.get('pe_risk', '未知')}")
        report_lines.append(f"  • PB风险: {risk_assessment.get('pb_risk', '未知')}")
        report_lines.append(f"  • 总体风险: {risk_assessment.get('overall_risk', '未知')}")
        report_lines.append("")
        
        # 投资建议
        investment_advice = analysis.get('investment_advice', {})
        report_lines.append("🎯 投资建议")
        report_lines.append(f"  • 短期策略: {investment_advice.get('short_term', '')}")
        report_lines.append(f"  • 操作建议: {investment_advice.get('action', '')}")
        report_lines.append(f"  • 信心指数: {investment_advice.get('confidence', 0)}%")
        report_lines.append("")
        
        # 总结
        report_lines.append("📌 总结")
        report_lines.append(analysis.get('summary', ''))
        report_lines.append("")
        report_lines.append("=" * 50)
        report_lines.append("⚠️ 免责声明: 以上分析基于实时数据，仅供参考。")
        report_lines.append("   投资有风险，入市需谨慎。")
        
        return "\n".join(report_lines)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python stock_real_time_analyzer.py <股票代码或名称>")
        print("示例: python stock_real_time_analyzer.py 601869")
        print("示例: python stock_real_time_analyzer.py 长飞光纤")
        print("示例: python stock_real_time_analyzer.py 贵州茅台")
        sys.exit(1)
    
    stock_input = sys.argv[1]
    
    print(f"🔍 正在分析 {stock_input}...")
    print("=" * 50)
    
    analyzer = OptimizedRealTimeStockAnalyzer()
    result = analyzer.analyze_stock_efficient(stock_input)
    
    if 'error' in result:
        print(f"❌ 错误: {result['error']}")
        sys.exit(1)
    
    report = analyzer.format_analysis_report_efficient(result)
    print(report)
    
    # 保存详细数据
    output_file = f"/tmp/stock_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"📁 详细数据已保存到: {output_file}")


if __name__ == "__main__":
    main()