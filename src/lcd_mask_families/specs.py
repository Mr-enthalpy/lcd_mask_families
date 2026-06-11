from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .constants import CONTRACT_VERSION


SUPPORTED_COORDINATE_FRAMES = frozenset({"normalized_lcd_pupil", "pixel_index"})
SUPPORTED_OUTPUT_DTYPES = frozenset({"uint8", "float32"})
SUPPORTED_QUANTIZATION = frozenset({"round", "none", "threshold"})
SUPPORTED_NORMALIZATION = frozenset({"none", "minmax"})


def _immutable_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class GridSpec:
    coordinate_frame: str
    shape_hw: tuple[int, int]
    extent: tuple[float, float, float, float] | None = None
    origin: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        shape_hw = tuple(self.shape_hw)
        if self.coordinate_frame not in SUPPORTED_COORDINATE_FRAMES:
            raise ValueError(f"unsupported coordinate_frame: {self.coordinate_frame!r}")
        if len(shape_hw) != 2:
            raise ValueError("shape_hw must contain exactly two integers")
        if not all(isinstance(v, int) and v > 0 for v in shape_hw):
            raise ValueError("shape_hw values must be positive integers")
        object.__setattr__(self, "shape_hw", shape_hw)

        if self.extent is not None:
            extent = tuple(float(v) for v in self.extent)
            if len(extent) != 4:
                raise ValueError("extent must contain exactly four values")
            object.__setattr__(self, "extent", extent)

        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "GridSpec":
        return cls(
            coordinate_frame=str(data["coordinate_frame"]),
            shape_hw=tuple(data["shape_hw"]),
            extent=tuple(data["extent"]) if data.get("extent") is not None else None,
            origin=data.get("origin"),
            metadata=dict(data.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "coordinate_frame": self.coordinate_frame,
            "shape_hw": list(self.shape_hw),
        }
        if self.extent is not None:
            payload["extent"] = list(self.extent)
        if self.origin is not None:
            payload["origin"] = self.origin
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class ProjectionSpec:
    output_dtype: str = "uint8"
    value_range: tuple[float, float] = (0.0, 255.0)
    quantization: str = "round"
    clip: bool = True
    threshold: float | None = None
    normalize: str = "none"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        value_range = tuple(float(v) for v in self.value_range)
        if self.output_dtype not in SUPPORTED_OUTPUT_DTYPES:
            raise ValueError(f"unsupported output_dtype: {self.output_dtype!r}")
        if self.quantization not in SUPPORTED_QUANTIZATION:
            raise ValueError(f"unsupported quantization: {self.quantization!r}")
        if self.normalize not in SUPPORTED_NORMALIZATION:
            raise ValueError(f"unsupported normalize policy: {self.normalize!r}")
        if len(value_range) != 2:
            raise ValueError("value_range must contain exactly two values")
        if value_range[0] >= value_range[1]:
            raise ValueError("value_range must be increasing")
        if self.output_dtype == "uint8" and self.quantization == "none":
            raise ValueError("uint8 projection requires quantization='round' or 'threshold'")
        if self.quantization == "threshold" and self.threshold is None:
            raise ValueError("threshold quantization requires threshold")
        if self.threshold is not None:
            threshold = float(self.threshold)
            if not 0.0 <= threshold <= 1.0:
                raise ValueError("threshold must be in [0, 1]")
            object.__setattr__(self, "threshold", threshold)
        object.__setattr__(self, "value_range", value_range)
        object.__setattr__(self, "clip", bool(self.clip))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ProjectionSpec":
        return cls(
            output_dtype=str(data.get("output_dtype", "uint8")),
            value_range=tuple(data.get("value_range", (0.0, 255.0))),
            quantization=str(data.get("quantization", "round")),
            clip=bool(data.get("clip", True)),
            threshold=data.get("threshold"),
            normalize=str(data.get("normalize", "none")),
            metadata=dict(data.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "output_dtype": self.output_dtype,
            "value_range": list(self.value_range),
            "quantization": self.quantization,
            "clip": self.clip,
            "normalize": self.normalize,
        }
        if self.threshold is not None:
            payload["threshold"] = self.threshold
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class MaskIdentity:
    mask_id: str | None = None
    hash: str | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> "MaskIdentity":
        if data is None:
            return cls()
        return cls(mask_id=data.get("mask_id"), hash=data.get("hash"))

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.mask_id is not None:
            payload["mask_id"] = self.mask_id
        if self.hash is not None:
            payload["hash"] = self.hash
        return payload


@dataclass(frozen=True)
class MaskFamilySpec:
    family_id: str
    family_version: str
    parameter_schema: Mapping[str, Any]
    differentiability: Mapping[str, Any]
    design_intent: Mapping[str, Any]
    response_prior: Mapping[str, Any]
    status: str = "active"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.family_id:
            raise ValueError("family_id must be non-empty")
        if not self.family_version:
            raise ValueError("family_version must be non-empty")
        object.__setattr__(self, "parameter_schema", _immutable_mapping(self.parameter_schema))
        object.__setattr__(self, "differentiability", _immutable_mapping(self.differentiability))
        object.__setattr__(self, "design_intent", _immutable_mapping(self.design_intent))
        object.__setattr__(self, "response_prior", _immutable_mapping(self.response_prior))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MaskFamilySpec":
        return cls(
            family_id=str(data["family_id"]),
            family_version=str(data["family_version"]),
            parameter_schema=dict(data.get("parameter_schema", {})),
            differentiability=dict(data.get("differentiability", {})),
            design_intent=dict(data.get("design_intent", {})),
            response_prior=dict(data.get("response_prior", {})),
            status=str(data.get("status", "active")),
            metadata=dict(data.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "family_id": self.family_id,
            "family_version": self.family_version,
            "status": self.status,
            "parameter_schema": dict(self.parameter_schema),
            "differentiability": dict(self.differentiability),
            "design_intent": dict(self.design_intent),
            "response_prior": dict(self.response_prior),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class MaskInstanceSpec:
    family_id: str
    family_version: str
    parameters: Mapping[str, Any]
    grid: GridSpec
    projection: ProjectionSpec
    schema_version: str = CONTRACT_VERSION
    identity: MaskIdentity = field(default_factory=MaskIdentity)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    seed: int | None = None
    mask_id: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported schema_version: {self.schema_version!r}")
        if not self.family_id:
            raise ValueError("family_id must be non-empty")
        if not self.family_version:
            raise ValueError("family_version must be non-empty")
        if not isinstance(self.parameters, Mapping):
            raise ValueError("parameters must be a mapping")
        if not isinstance(self.grid, GridSpec):
            object.__setattr__(self, "grid", GridSpec.from_dict(self.grid))  # type: ignore[arg-type]
        if not isinstance(self.projection, ProjectionSpec):
            object.__setattr__(self, "projection", ProjectionSpec.from_dict(self.projection))  # type: ignore[arg-type]
        if not isinstance(self.identity, MaskIdentity):
            object.__setattr__(self, "identity", MaskIdentity.from_dict(self.identity))  # type: ignore[arg-type]
        if self.seed is not None and (not isinstance(self.seed, int) or isinstance(self.seed, bool)):
            raise ValueError("seed must be an integer or None")

        identity = self.identity
        if self.mask_id is not None and identity.mask_id is None:
            identity = MaskIdentity(mask_id=self.mask_id, hash=identity.hash)
            object.__setattr__(self, "identity", identity)

        object.__setattr__(self, "parameters", _immutable_mapping(self.parameters))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MaskInstanceSpec":
        identity_data = data.get("identity")
        if identity_data is None and ("mask_id" in data or "hash" in data):
            identity_data = {"mask_id": data.get("mask_id"), "hash": data.get("hash")}
        return cls(
            schema_version=str(data.get("schema_version", CONTRACT_VERSION)),
            family_id=str(data["family_id"]),
            family_version=str(data["family_version"]),
            parameters=dict(data.get("parameters", {})),
            grid=GridSpec.from_dict(data["grid"]),
            projection=ProjectionSpec.from_dict(data["projection"]),
            identity=MaskIdentity.from_dict(identity_data),
            metadata=dict(data.get("metadata", {})),
            seed=data.get("seed"),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "family_id": self.family_id,
            "family_version": self.family_version,
            "parameters": dict(self.parameters),
            "grid": self.grid.to_dict(),
            "projection": self.projection.to_dict(),
            "identity": self.identity.to_dict(),
            "metadata": dict(self.metadata),
        }
        if self.seed is not None:
            payload["seed"] = self.seed
        return payload


@dataclass(frozen=True)
class MaskSequenceSpec:
    sequence_id: str
    masks: tuple[MaskInstanceSpec, ...]
    schema_version: str = CONTRACT_VERSION
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.schema_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported schema_version: {self.schema_version!r}")
        if not self.sequence_id:
            raise ValueError("sequence_id must be non-empty")
        masks = tuple(
            mask if isinstance(mask, MaskInstanceSpec) else MaskInstanceSpec.from_dict(mask)
            for mask in self.masks
        )
        object.__setattr__(self, "masks", masks)
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MaskSequenceSpec":
        return cls(
            schema_version=str(data.get("schema_version", CONTRACT_VERSION)),
            sequence_id=str(data["sequence_id"]),
            masks=tuple(MaskInstanceSpec.from_dict(item) for item in data.get("masks", ())),
            metadata=dict(data.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "sequence_id": self.sequence_id,
            "masks": [mask.to_dict() for mask in self.masks],
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class RenderedMask:
    mask: Any
    mask_id: str
    hash: str
    family_id: str
    family_version: str
    grid: GridSpec
    projection: ProjectionSpec
    dtype: str
    shape_hw: tuple[int, int]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "shape_hw", tuple(self.shape_hw))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))
