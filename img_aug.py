"""img_aug.py
各种基于 Pillow / NumPy 的轻量级图像增强工具。

后续如需更丰富的增强（透视畸变、仿射、颜色抖动等）可继续在此文件中扩展，
保持与核心生成逻辑解耦。
"""
from __future__ import annotations

import random
from typing import Callable, List

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

__all__ = [
    "apply_augmentations",
]

# ---------------------------------------------------------------------------
# 单项增强函数
# ---------------------------------------------------------------------------

def _rand_bool(p: float) -> bool:
    """Helper: return True with probability *p* (0~1)."""
    return random.random() < p


def gaussian_blur(img: Image.Image, p: float = 0.25) -> Image.Image:
    """Apply random Gaussian blur."""
    if not _rand_bool(p):
        return img
    radius = random.uniform(0.3, 1.5)
    return img.filter(ImageFilter.GaussianBlur(radius))


def brightness(img: Image.Image, p: float = 0.3) -> Image.Image:
    if not _rand_bool(p):
        return img
    factor = random.uniform(0.7, 1.3)  # 1 == original
    return ImageEnhance.Brightness(img).enhance(factor)


def contrast(img: Image.Image, p: float = 0.3) -> Image.Image:
    if not _rand_bool(p):
        return img
    factor = random.uniform(0.7, 1.3)
    return ImageEnhance.Contrast(img).enhance(factor)


def add_gaussian_noise(img: Image.Image, p: float = 0.25, var: float = 8.0) -> Image.Image:
    """Add zero-mean Gaussian noise with variance *var* (0~255 scale)."""
    if not _rand_bool(p):
        return img

    arr = np.asarray(img).astype(np.float32)
    noise = np.random.normal(0, var, arr.shape).astype(np.float32)
    arr += noise
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode=img.mode)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

_AUGS: List[Callable[[Image.Image], Image.Image]] = [
    gaussian_blur,
    brightness,
    contrast,
    add_gaussian_noise,
]


def apply_augmentations(img: Image.Image) -> Image.Image:
    """Apply a sequence of random augmentations (order fixed, each with its own prob)."""
    for fn in _AUGS:
        img = fn(img)
    return img
