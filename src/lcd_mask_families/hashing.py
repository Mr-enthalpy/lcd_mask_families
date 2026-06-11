from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

import numpy as np

from .constants import CONTRACT_VERSION, __version__
from .specs import MaskInstanceSpec, MaskSequenceSpec


def canonicalize_spec(spec: Any) -> dict[str, Any]:
    canonical = _canonicalize(spec)
    if not isinstance(canonical, dict):
        raise ValueError("canonicalized spec must be a mapping")
    return canonical


def hash_mask_instance(spec: MaskInstanceSpec | Mapping[str, Any]) -> str:
    if not isinstance(spec, MaskInstanceSpec):
        spec = MaskInstanceSpec.from_dict(spec)
    payload = {
        "contract_version": CONTRACT_VERSION,
        "renderer_version": __version__,
        "family_id": spec.family_id,
        "family_version": spec.family_version,
        "parameters": _canonicalize(dict(spec.parameters)),
        "grid": _canonicalize(spec.grid.to_dict()),
        "projection": _canonicalize(spec.projection.to_dict()),
        "seed": spec.seed,
    }
    return _hash_payload(payload)


def hash_mask_sequence(spec: MaskSequenceSpec | Mapping[str, Any]) -> str:
    if not isinstance(spec, MaskSequenceSpec):
        spec = MaskSequenceSpec.from_dict(spec)
    payload = {
        "contract_version": CONTRACT_VERSION,
        "renderer_version": __version__,
        "sequence_id": spec.sequence_id,
        "mask_hashes": [hash_mask_instance(mask) for mask in spec.masks],
    }
    return _hash_payload(payload)


def _hash_payload(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        _canonicalize(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _canonicalize(value: Any) -> Any:
    if isinstance(value, MaskInstanceSpec):
        return {
            "schema_version": value.schema_version,
            "family_id": value.family_id,
            "family_version": value.family_version,
            "parameters": _canonicalize(dict(value.parameters)),
            "grid": _canonicalize(value.grid.to_dict()),
            "projection": _canonicalize(value.projection.to_dict()),
            "identity": _canonicalize(value.identity.to_dict()),
            "metadata": _canonicalize(dict(value.metadata)),
            "seed": value.seed,
        }
    if isinstance(value, MaskSequenceSpec):
        return {
            "schema_version": value.schema_version,
            "sequence_id": value.sequence_id,
            "masks": [_canonicalize(mask) for mask in value.masks],
            "metadata": _canonicalize(dict(value.metadata)),
        }
    if is_dataclass(value):
        return _canonicalize(asdict(value))
    if isinstance(value, Mapping):
        return {str(k): _canonicalize(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple)):
        return [_canonicalize(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value
