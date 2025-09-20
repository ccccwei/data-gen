#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNTM 自动化安装配置脚本
快速设置和配置 GNTM 项目环境
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import urllib.request
import zipfile
import tarfile

def print_banner():
    """打印欢迎信息"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🚀 GNTM: Generative but Natural TextImage Maker 🚀      ║
    ║                                                              ║
    ║              欢迎使用 GNTM 自动安装配置脚本                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    if sys.version_info < (3, 7):
        print("❌ 错误：需要Python 3.7或更高版本")
        print(f"   当前版本：{sys.version}")
        sys.exit(1)
    print(f"✅ Python版本检查通过：{sys.version}")

def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ 依赖包安装完成")
    except subprocess.CalledProcessError:
        print("❌ 依赖包安装失败")
        print("💡 请手动运行：pip install -r requirements.txt")
        return False
    return True

def create_directories():
    """创建必要的目录结构"""
    print("\n📁 创建目录结构...")
    directories = [
        "output",
        "output/images", 
        "bg",
        "fonts/ch",
        "fonts/en",
        "texts",
        "examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录：{directory}")

def download_sample_fonts():
    """下载示例字体文件"""
    print("\n🔤 下载示例字体...")
    
    # 这里可以添加自动下载开源字体的逻辑
    # 由于版权问题，这里只创建说明文件
    
    fonts_readme = """# 字体文件说明

## 如何添加字体

### 中文字体 (fonts/ch/)
推荐字体：
- 思源黑体 (Noto Sans CJK)
- 阿里巴巴普惠体
- 微软雅黑
- 宋体

### 英文字体 (fonts/en/)
推荐字体：
- Roboto
- Arial
- Times New Roman
- Open Sans

## 字体下载来源
- Google Fonts: https://fonts.google.com/
- 阿里巴巴字体: https://fonts.alibabagroup.com/
- 思源字体: https://github.com/adobe-fonts/

## 注意事项
请确保字体文件的商业使用许可
"""
    
    with open("fonts/README.md", "w", encoding="utf-8") as f:
        f.write(fonts_readme)
    
    print("✅ 字体说明文件已创建")

def create_sample_corpus():
    """创建示例语料库"""
    print("\n📝 创建示例语料库...")
    
    sample_chinese = [
        "你好世界",
        "机器学习",
        "深度学习", 
        "人工智能",
        "计算机视觉",
        "自然语言处理",
        "数据科学",
        "算法工程师",
        "开源项目",
        "代码生成"
    ]
    
    sample_english = [
        "Hello World",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence", 
        "Computer Vision",
        "Natural Language Processing",
        "Data Science",
        "Algorithm Engineer",
        "Open Source Project",
        "Code Generation"
    ]
    
    # 创建中文示例
    with open("texts/sample_chinese.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sample_chinese))
    
    # 创建英文示例
    with open("texts/sample_english.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sample_english))
    
    print("✅ 示例语料库已创建")
    print("   - texts/sample_chinese.txt")
    print("   - texts/sample_english.txt")

def create_sample_config():
    """创建示例配置文件"""
    print("\n⚙️ 创建示例配置...")
    
    quick_config = """# GNTM 快速开始配置
# 适合初次使用的简化配置

FILE_SETTINGS:
  OUTPUT_DIR: "output/images"
  EXTENSION: "jpg"
  NAME_FORMAT: 2
  FONTS: ch

TEXT_SETTINGS:
  LANGUAGE: "ch"
  CORPUS: "texts/sample_chinese.txt"
  CORPUS_TYPE: "CORPUS"
  SIZE: 32
  COLOR: "(0,0,0)"
  STROKE_WIDTH: 0
  STROKE_FILL: "(0,0,0)"
  HEIGHT: 0

IMAGE_FORMAT_SETTINGS:
  WIDTH: 0
  ORIENTATION: 0
  SPACE_WIDTH: 1.0
  MARGINS: "5,4,5,4"
  FIT: False

DISTORTION_SETTINGS:
  SKEW_ANGLE: 5
  RANDOM_SKEW: True

