from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .specs import MaskInstanceSpec, MaskSequenceSpec


def load_mask_instance_spec(path: str | Path) -> MaskInstanceSpec:
    return MaskInstanceSpec.from_dict(_load_mapping(path))


def load_mask_sequence_spec(path: str | Path) -> MaskSequenceSpec:
    return MaskSequenceSpec.from_dict(_load_mapping(path))


def dump_mask_instance_spec(spec: MaskInstanceSpec | Mapping[str, Any], path: str | Path) -> None:
    if not isinstance(spec, MaskInstanceSpec):
        spec = MaskInstanceSpec.from_dict(spec)
    _dump_mapping(spec.to_dict(), path)


def dump_mask_sequence_spec(spec: MaskSequenceSpec | Mapping[str, Any], path: str | Path) -> None:
    if not isinstance(spec, MaskSequenceSpec):
        spec = MaskSequenceSpec.from_dict(spec)
    _dump_mapping(spec.to_dict(), path)


def _load_mapping(path: str | Path) -> dict[str, Any]:
    spec_path = Path(path)
    with spec_path.open("r", encoding="utf-8") as handle:
        if spec_path.suffix.lower() in {".yaml", ".yml"}:
            import yaml

            payload = yaml.safe_load(handle)
        else:
            payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("spec file must contain a mapping")
    return payload


def _dump_mapping(payload: Mapping[str, Any], path: str | Path) -> None:
    spec_path = Path(path)
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    with spec_path.open("w", encoding="utf-8") as handle:
        if spec_path.suffix.lower() in {".yaml", ".yml"}:
            import yaml

            yaml.safe_dump(
                dict(payload),
                handle,
                sort_keys=False,
                allow_unicode=False,
            )
        else:
            json.dump(dict(payload), handle, indent=2, sort_keys=False)
            handle.write("\n")
