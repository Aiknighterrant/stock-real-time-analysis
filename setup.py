#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票实时分析技能安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README.md内容
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements.txt内容
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='stock-real-time-analysis',
    version='1.0.0',
    description='OpenClaw股票实时分析技能 - 支持自动触发、实时数据获取、完整基本面分析',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='OpenClaw Community',
    author_email='',
    url='https://github.com/yourusername/stock-real-time-analysis',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords='stock, analysis, real-time, openclaw, skill, investment, finance',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'stock-analyzer=stock_real_time_analyzer:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/stock-real-time-analysis/issues',
        'Source': 'https://github.com/yourusername/stock-real-time-analysis',
        'Documentation': 'https://github.com/yourusername/stock-real-time-analysis/wiki',
    },
)