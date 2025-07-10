"""Visualization subpackage (animations, helpers)."""

from .animation import AnimationController
import importlib

def visualize_k_labeling(*args, **kwargs):
    """Lazy import and call to static visualize_k_labeling."""
    mod = importlib.import_module("src.visualization.static")
    return getattr(mod, "visualize_k_labeling")(*args, **kwargs)

__all__ = [
    "AnimationController",
    "visualize_k_labeling",
] 