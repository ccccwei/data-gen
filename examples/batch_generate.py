#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNTM 批量生成示例
演示如何批量生成不同语言和样式的数据集
"""

import sys
import subprocess
from pathlib import Path
import time

def generate_dataset(name, **kwargs):
    """生成单个数据集"""
    print(f"\n🔄 生成 {name} 数据集...")
    
    # 构建命令
    cmd = [sys.executable, "run.py"]
    
    for key, value in kwargs.items():
        cmd.extend([f"--{key}", str(value)])
    
    try:
        start_time = time.time()
        subprocess.run(cmd, check=True)
        duration = time.time() - start_time
        print(f"✅ {name} 数据集生成完成 (用时: {duration:.2f}秒)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} 数据集生成失败：{e}")
        return False

def main():
    print("🚀 GNTM 批量生成示例")
    print("这个脚本将生成多个不同样式的数据集")
    
    # 检查前置条件
    if not Path("texts/sample_chinese.txt").exists():
        print("❌ 请先运行 setup.py 创建示例文件")
        print("   python setup.py")
        return False
    
    # 数据集配置
    datasets = [
        {
            "name": "中文小字体",
            "language": "ch",
            "fonts": "ch",
            "corpus": "texts/sample_chinese.txt",
            "size": 24,
            "count": 200,
            "output_dir": "output/chinese_small"
        },
        {
            "name": "中文大字体",
            "language": "ch", 
            "fonts": "ch",
            "corpus": "texts/sample_chinese.txt",
            "size": 48,
            "count": 200,
            "output_dir": "output/chinese_large"
        },
        {
            "name": "英文数据集",
            "language": "en",
            "fonts": "en", 
            "corpus": "texts/sample_english.txt",
            "size": 32,
            "count": 200,
            "output_dir": "output/english"
        },
        {
            "name": "高质量PNG",
            "language": "ch",
            "fonts": "ch",
            "corpus": "texts/sample_chinese.txt",
            "size": 64,
            "extension": "png",
            "count": 100,
            "output_dir": "output/high_quality"
        }
    ]
    
    print(f"\n📋 计划生成 {len(datasets)} 个数据集")
    
    success_count = 0
    total_start_time = time.time()
    
    for dataset in datasets:
        name = dataset.pop("name")
        if generate_dataset(name, **dataset):
            success_count += 1
    
    total_duration = time.time() - total_start_time
    
    print(f"\n🎉 批量生成完成！")
    print(f"✅ 成功: {success_count}/{len(datasets)} 个数据集")
    print(f"⏱️ 总用时: {total_duration:.2f} 秒")
    
    if success_count > 0:
        print(f"\n📁 查看结果:")
        print(f"   ls output/")
        print(f"   find output/ -name '*.jpg' | wc -l  # 统计图片数量")
    
    return success_count == len(datasets)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
