import argparse
import sys
import yaml
from easydict import EasyDict as edict
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
import time

from generators.text_generator import (
    create_strings_from_dict,
    create_strings_from_corpus_file,
    create_strings_randomly_from_chars
)
from generators.data_generator import FakeTextDataGenerator
from core.config import load_config
from core.logger import setup_logger
from core.diagnostics import GTNMDiagnostics


def parse_margins(margin_str):
    """
    边距就是字符离左右上下边界的距离
    将逗号分隔的字符串转换为整数列表，用于设置边距。
    示例:
        "5" -> [5, 5, 5, 5]
        "5,10,5,10" -> [5, 10, 5, 10]
    """
    margins = margin_str.split(',')
    if len(margins) == 1:
        # 如果只给定一个值，则四个边距相同
        return [int(margins[0])] * 4
    return [int(m) for m in margins]


def parse_args():
    """
    解析命令行参数，返回命名空间对象。
    """
    parser = argparse.ArgumentParser(
        description="🚀 GNTM: Generative but Natural TextImage Maker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  基础使用:
    python run.py
  
  快速开始 (生成100张图片):
    python run.py --quick-start
    
  自定义配置:
    python run.py --cfg configs/my_config.yaml
    
  生成中文数据:
    python run.py --language ch --fonts ch --count 500
    
  生成英文数据:
    python run.py --language en --fonts en --count 500
    
  高质量输出:
    python run.py --size 64 --width 800 --extension png
    
  多进程加速:
    python run.py --num_workers 8
    
  自定义输出目录:
    python run.py --output_dir my_dataset

更多信息请查看 README.md
        """
    )
    
    # 基础设置
    basic_group = parser.add_argument_group('📁 基础设置')
    basic_group.add_argument(
        '--cfg', 
        help='配置文件路径 (默认: configs/config.yaml)', 
        type=str, 
        default='configs/config.yaml'
    )
    basic_group.add_argument(
        '--quick-start', 
        action='store_true',
        help='快速开始模式 (生成100张示例图片)'
    )
    basic_group.add_argument(
        '--output_dir', 
        help='输出目录 (默认: output/images)', 
        type=str
    )
    
    # 文本设置
    text_group = parser.add_argument_group('📝 文本设置')
    text_group.add_argument(
        '--language', 
        choices=['ch', 'en'],
        help='语言类型: ch=中文, en=英文'
    )
    text_group.add_argument(
        '--corpus', 
        help='文本语料库文件路径',
        type=str
    )
    text_group.add_argument(
        '--count', 
        help='生成图片数量 (默认: 1000)', 
        type=int
    )
    
    # 字体和样式
    style_group = parser.add_argument_group('🎨 字体和样式')
    style_group.add_argument(
        '--fonts', 
        help='字体目录: ch=中文字体, en=英文字体, 或具体字体文件名',
        type=str
    )
    style_group.add_argument(
        '--size', 
        help='字体大小 (像素, 推荐: 16-64)', 
        type=int
    )
    style_group.add_argument(
        '--color', 
        help='文字颜色 RGB格式 (如: "255,0,0" 表示红色)',
        type=str
    )
    
    # 图像设置
    image_group = parser.add_argument_group('🖼️ 图像设置')
    image_group.add_argument(
        '--width', 
        help='图像宽度 (像素, 0=自适应)', 
        type=int
    )
    image_group.add_argument(
        '--height', 
        help='图像高度 (像素, 0=自适应)', 
        type=int
    )
    image_group.add_argument(
        '--extension', 
        choices=['jpg', 'jpeg', 'png'],
        help='输出图片格式: jpg=压缩率高, png=质量高'
    )
    image_group.add_argument(
        '--margins', 
        help='边距设置 "上,左,下,右" (如: "10,5,10,5")',
        type=str
    )
    
    # 变形和增强
    effect_group = parser.add_argument_group('🔄 变形和增强')
    effect_group.add_argument(
        '--skew_angle', 
        help='最大倾斜角度 (度, 0=无倾斜)', 
        type=int
    )
    effect_group.add_argument(
        '--no_skew', 
        action='store_true',
        help='禁用随机倾斜'
    )
    
    # 性能设置
    perf_group = parser.add_argument_group('⚙️ 性能设置')
    perf_group.add_argument(
        '--num_workers', 
        help='多进程数量 (推荐: 4-8)', 
        type=int
    )
    
    # 调试选项
    debug_group = parser.add_argument_group('🔍 调试选项')
    debug_group.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='详细输出模式'
    )
    debug_group.add_argument(
        '--dry_run',
        action='store_true', 
        help='预览模式 (只显示设置，不生成图片)'
    )
    debug_group.add_argument(
        '--diagnose',
        action='store_true',
        help='运行系统诊断检查'
    )
    
    return parser.parse_args()

def load_fonts(font_or_dir):
    """
    加载指定路径（文件或目录）下的字体列表。
    如果 font_or_dir 是文件，则只返回该文件。
    如果是目录，则返回目录下所有文件。
    """
    p = Path("fonts/"+font_or_dir)
    if not p.exists():
        sys.exit(f"[Error] Font path does not exist: {font_or_dir}")

    if p.is_file():
        # 传入的是一个具体字体文件路径
        return [str(p)]
    else:
        # 从某个目录加载所有字体
        font_paths = [str(font) for font in p.glob('*') if font.is_file()]
        if not font_paths:
            sys.exit(f"[Error] No font files found in directory: {font_or_dir}")
        return font_paths


def load_corpus(corpus_file_path):
    """
    加载语料库文件，返回行列表。
    """
    p = Path(corpus_file_path)
    if not p.exists():
        sys.exit(f"[Error] Corpus file not found: {corpus_file_path}")
    with open(p, 'r', encoding="utf-8-sig", errors='ignore') as file:
        words_list = [line.strip() for line in file if line.strip()]
    return words_list

def worker(param_tuple):
    """
    包装函数，给多进程调用用的。
    """
    return FakeTextDataGenerator.generate(*param_tuple)

def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🚀 GNTM: Generative but Natural TextImage Maker 🚀      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def apply_quick_start_settings(args):
    """应用快速开始设置"""
    print("🚀 快速开始模式已启用")
    # 覆盖一些设置以适合快速测试
    args.count = 100
    args.num_workers = min(4, args.num_workers) if hasattr(args, 'num_workers') else 4
    
    # 使用示例语料库（如果存在）
    if Path("texts/sample_chinese.txt").exists():
        args.corpus = "texts/sample_chinese.txt"
        print("📝 使用示例中文语料库")
    elif Path("texts/sample_english.txt").exists():
        args.corpus = "texts/sample_english.txt"
        args.language = "en"
        args.fonts = "en"
        print("📝 使用示例英文语料库")

def apply_command_line_overrides(args, cfg):
    """应用命令行参数覆盖配置文件设置"""
    override_mapping = {
        'output_dir': ('FILE_SETTINGS', 'OUTPUT_DIR'),
        'language': ('TEXT_SETTINGS', 'LANGUAGE'),
        'corpus': ('TEXT_SETTINGS', 'CORPUS'),
        'count': ('OTHER_SETTINGS', 'COUNT'),
        'fonts': ('FILE_SETTINGS', 'FONTS'),
        'size': ('TEXT_SETTINGS', 'SIZE'),
        'color': ('TEXT_SETTINGS', 'COLOR'),
        'width': ('IMAGE_FORMAT_SETTINGS', 'WIDTH'),
        'height': ('TEXT_SETTINGS', 'HEIGHT'),
        'extension': ('FILE_SETTINGS', 'EXTENSION'),
        'margins': ('IMAGE_FORMAT_SETTINGS', 'MARGINS'),
        'skew_angle': ('DISTORTION_SETTINGS', 'SKEW_ANGLE'),
        'num_workers': ('OTHER_SETTINGS', 'NUM_WORKERS'),
    }
    
    for arg_name, (section_name, config_key) in override_mapping.items():
        if hasattr(args, arg_name) and getattr(args, arg_name) is not None:
            section = getattr(cfg, section_name)
            setattr(section, config_key, getattr(args, arg_name))
            if args.verbose:
                print(f"🔧 覆盖配置: {section_name}.{config_key} = {getattr(args, arg_name)}")
    
    # 特殊处理
    if args.no_skew:
        cfg.DISTORTION_SETTINGS.SKEW_ANGLE = 0
        cfg.DISTORTION_SETTINGS.RANDOM_SKEW = False
        if args.verbose:
            print("🔧 已禁用随机倾斜")
    
    if args.color:
        # 转换颜色格式
        if not args.color.startswith('('):
            # 如果用户输入 "255,0,0"，转换为 "(255,0,0)"
            cfg.TEXT_SETTINGS.COLOR = f"({args.color})"

def print_settings_summary(args):
    """打印设置摘要"""
    print("\n📋 当前设置摘要:")
    print(f"   语言: {args.language}")
    print(f"   语料库: {args.corpus}")
    print(f"   字体: {args.fonts}")
    print(f"   图片数量: {getattr(args, 'count', 'N/A')}")
    print(f"   输出目录: {args.output_dir}")
    print(f"   字体大小: {args.size}")
    print(f"   进程数: {args.num_workers}")
    print(f"   图片格式: {args.extension}")

def main():
    # 打印欢迎信息
    print_banner()
    
    # 1. 解析参数
    args = parse_args()
    
    # 诊断模式
    if args.diagnose:
        print("🔍 运行系统诊断...")
        report = GTNMDiagnostics.create_diagnostic_report()
        print(report)
        return
    
    # 设置日志级别
    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger("data_gen", level=log_level)
    
    # 2. 加载配置文件
    if args.verbose:
        print(f"📖 加载配置文件: {args.cfg}")
    
    cfg = load_config(args.cfg)
    
    # 3. 应用快速开始设置
    if args.quick_start:
        apply_quick_start_settings(args)
    
    # 4. 应用命令行参数覆盖
    apply_command_line_overrides(args, cfg)
    
    # 5. 将配置文件扁平化写入 args，保持后续代码兼容
    for section in cfg.__dict__.values():
        for key, value in section.__dict__.items():
            if not hasattr(args, key.lower()) or getattr(args, key.lower()) is None:
                setattr(args, key.lower(), value)
    
    # 6. 打印设置摘要
    if args.verbose:
        print_settings_summary(args)
    
    # 7. 预览模式
    if args.dry_run:
        print("\n🔍 预览模式 - 不会生成实际图片")
        print_settings_summary(args)
        print(f"\n📊 预计生成 {args.count} 张图片")
        print(f"📁 保存到: {args.output_dir}")
        return

    # 8. 加载语料库
    try:
        corpus_list = load_corpus(args.corpus)
    except Exception as e:
        print(f"❌ 加载语料库失败: {e}")
        print(f"💡 请检查文件路径: {args.corpus}")
        sys.exit(1)
    num_texts = len(corpus_list)
    print(f"✅ 加载语料库成功: {num_texts} 行文本")

    # 9. 加载字体
    try:
        if args.fonts:
            font_paths = load_fonts(args.fonts)
        else:
            font_paths = load_fonts('ch')  # 默认从 'ch' 目录加载
        num_fonts = len(font_paths)
        print(f"✅ 加载字体成功: {num_fonts} 个字体文件")
        if args.verbose:
            for font in font_paths[:3]:  # 只显示前3个
                print(f"   - {Path(font).name}")
            if num_fonts > 3:
                print(f"   ... 还有 {num_fonts - 3} 个字体文件")
    except Exception as e:
        print(f"❌ 加载字体失败: {e}")
        print(f"💡 请检查字体目录: fonts/{args.fonts}/")
        sys.exit(1)

    # 10. 根据 corpus_type 生成字符串列表
    print(f"📝 生成文本内容...")
    if args.corpus_type.upper() == "CORPUS":
        print(f"   使用语料库文件: {Path(args.corpus).name}")
        args.strings = create_strings_from_corpus_file(args.corpus)
    elif args.corpus_type.upper() == "RANDOM":
        print("   使用随机字符生成")
        args.strings = create_strings_randomly_from_chars(
            length=args.length,
            allow_variable=args.random,
            count=args.count,
            include_letters=args.include_letters,
            include_numbers=args.include_numbers,
            include_symbols=args.include_symbols,
            language=args.language
        )
        # 如果包含符号，或者其他条件不符合，就强制 name_format=2
        if args.include_symbols or not any([
            args.include_letters,
            args.include_numbers,
            args.include_symbols
        ]):
            args.name_format = 2
    else:
        print("   使用字典循环生成")
        args.strings = create_strings_from_dict(
            args.length,
            args.random,
            args.count,
            corpus_list
        )

    total_count = len(args.strings)
    print(f"✅ 文本内容准备完成: {total_count} 个样本")

    # 11. 设置颜色
    try:
        font_color = tuple(map(int, args.color.strip("()").split(",")))
        font_colors = [font_color]
        num_colors = len(font_colors)
        if args.verbose:
            print(f"🎨 文字颜色: RGB{font_color}")
    except Exception as e:
        print(f"❌ 颜色格式错误: {args.color}")
        print("💡 请使用格式: '(R,G,B)' 例如 '(0,0,0)' 表示黑色")
        sys.exit(1)

    # 12. 准备输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 输出目录: {output_dir}")

    # 13. 构造参数列表
    print("⚙️ 准备生成参数...")
    cursive_flags = [0] * total_count
    margins_str = args.margins

    image_params = []
    for i in range(total_count):
        color_idx = i % num_colors
        param_tuple = (
            i,
            args.strings[i],
            font_paths,
            str(output_dir),
            cursive_flags[i],
            args.size,
            args.extension,
            args.skew_angle,
            args.width,
            font_colors[color_idx],
            args.orientation,
            args.space_width,
            margins_str,
            args.fit,
            args.stroke_width,
            args.stroke_fill,
            args.height
        )
        image_params.append(param_tuple)

    print(f"\n🚀 开始生成 {total_count} 张图像...")
    print(f"📊 进程数: {args.num_workers}")
    print(f"🎯 目标格式: {args.extension.upper()}")
    start_time = time.time()

    # 14. 多进程 / 单进程执行
    try:
        if args.num_workers <= 1:
            # 单进程执行
            print("🔄 单进程模式")
            for params in tqdm(image_params, total=total_count, desc="生成进度"):
                FakeTextDataGenerator.generate(*params)
        else:
            # 多进程执行
            print(f"🔄 多进程模式 ({args.num_workers} 个进程)")
            with Pool(processes=args.num_workers) as pool:
                for _ in tqdm(pool.imap_unordered(worker, image_params), total=total_count, desc="生成进度"):
                    pass
    except KeyboardInterrupt:
        print("\n❌ 生成被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 生成过程中发生错误: {e}")
        sys.exit(1)

    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🎉 数据生成完成！")
    print(f"⏱️  总用时: {duration:.2f} 秒")
    print(f"⚡ 平均速度: {total_count/duration:.2f} 张/秒")
    print(f"📁 输出目录: {output_dir}")
    print(f"📄 标签文件: {output_dir.parent}/label.txt")
    print(f"\n💡 使用以下命令查看结果:")
    print(f"   ls {output_dir}")
    print(f"   head {output_dir.parent}/label.txt")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)