#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNTM 诊断和错误处理模块
提供友好的错误信息和解决建议
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple, Optional
import traceback

class GTNMDiagnostics:
    """GNTM 诊断工具类"""
    
    @staticmethod
    def check_environment() -> List[Tuple[str, bool, str]]:
        """检查运行环境"""
        checks = []
        
        # Python版本检查
        py_version = sys.version_info
        py_ok = py_version >= (3, 7)
        py_msg = f"Python {py_version.major}.{py_version.minor}.{py_version.micro}"
        if not py_ok:
            py_msg += " (需要 3.7+)"
        checks.append(("Python版本", py_ok, py_msg))
        
        # 核心文件检查
        core_files = [
            "run.py",
            "configs/config.yaml", 
            "requirements.txt",
            "core/__init__.py"
        ]
        
        for file_path in core_files:
            exists = Path(file_path).exists()
            checks.append((f"核心文件 {file_path}", exists, "存在" if exists else "缺失"))
        
        # 目录结构检查
        required_dirs = ["fonts", "texts", "bg", "generators", "core"]
        for dir_path in required_dirs:
            exists = Path(dir_path).exists()
            checks.append((f"目录 {dir_path}", exists, "存在" if exists else "缺失"))
        
        return checks
    
    @staticmethod
    def check_fonts(font_dir: str = "ch") -> Tuple[bool, List[str], str]:
        """检查字体文件"""
        font_path = Path(f"fonts/{font_dir}")
        
        if not font_path.exists():
            return False, [], f"字体目录不存在: {font_path}"
        
        font_extensions = ['.ttf', '.otf', '.ttc']
        font_files = []
        
        for ext in font_extensions:
            font_files.extend(font_path.glob(f"*{ext}"))
        
        if not font_files:
            return False, [], f"字体目录为空: {font_path}"
        
        font_names = [f.name for f in font_files]
        return True, font_names, f"找到 {len(font_files)} 个字体文件"
    
    @staticmethod
    def check_corpus(corpus_path: str) -> Tuple[bool, int, str]:
        """检查语料库文件"""
        path = Path(corpus_path)
        
        if not path.exists():
            return False, 0, f"语料库文件不存在: {corpus_path}"
        
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            if not lines:
                return False, 0, "语料库文件为空"
            
            return True, len(lines), f"包含 {len(lines)} 行有效文本"
            
        except Exception as e:
            return False, 0, f"读取语料库失败: {e}"
    
    @staticmethod
    def diagnose_error(error: Exception) -> str:
        """诊断错误并提供解决建议"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        # 常见错误类型和建议
        error_suggestions = {
            "FileNotFoundError": {
                "description": "文件或目录不存在",
                "solutions": [
                    "检查文件路径是否正确",
                    "确保文件确实存在",
                    "运行 'python setup.py' 创建必要文件"
                ]
            },
            "UnicodeDecodeError": {
                "description": "文本编码问题", 
                "solutions": [
                    "确保文本文件使用 UTF-8 编码保存",
                    "检查文件是否包含特殊字符",
                    "尝试用记事本另存为 UTF-8 格式"
                ]
            },
            "OSError": {
                "description": "系统操作错误",
                "solutions": [
                    "检查磁盘空间是否充足",
                    "确保有足够的权限访问文件",
                    "检查路径长度是否过长"
                ]
            },
            "MemoryError": {
                "description": "内存不足",
                "solutions": [
                    "减少 --count 参数值",
                    "降低图片尺寸 --size",
                    "减少进程数 --num_workers"
                ]
            },
            "ImportError": {
                "description": "依赖包缺失",
                "solutions": [
                    "运行 'pip install -r requirements.txt'",
                    "检查Python环境是否正确",
                    "尝试重新安装依赖包"
                ]
            }
        }
        
        suggestion = error_suggestions.get(error_type, {
            "description": "未知错误",
            "solutions": [
                "检查控制台错误信息",
                "确保所有依赖正确安装",
                "尝试使用 --verbose 查看详细信息"
            ]
        })
        
        diagnosis = f"""
❌ 错误类型: {error_type}
📝 错误描述: {suggestion['description']}
💬 错误信息: {error_msg}

💡 解决建议:
"""
        for i, solution in enumerate(suggestion['solutions'], 1):
            diagnosis += f"   {i}. {solution}\n"
        
        # 特殊情况的额外建议
        if "font" in error_msg.lower():
            diagnosis += "\n🔤 字体相关问题:\n"
            diagnosis += "   - 确保 fonts/ 目录下有字体文件\n"
            diagnosis += "   - 检查字体文件格式 (.ttf, .otf)\n"
            diagnosis += "   - 尝试使用系统默认字体\n"
        
        if "corpus" in error_msg.lower() or "text" in error_msg.lower():
            diagnosis += "\n📝 文本相关问题:\n"
            diagnosis += "   - 确保语料库文件存在且不为空\n"
            diagnosis += "   - 检查文件编码是否为 UTF-8\n"
            diagnosis += "   - 尝试使用示例文件测试\n"
        
        return diagnosis
    
    @staticmethod
    def create_diagnostic_report() -> str:
        """创建完整的诊断报告"""
        report = "🔍 GNTM 系统诊断报告\n"
        report += "=" * 50 + "\n\n"
        
        # 环境检查
        report += "📋 环境检查:\n"
        checks = GTNMDiagnostics.check_environment()
        for name, status, message in checks:
            status_icon = "✅" if status else "❌"
            report += f"   {status_icon} {name}: {message}\n"
        
        # 字体检查
        report += "\n🔤 字体检查:\n"
        for font_dir in ["ch", "en"]:
            ok, fonts, msg = GTNMDiagnostics.check_fonts(font_dir)
            status_icon = "✅" if ok else "❌"
            report += f"   {status_icon} fonts/{font_dir}/: {msg}\n"
            if ok and len(fonts) <= 3:
                for font in fonts:
                    report += f"      - {font}\n"
            elif ok and len(fonts) > 3:
                for font in fonts[:3]:
                    report += f"      - {font}\n"
                report += f"      ... 还有 {len(fonts) - 3} 个字体\n"
        
        # 语料库检查
        report += "\n📝 语料库检查:\n"
        for corpus in ["texts/Company-Shorter-Form1000.txt", "texts/sample_chinese.txt", "texts/sample_english.txt"]:
            if Path(corpus).exists():
                ok, count, msg = GTNMDiagnostics.check_corpus(corpus)
                status_icon = "✅" if ok else "❌"
                report += f"   {status_icon} {corpus}: {msg}\n"
        
        report += "\n" + "=" * 50 + "\n"
        return report

def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理器"""
    if issubclass(exc_type, KeyboardInterrupt):
        # 用户中断，优雅退出
        print("\n❌ 程序被用户中断")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("❌ GNTM 运行时发生错误")
    print("="*60)
    
    # 显示友好的错误诊断
    diagnosis = GTNMDiagnostics.diagnose_error(exc_value)
    print(diagnosis)
    
    print("\n🔍 详细错误信息:")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    
    print("\n📋 如需更多帮助:")
    print("   1. 运行诊断: python -c \"from core.diagnostics import GTNMDiagnostics; print(GTNMDiagnostics.create_diagnostic_report())\"")
    print("   2. 查看文档: cat README.md")
    print("   3. 尝试快速开始: python run.py --quick-start")
    
    sys.exit(1)

# 注册全局异常处理器
sys.excepthook = handle_exception
