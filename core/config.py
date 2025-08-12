from types import SimpleNamespace
from pathlib import Path
import yaml

__all__ = ["load_config"]

def _dict_to_namespace(d: dict):
    """Recursively convert a mapping to SimpleNamespace objects."""
    if not isinstance(d, dict):
        return d
    return SimpleNamespace(**{k: _dict_to_namespace(v) for k, v in d.items()})


def load_config(cfg_path: str):
    """Load a YAML configuration file and return a nested SimpleNamespace.

    This helper keeps原有 YAML 的层次结构，但提供属性式访问。例如::

        cfg = load_config("configs/config.yaml")
        print(cfg.TEXT_SETTINGS.LANGUAGE)

    Args:
        cfg_path: Path to the YAML configuration file.

    Returns:
        SimpleNamespace: nested namespace reflecting YAML hierarchy.
    """
    path = Path(cfg_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")

    with path.open("r", encoding="utf-8") as f:
        raw_cfg = yaml.load(f, Loader=yaml.FullLoader) or {}

    return _dict_to_namespace(raw_cfg) 