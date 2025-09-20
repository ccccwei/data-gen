# GNTM: Generative but Natural TextImage Maker

<div align="center">
  <img src="srg/WechatIMG909.jpeg" alt="GNTM Logo" width="200">
  
  **🔥 专业的OCR训练数据合成工具 🔥**
  
  [![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![Stars](https://img.shields.io/github/stars/your-repo/data-gen.svg)](https://github.com/your-repo/data-gen)
</div>

> 原项目灵感来源于优秀的 [ocrdata](https://github.com/juwonh/ocrdata.git) 项目

**如果这个项目对你的OCR工作流程有帮助，别忘了给我们 [⭐ 点个Star ⭐](#)！** 🙇🙇🙇

## 🚀 快速开始

### 一键运行（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/data-gen.git
cd data-gen

# 2. 运行自动安装脚本
python setup.py

# 3. 生成示例数据
python run.py --quick-start
```

### 手动安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 生成数据（使用默认配置）
python run.py

# 3. 查看生成结果
ls output/images/
```

## 📁 项目结构

```
data-gen/
├── 📁 configs/          # 配置文件
│   └── config.yaml      # 主配置文件
├── 📁 fonts/            # 字体文件夹
│   ├── ch/              # 中文字体
│   └── en/              # 英文字体
├── 📁 texts/            # 文本语料库
├── 📁 bg/               # 背景图片
├── 📁 output/           # 生成结果（自动创建）
│   ├── images/          # 生成的图片
│   └── label.txt        # 标签文件
└── run.py               # 主程序
```

## 🎯 核心功能

### 1. **智能字体渲染**
- 🔄 自动字体回退：某字体不支持时自动切换
- 🎨 多种文字效果：描边、阴影、渐变
- 📐 灵活布局：水平/垂直排版

### 2. **丰富的背景选择**
- 🖼️ 图片背景：从bg文件夹随机选择
- 🌫️ 噪声背景：模拟真实纸张纹理
- 🎨 纯色背景：可自定义颜色

### 3. **真实感数据增强**
- 🔄 随机旋转：模拟拍摄角度
- 💫 模糊效果：模拟拍摄模糊
- 🌟 亮度对比度：模拟光照条件
- 📱 噪声添加：模拟设备噪声

## 💡 使用示例

### 基础用法

```bash
# 使用默认配置生成1000张图片
python run.py

# 指定配置文件
python run.py --cfg configs/my_config.yaml

# 快速生成少量样本（100张）
python run.py --count 100
```

### 高级用法

```bash
# 只生成中文数据
python run.py --language ch --fonts ch

# 生成英文数据
python run.py --language en --fonts en

# 自定义输出目录
python run.py --output_dir my_output

# 使用多进程加速（8个进程）
python run.py --num_workers 8

# 生成高质量大图（字体大小64）
python run.py --size 64 --width 800
```

## ⚙️ 配置说明

主要配置在 `configs/config.yaml` 中：

```yaml
# 文本设置
TEXT_SETTINGS:
  LANGUAGE: "ch"           # 语言：ch=中文, en=英文
  CORPUS: "texts/xxx.txt"  # 文本语料库文件
  SIZE: 32                 # 字体大小
  COLOR: "(0,0,0)"        # 文字颜色（黑色）

# 图像设置
IMAGE_FORMAT_SETTINGS:
  WIDTH: 0                 # 图片宽度（0=自适应）
  ORIENTATION: 0           # 方向：0=水平, 1=垂直
  MARGINS: "5,4,5,4"      # 边距：上,左,下,右

# 输出设置
FILE_SETTINGS:
  OUTPUT_DIR: "output/images"  # 输出目录
  EXTENSION: "jpg"             # 图片格式
  FONTS: "ch"                  # 字体目录
```

## 📖 详细教程

### 1. 准备字体文件

```bash
# 将字体文件放入对应目录
fonts/
├── ch/                    # 中文字体
│   ├── SimHei.ttf
│   └── AlibabaPuHuiTi-3-55-Regular.ttf
└── en/                    # 英文字体
    ├── Arial.ttf
    └── Roboto-Regular.ttf
```

### 2. 准备文本语料

```bash
# 创建文本文件，每行一个文本样本
echo "你好世界" >> texts/my_corpus.txt
echo "机器学习" >> texts/my_corpus.txt
echo "深度学习" >> texts/my_corpus.txt
```

### 3. 准备背景图片（可选）

```bash
# 将背景图片放入bg文件夹
bg/
├── paper1.jpg
├── texture1.png
└── background1.jpg
```

### 4. 运行生成

```bash
# 使用自定义语料库
python run.py --corpus texts/my_corpus.txt

# 查看生成结果
ls output/images/        # 查看图片
cat output/label.txt     # 查看标签
```

## 🔧 常见问题

### Q: 生成的图片是空白的？
A: 检查字体文件是否支持你的文本字符，可以查看 `output/no_support_char_and_corpus.txt` 文件

### Q: 如何提高生成速度？
A: 使用 `--num_workers 8` 参数启用多进程

### Q: 如何自定义背景？
A: 将图片放入 `bg/` 文件夹，或修改 `background_generator.py`

### Q: 如何批量处理多个语料库？
A: 创建脚本循环调用 `run.py` 或修改配置文件

## 🎨 输出示例

生成的数据包含：
- 📷 **图片文件**：`00000001.jpg`, `00000002.jpg`, ...
- 📄 **标签文件**：`label.txt` (格式：`图片路径\t文本内容`)

标签文件示例：
```
images/00000001.jpg	你好世界
images/00000002.jpg	机器学习
images/00000003.jpg	深度学习
```

## 🤝 贡献指南

欢迎贡献代码！请：
1. Fork 本项目
2. 创建功能分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 创建 Pull Request

### Co-developer
- 👩‍💻 [lalallllllll](https://github.com/lalallllllll)

## 📄 开源协议

本项目采用 MIT 开源协议。详见 [LICENSE](LICENSE) 文件。

---

<div align="center">
  <strong>🚀 准备好用GNTM改变你的OCR工作流程了吗？让我们开始吧！ 🚀</strong>
</div>