OTHER_SETTINGS:
  NUM_WORKERS: 4
"""
    
    with open("configs/quick_start.yaml", "w", encoding="utf-8") as f:
        f.write(quick_config)
    
    print("✅ 快速开始配置已创建：configs/quick_start.yaml")

def create_examples():
    """创建使用示例脚本"""
    print("\n📚 创建使用示例...")
    
    basic_example = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
GNTM 基础使用示例
生成100张中文图片
\"\"\"

import subprocess
import sys

def main():
    print("🚀 GNTM 基础示例：生成100张中文图片")
    
    cmd = [
        sys.executable, "run.py",
        "--cfg", "configs/quick_start.yaml",
        "--count", "100"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 生成完成！请查看 output/images/ 目录")
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败：{e}")

if __name__ == "__main__":
    main()
"""
    
    with open("examples/basic_example.py", "w", encoding="utf-8") as f:
        f.write(basic_example)
    
    # 创建批量生成示例
    batch_example = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
GNTM 批量生成示例
生成中英文混合数据集
\"\"\"

import subprocess
import sys
from pathlib import Path

def generate_dataset(language, corpus_file, output_dir, count=500):
    \"\"\"生成指定语言的数据集\"\"\"
    print(f"🔄 生成{language}数据集...")
    
    cmd = [
        sys.executable, "run.py",
        "--language", language,
        "--corpus", corpus_file,
        "--output_dir", output_dir,
        "--count", str(count),
        "--num_workers", "4"
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ {language}数据集生成完成")

def main():
    print("🚀 GNTM 批量生成示例")
    
    # 创建输出目录
    Path("output/chinese").mkdir(parents=True, exist_ok=True)
    Path("output/english").mkdir(parents=True, exist_ok=True)
    
    try:
        # 生成中文数据集
        generate_dataset("ch", "texts/sample_chinese.txt", "output/chinese")
        
        # 生成英文数据集
        generate_dataset("en", "texts/sample_english.txt", "output/english")
        
        print("🎉 批量生成完成！")
        print("📁 中文数据：output/chinese/")
        print("📁 英文数据：output/english/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败：{e}")

if __name__ == "__main__":
    main()
"""
    
    with open("examples/batch_example.py", "w", encoding="utf-8") as f:
        f.write(batch_example)
    
    print("✅ 使用示例已创建：")
    print("   - examples/basic_example.py")
    print("   - examples/batch_example.py")

def check_installation():
    """检查安装是否成功"""
    print("\n🔍 检查安装状态...")
    
    # 检查核心文件
    core_files = [
        "run.py",
        "configs/config.yaml",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in core_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ 缺少核心文件：")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    # 检查目录结构
    required_dirs = ["output", "fonts", "texts", "bg"]
    for directory in required_dirs:
        if not Path(directory).exists():
            print(f"❌ 缺少目录：{directory}")
            return False
    
    print("✅ 安装检查通过")
    return True

def print_next_steps():
    """打印后续步骤说明"""
    next_steps = """
    🎉 安装完成！接下来你可以：

    📖 快速开始：
    python run.py --cfg configs/quick_start.yaml

    🔤 添加字体文件：
    - 将中文字体放入 fonts/ch/ 目录
    - 将英文字体放入 fonts/en/ 目录

    📝 自定义语料库：
    - 编辑 texts/ 目录下的文本文件
    - 每行一个文本样本

    🖼️ 添加背景图片：
    - 将图片放入 bg/ 目录

    📚 查看更多示例：
    python examples/basic_example.py
    python examples/batch_example.py

    📋 查看详细文档：
    cat README.md

    ❓ 如有问题，请查看 README.md 中的常见问题部分
    """
    print(next_steps)

def main():
    """主函数"""
    try:
        print_banner()
        check_python_version()
        
        if install_dependencies():
            create_directories()
            download_sample_fonts()
            create_sample_corpus()
            create_sample_config()
            create_examples()
            
            if check_installation():
                print_next_steps()
                return True
        
        return False
        
    except KeyboardInterrupt:
        print("\n❌ 安装被用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 安装过程中发生错误：{e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
