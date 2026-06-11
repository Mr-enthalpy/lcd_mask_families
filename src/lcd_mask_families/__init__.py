from __future__ import annotations

from .constants import CONTRACT_VERSION, __version__
from .hashing import canonicalize_spec, hash_mask_instance, hash_mask_sequence
from .metadata import get_family_metadata, list_families
from .projection import project_display_mask
from .render import (
    render_continuous_mask,
    render_display_mask,
    render_mask_instance,
    render_mask_sequence,
)
from .serialization import (
    dump_mask_instance_spec,
    dump_mask_sequence_spec,
    load_mask_instance_spec,
    load_mask_sequence_spec,
)
from .specs import (
    GridSpec,
    MaskFamilySpec,
    MaskIdentity,
    MaskInstanceSpec,
    MaskSequenceSpec,
    ProjectionSpec,
    RenderedMask,
)


__all__ = [
    "__version__",
    "CONTRACT_VERSION",
    "MaskFamilySpec",
    "MaskInstanceSpec",
    "MaskSequenceSpec",
    "GridSpec",
    "ProjectionSpec",
    "MaskIdentity",
    "RenderedMask",
    "render_continuous_mask",
    "project_display_mask",
    "render_display_mask",
    "render_mask_instance",
    "render_mask_sequence",
    "canonicalize_spec",
    "hash_mask_instance",
    "hash_mask_sequence",
    "load_mask_instance_spec",
    "load_mask_sequence_spec",
    "dump_mask_instance_spec",
    "dump_mask_sequence_spec",
    "list_families",
    "get_family_metadata",
]
