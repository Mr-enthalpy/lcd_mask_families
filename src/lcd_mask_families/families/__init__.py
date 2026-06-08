from __future__ import annotations

from .blocks import FAMILY_METADATA as BLOCKS_METADATA, render_blocks
from .stripes import FAMILY_METADATA as STRIPES_METADATA, render_stripes


FAMILY_REGISTRY = {
    "stripes": render_stripes,
    "blocks": render_blocks,
}

FAMILY_METADATA_REGISTRY = {
    "stripes": STRIPES_METADATA,
    "blocks": BLOCKS_METADATA,
}


def _validate_registries() -> None:
    if set(FAMILY_REGISTRY) != set(FAMILY_METADATA_REGISTRY):
        raise RuntimeError("family render and metadata registries must have matching keys")
    for family_id, metadata in FAMILY_METADATA_REGISTRY.items():
        if metadata.family_id != family_id:
            raise RuntimeError("family metadata id must match registry key")
        if metadata.status != "active":
            raise RuntimeError("active family registry may only contain active metadata")


_validate_registries()

__all__ = [
    "FAMILY_METADATA_REGISTRY",
    "FAMILY_REGISTRY",
    "render_blocks",
    "render_stripes",
]
