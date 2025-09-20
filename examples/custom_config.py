#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNTM 自定义配置示例
演示如何创建和使用自定义配置文件
"""

import sys
import subprocess
import yaml
from pathlib import Path

def create_custom_config():
    """创建自定义配置文件"""
    config = {
        "FILE_SETTINGS": {
            "OUTPUT_DIR": "output/custom",
            "EXTENSION": "png",
            "NAME_FORMAT": 2,
            "FONTS": "ch"
        },
        "TEXT_SETTINGS": {
            "LANGUAGE": "ch",
            "CORPUS": "texts/sample_chinese.txt",
            "CORPUS_TYPE": "CORPUS", 
            "SIZE": 40,
            "COLOR": "(255, 0, 0)",  # 红色文字
            "STROKE_WIDTH": 2,
            "STROKE_FILL": "(0, 0, 0)",  # 黑色描边
            "HEIGHT": 0
        },
        "IMAGE_FORMAT_SETTINGS": {
            "WIDTH": 400,  # 固定宽度
            "ORIENTATION": 0,
            "SPACE_WIDTH": 1.2,
            "MARGINS": "10,15,10,15",  # 较大边距
            "FIT": False
        },
        "DISTORTION_SETTINGS": {
            "SKEW_ANGLE": 15,  # 较大倾斜角度
            "RANDOM_SKEW": True
        },
        "OTHER_SETTINGS": {
            "NUM_WORKERS": 4,
            "COUNT": 150
        }
    }
    
    config_path = Path("configs/custom_demo.yaml")
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    return config_path

def main():
    print("🚀 GNTM 自定义配置示例")
    print("这个示例展示如何创建和使用自定义配置")
    
    # 检查前置条件
    if not Path("texts/sample_chinese.txt").exists():
        print("❌ 请先运行 setup.py 创建示例文件")
        print("   python setup.py")
        return False
    
    print("\n⚙️ 创建自定义配置文件...")
    config_path = create_custom_config()
    print(f"✅ 配置文件已创建: {config_path}")
    
    print("\n📋 自定义配置特点:")
    print("   - 红色文字 + 黑色描边")
    print("   - 固定宽度 400px")
    print("   - 较大倾斜角度 (±15°)")
    print("   - PNG 高质量输出")
    print("   - 字体大小 40px")
    
    print(f"\n🔄 使用自定义配置生成图片...")
    
    cmd = [
        sys.executable, "run.py", 
        "--cfg", str(config_path),
        "--verbose"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ 自定义配置示例完成！")
        print("📁 请查看 output/custom/ 目录")
        print("💡 注意观察红色文字和黑色描边效果")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败：{e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
