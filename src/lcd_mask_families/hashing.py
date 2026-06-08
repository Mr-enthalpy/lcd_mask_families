from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any

import numpy as np

from .specs import MaskInstanceSpec


SCHEMA_VERSION = "lcd_mask_families.mask_instance.v1"


def mask_spec_hash(spec: MaskInstanceSpec) -> str:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "spec": _canonicalize(spec),
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def array_hash(mask: np.ndarray) -> str:
    array = np.ascontiguousarray(mask)
    digest = hashlib.sha256()
    digest.update(str(array.dtype).encode("utf-8"))
    digest.update(json.dumps(list(array.shape), separators=(",", ":")).encode("utf-8"))
    digest.update(array.tobytes(order="C"))
    return digest.hexdigest()


def _canonicalize(value: Any) -> Any:
    if isinstance(value, MaskInstanceSpec):
        return _canonicalize(value.to_dict())
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {str(k): _canonicalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonicalize(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value
