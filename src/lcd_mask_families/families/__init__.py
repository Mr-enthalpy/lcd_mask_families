from __future__ import annotations

from .blocks import render_blocks
from .stripes import render_stripes


FAMILY_REGISTRY = {
    "stripes": render_stripes,
    "blocks": render_blocks,
}

__all__ = ["FAMILY_REGISTRY", "render_blocks", "render_stripes"]
