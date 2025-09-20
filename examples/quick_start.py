#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNTM 快速开始示例
演示最基本的使用方法
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 GNTM 快速开始示例")
    print("这个脚本将生成100张示例图片")
    
    # 检查是否已运行setup.py
    if not Path("texts/sample_chinese.txt").exists():
        print("❌ 请先运行 setup.py 创建示例文件")
        print("   python setup.py")
        return
    
    print("\n⚙️ 使用快速开始模式...")
    
    cmd = [
        sys.executable, "run.py",
        "--quick-start",
        "--verbose"
    ]
    
    try:
        print("🔄 正在生成...")
        subprocess.run(cmd, check=True)
        print("\n✅ 快速开始示例完成！")
        print("📁 请查看 output/images/ 目录")
        print("📄 标签文件: output/label.txt")
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败：{e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
