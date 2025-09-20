# GNTM 使用示例

这个目录包含了 GNTM 的各种使用示例，帮助你快速上手和学习高级用法。

## 📚 示例列表

### 1. 快速开始 (`quick_start.py`)
**适合**: 初次使用者
**功能**: 生成100张基础示例图片
**用法**:
```bash
python examples/quick_start.py
```

### 2. 批量生成 (`batch_generate.py`)
**适合**: 需要生成多种样式数据集
**功能**: 
- 中文小字体数据集 (24px)
- 中文大字体数据集 (48px)  
- 英文数据集 (32px)
- 高质量PNG数据集 (64px)

**用法**:
```bash
python examples/batch_generate.py
```

### 3. 自定义配置 (`custom_config.py`)
**适合**: 需要特殊样式效果
**功能**: 演示红色文字 + 黑色描边效果
**特点**:
- 固定宽度400px
- 较大倾斜角度
- PNG高质量输出

**用法**:
```bash
python examples/custom_config.py
```

## 🔧 运行前准备

在运行任何示例之前，请确保：

1. **已安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **已运行初始化脚本**:
   ```bash
   python setup.py
   ```

3. **已准备字体文件** (将字体文件放入对应目录):
   - 中文字体: `fonts/ch/`
   - 英文字体: `fonts/en/`

## 📖 自定义示例

你可以基于这些示例创建自己的生成脚本：

### 基础模板

```python
#!/usr/bin/env python3
import subprocess
import sys

def generate_my_dataset():
    cmd = [
        sys.executable, "run.py",
        "--language", "ch",           # 语言
        "--fonts", "ch",              # 字体目录
        "--size", "32",               # 字体大小
        "--count", "1000",            # 图片数量
        "--output_dir", "my_output",  # 输出目录
        "--num_workers", "8"          # 进程数
    ]
    
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    generate_my_dataset()
```

### 高级配置模板

```python
#!/usr/bin/env python3
import yaml

def create_advanced_config():
    config = {
        "FILE_SETTINGS": {
            "OUTPUT_DIR": "output/advanced",
            "EXTENSION": "jpg",
            "FONTS": "ch"
        },
        "TEXT_SETTINGS": {
            "LANGUAGE": "ch",
            "CORPUS": "my_corpus.txt",
            "SIZE": 48,
            "COLOR": "(0,100,200)",      # 蓝色
            "STROKE_WIDTH": 3,
            "STROKE_FILL": "(255,255,255)" # 白色描边
        },
        "IMAGE_FORMAT_SETTINGS": {
            "WIDTH": 800,                # 宽图
            "MARGINS": "20,30,20,30"
        },
        "DISTORTION_SETTINGS": {
            "SKEW_ANGLE": 8
        },
        "OTHER_SETTINGS": {
            "NUM_WORKERS": 6,
            "COUNT": 2000
        }
    }
    
    with open("configs/advanced.yaml", 'w') as f:
        yaml.dump(config, f, allow_unicode=True)

# 使用: python run.py --cfg configs/advanced.yaml
```

## 🎯 典型使用场景

### 场景1: OCR模型训练数据
```bash
# 生成大量标准训练数据
python run.py --count 10000 --num_workers 8

# 生成困难样本 (倾斜、小字体)
python run.py --size 16 --skew_angle 20 --count 2000
```

### 场景2: 多语言数据集
```bash
# 中文数据集
python run.py --language ch --fonts ch --corpus texts/chinese.txt

# 英文数据集  
python run.py --language en --fonts en --corpus texts/english.txt
```

### 场景3: 特定样式数据
```bash
# 大字体高清数据
python run.py --size 64 --extension png --width 1200

# 小字体密集数据
python run.py --size 16 --margins "2,2,2,2" --count 5000
```

## 💡 提示和技巧

1. **性能优化**: 使用 `--num_workers` 参数启用多进程
2. **质量vs速度**: PNG质量高但慢，JPG快但压缩
3. **调试模式**: 使用 `--verbose` 查看详细信息
4. **预览设置**: 使用 `--dry_run` 预览而不生成
5. **快速测试**: 使用 `--quick-start` 快速验证

## ❓ 常见问题

### Q: 示例运行失败？
A: 确保已运行 `python setup.py` 创建必要文件

### Q: 字体相关错误？
A: 检查 `fonts/` 目录下是否有字体文件

### Q: 生成速度慢？
A: 增加 `--num_workers` 参数值

### Q: 想要特殊效果？
A: 参考 `custom_config.py` 创建自定义配置

---

更多信息请查看主目录的 [README.md](../README.md)
