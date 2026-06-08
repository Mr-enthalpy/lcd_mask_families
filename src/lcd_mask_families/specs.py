from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


SUPPORTED_COORDINATE_FRAMES = frozenset({"normalized_lcd_pupil", "pixel_index"})
SUPPORTED_OUTPUT_DTYPES = frozenset({"uint8", "float32"})
SUPPORTED_QUANTIZATION = frozenset({"round", "none"})


@dataclass(frozen=True)
class GridSpec:
    coordinate_frame: str
    shape_hw: tuple[int, int]

    def __post_init__(self) -> None:
        shape_hw = tuple(self.shape_hw)
        if self.coordinate_frame not in SUPPORTED_COORDINATE_FRAMES:
            raise ValueError(f"unsupported coordinate_frame: {self.coordinate_frame!r}")
        if len(shape_hw) != 2:
            raise ValueError("shape_hw must contain exactly two integers")
        if not all(isinstance(v, int) and v > 0 for v in shape_hw):
            raise ValueError("shape_hw values must be positive integers")
        object.__setattr__(self, "shape_hw", shape_hw)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "GridSpec":
        return cls(
            coordinate_frame=str(data["coordinate_frame"]),
            shape_hw=tuple(data["shape_hw"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "coordinate_frame": self.coordinate_frame,
            "shape_hw": list(self.shape_hw),
        }


@dataclass(frozen=True)
class ProjectionSpec:
    output_dtype: str = "uint8"
    value_range: tuple[float, float] = (0.0, 255.0)
    clip: bool = True
    quantization: str = "round"

    def __post_init__(self) -> None:
        value_range = tuple(float(v) for v in self.value_range)
        if self.output_dtype not in SUPPORTED_OUTPUT_DTYPES:
            raise ValueError(f"unsupported output_dtype: {self.output_dtype!r}")
        if self.quantization not in SUPPORTED_QUANTIZATION:
            raise ValueError(f"unsupported quantization: {self.quantization!r}")
        if len(value_range) != 2:
            raise ValueError("value_range must contain exactly two values")
        if value_range[0] >= value_range[1]:
            raise ValueError("value_range must be increasing")
        if self.output_dtype == "uint8" and self.quantization == "none":
            raise ValueError("uint8 projection requires quantization='round'")
        object.__setattr__(self, "value_range", value_range)
        object.__setattr__(self, "clip", bool(self.clip))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ProjectionSpec":
        return cls(
            output_dtype=str(data.get("output_dtype", "uint8")),
            value_range=tuple(data.get("value_range", (0.0, 255.0))),
            clip=bool(data.get("clip", True)),
            quantization=str(data.get("quantization", "round")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_dtype": self.output_dtype,
            "value_range": list(self.value_range),
            "clip": self.clip,
            "quantization": self.quantization,
        }


@dataclass(frozen=True)
class MaskInstanceSpec:
    family_id: str
    family_version: str
    parameters: Mapping[str, Any]
    grid: GridSpec
    projection: ProjectionSpec
    mask_id: str | None = None
    seed: int | None = None

    def __post_init__(self) -> None:
        if not self.family_id:
            raise ValueError("family_id must be non-empty")
        if not self.family_version:
            raise ValueError("family_version must be non-empty")
        if not isinstance(self.parameters, Mapping):
            raise ValueError("parameters must be a mapping")
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("seed must be an integer or None")
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MaskInstanceSpec":
        return cls(
            family_id=str(data["family_id"]),
            family_version=str(data["family_version"]),
            parameters=dict(data.get("parameters", {})),
            grid=GridSpec.from_dict(data["grid"]),
            projection=ProjectionSpec.from_dict(data["projection"]),
            mask_id=data.get("mask_id"),
            seed=data.get("seed"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "family_id": self.family_id,
            "family_version": self.family_version,
            "parameters": dict(self.parameters),
            "grid": self.grid.to_dict(),
            "projection": self.projection.to_dict(),
            "mask_id": self.mask_id,
            "seed": self.seed,
        }
