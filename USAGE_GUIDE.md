# 🚀 GNTM 使用指南

欢迎使用 GNTM (Generative but Natural TextImage Maker)！这是一个全面的使用指南，帮助你快速上手并掌握所有功能。

## 📋 目录

1. [快速开始](#快速开始)
2. [基础用法](#基础用法)  
3. [高级功能](#高级功能)
4. [Web界面](#web界面)
5. [常见问题](#常见问题)
6. [最佳实践](#最佳实践)

## 🚀 快速开始

### 1. 一键安装和配置

```bash
# 克隆项目
git clone https://github.com/your-repo/data-gen.git
cd data-gen

# 自动安装和配置
python setup.py

# 快速生成示例
python run.py --quick-start
```

### 2. 查看结果

```bash
# 查看生成的图片
ls output/images/

# 查看标签文件
head output/label.txt
```

## 📖 基础用法

### 命令行基础语法

```bash
python run.py [选项]
```

### 常用命令示例

```bash
# 使用默认设置生成图片
python run.py

# 生成指定数量的图片
python run.py --count 500

# 使用英文字体和语料
python run.py --language en --fonts en

# 指定输出目录
python run.py --output_dir my_dataset

# 使用多进程加速
python run.py --num_workers 8

# 查看详细信息
python run.py --verbose
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--count` | 生成图片数量 | `--count 1000` |
| `--language` | 语言 (ch/en) | `--language ch` |
| `--fonts` | 字体目录 | `--fonts ch` |
| `--size` | 字体大小 | `--size 32` |
| `--output_dir` | 输出目录 | `--output_dir my_output` |
| `--num_workers` | 进程数 | `--num_workers 8` |
| `--extension` | 图片格式 | `--extension png` |

## ⚙️ 高级功能

### 1. 自定义配置文件

创建 `configs/my_config.yaml`：

```yaml
FILE_SETTINGS:
  OUTPUT_DIR: "output/custom"
  EXTENSION: "png"
  FONTS: "ch"

TEXT_SETTINGS:
  LANGUAGE: "ch"
  CORPUS: "texts/my_corpus.txt"
  SIZE: 48
  COLOR: "(255,0,0)"    # 红色文字
  STROKE_WIDTH: 2
  STROKE_FILL: "(0,0,0)" # 黑色描边

IMAGE_FORMAT_SETTINGS:
  WIDTH: 800            # 固定宽度
  MARGINS: "15,20,15,20" # 自定义边距

DISTORTION_SETTINGS:
  SKEW_ANGLE: 15        # 较大倾斜角度

OTHER_SETTINGS:
  NUM_WORKERS: 6
  COUNT: 2000
```

使用自定义配置：

```bash
python run.py --cfg configs/my_config.yaml
```

### 2. 自定义语料库

创建 `texts/my_corpus.txt`：

```
你好世界
机器学习
深度学习
计算机视觉
自然语言处理
```

使用自定义语料库：

```bash
python run.py --corpus texts/my_corpus.txt
```

### 3. 批量生成不同样式

```bash
# 小字体数据集
python run.py --size 16 --count 1000 --output_dir output/small_font

# 大字体数据集  
python run.py --size 64 --count 1000 --output_dir output/large_font

# 高倾斜角度数据集
python run.py --skew_angle 20 --count 1000 --output_dir output/high_skew

# 英文数据集
python run.py --language en --fonts en --corpus texts/english.txt --output_dir output/english
```

### 4. 调试和诊断

```bash
# 运行系统诊断
python run.py --diagnose

# 预览设置(不生成图片)
python run.py --dry_run --verbose

# 详细输出模式
python run.py --verbose
```

## 🌐 Web界面

### 启动Web界面

```bash
python web_interface.py
```

默认访问地址：http://localhost:8080

### Web界面功能

- 📝 可视化配置参数
- 🎨 实时预览设置
- 📊 生成进度显示
- 🖼️ 结果图片预览
- 📱 移动设备友好

### 自定义端口

```bash
python web_interface.py --port 9000
```

## 🔧 常见问题

### Q: 生成的图片是空白的？

**原因**: 字体不支持相应字符

**解决方案**:
1. 检查字体文件：`ls fonts/ch/`
2. 查看不支持的字符：`cat output/no_support_char_and_corpus.txt`
3. 添加更多字体文件到 `fonts/` 目录

### Q: 生成速度很慢？

**解决方案**:
1. 增加进程数：`--num_workers 8`
2. 使用JPG格式：`--extension jpg`
3. 减少图片尺寸：`--size 24`

### Q: 内存不足错误？

**解决方案**:
1. 减少生成数量：`--count 500`
2. 减少进程数：`--num_workers 2`
3. 降低图片尺寸：`--size 16`

### Q: 字体路径错误？

**解决方案**:
1. 检查字体目录：`ls fonts/`
2. 确保字体文件存在：`ls fonts/ch/*.ttf`
3. 运行诊断：`python run.py --diagnose`

### Q: 语料库文件编码问题？

**解决方案**:
1. 确保文件使用UTF-8编码
2. 检查文件内容：`head -5 texts/your_corpus.txt`
3. 重新保存为UTF-8格式

## 💡 最佳实践

### 1. 性能优化

```bash
# 最佳性能配置
python run.py \
  --num_workers 8 \
  --extension jpg \
  --size 32 \
  --count 5000
```

### 2. 质量优化

```bash
# 最佳质量配置
python run.py \
  --extension png \
  --size 48 \
  --width 800 \
  --no_skew \
  --count 1000
```

### 3. 生产环境配置

```yaml
FILE_SETTINGS:
  OUTPUT_DIR: "datasets/train_data"
  EXTENSION: "jpg"
  FONTS: "ch"

TEXT_SETTINGS:
  SIZE: 32
  COLOR: "(0,0,0)"

OTHER_SETTINGS:
  NUM_WORKERS: 16
  COUNT: 50000
```

### 4. 目录结构建议

```
data-gen/
├── datasets/           # 生产数据集
│   ├── train/
│   ├── val/
│   └── test/
├── experiments/        # 实验数据
├── fonts/
│   ├── ch/            # 中文字体
│   └── en/            # 英文字体
└── corpus/            # 语料库文件
    ├── general.txt
    ├── domain_specific.txt
    └── test_samples.txt
```

### 5. 批量处理脚本

```bash
#!/bin/bash
# 批量生成多个数据集

echo "生成训练集..."
python run.py --count 40000 --output_dir datasets/train --num_workers 8

echo "生成验证集..."  
python run.py --count 5000 --output_dir datasets/val --num_workers 8

echo "生成测试集..."
python run.py --count 5000 --output_dir datasets/test --num_workers 8

echo "所有数据集生成完成！"
ls -la datasets/
```

## 🔍 故障排除

### 运行诊断检查

```bash
python run.py --diagnose
```

### 检查依赖安装

```bash
pip install -r requirements.txt
python -c "import PIL, cv2, numpy, yaml; print('所有依赖正常')"
```

### 检查文件权限

```bash
ls -la fonts/
ls -la texts/
mkdir -p output/test && echo "权限正常" || echo "权限问题"
```

### 查看详细错误

```bash
python run.py --verbose --count 10
```

## 📚 示例脚本

查看 `examples/` 目录获取更多示例：

- `examples/quick_start.py` - 快速开始示例
- `examples/batch_generate.py` - 批量生成示例  
- `examples/custom_config.py` - 自定义配置示例

## 🆘 获取帮助

1. **查看帮助信息**:
   ```bash
   python run.py --help
   ```

2. **运行系统诊断**:
   ```bash
   python run.py --diagnose
   ```

3. **查看示例**:
   ```bash
   python examples/quick_start.py
   ```

4. **阅读文档**:
   - [README.md](README.md) - 项目概述
   - [examples/README.md](examples/README.md) - 示例说明

---

🎉 现在你已经掌握了GNTM的所有功能！开始创建你的OCR训练数据集吧！
