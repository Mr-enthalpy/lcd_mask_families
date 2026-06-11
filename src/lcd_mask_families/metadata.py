from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


SUPPORTED_FAMILY_STATUSES = frozenset({"active", "planned", "experimental"})
SUPPORTED_PROJECTION_DIFFERENTIABILITY = frozenset({"exact", "relaxed", "ste", "none"})
SUPPORTED_RANDOM_WALK_RISK = frozenset({"low", "medium", "high"})


def _mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class FamilyMetadata:
    family_id: str
    family_version: str
    status: str
    differentiability: Mapping[str, Any]
    design_intent: Mapping[str, Any]
    response_prior: Mapping[str, Any]
    notes: str = ""
    parameter_schema: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.family_id:
            raise ValueError("family_id must be non-empty")
        if not self.family_version:
            raise ValueError("family_version must be non-empty")
        if self.status not in SUPPORTED_FAMILY_STATUSES:
            raise ValueError(f"unsupported family status: {self.status!r}")

        differentiability = dict(self.differentiability)
        design_intent = dict(self.design_intent)
        response_prior = dict(self.response_prior)

        required_diff = {
            "continuous_parameters",
            "differentiable_render",
            "differentiable_projection",
            "seed_is_optimization_variable",
        }
        required_design = {
            "diffraction_oriented",
            "orthogonal_basis",
            "seeded_random",
            "recommended_for_capture",
            "recommended_for_optimization",
            "random_walk_risk",
        }
        if not required_diff.issubset(differentiability):
            missing = sorted(required_diff - set(differentiability))
            raise ValueError(f"missing differentiability fields: {missing!r}")
        if not required_design.issubset(design_intent):
            missing = sorted(required_design - set(design_intent))
            raise ValueError(f"missing design_intent fields: {missing!r}")
        if "validated_by_measured_psf" not in response_prior:
            response_prior["validated_by_measured_psf"] = False
        if "expected_effect" not in response_prior:
            response_prior["expected_effect"] = []

        for field_name in (
            "continuous_parameters",
            "differentiable_render",
            "seed_is_optimization_variable",
        ):
            if not isinstance(differentiability[field_name], bool):
                raise ValueError(f"differentiability.{field_name} must be a bool")
        if differentiability["differentiable_projection"] not in SUPPORTED_PROJECTION_DIFFERENTIABILITY:
            raise ValueError("unsupported differentiable_projection")

        for field_name in (
            "diffraction_oriented",
            "orthogonal_basis",
            "seeded_random",
            "recommended_for_capture",
            "recommended_for_optimization",
        ):
            if not isinstance(design_intent[field_name], bool):
                raise ValueError(f"design_intent.{field_name} must be a bool")
        if design_intent["random_walk_risk"] not in SUPPORTED_RANDOM_WALK_RISK:
            raise ValueError("unsupported random_walk_risk")

        if not isinstance(response_prior["expected_effect"], list):
            raise ValueError("response_prior.expected_effect must be a list")
        if response_prior["validated_by_measured_psf"] is not False:
            raise ValueError("validated_by_measured_psf must be false in this repository")

        object.__setattr__(self, "differentiability", _mapping(differentiability))
        object.__setattr__(self, "design_intent", _mapping(design_intent))
        object.__setattr__(self, "response_prior", _mapping(response_prior))
        object.__setattr__(self, "parameter_schema", _mapping(self.parameter_schema))

    @property
    def differentiable(self) -> bool:
        return bool(self.differentiability["differentiable_render"])

    @property
    def continuous_parameters(self) -> bool:
        return bool(self.differentiability["continuous_parameters"])

    @property
    def seeded(self) -> bool:
        return bool(self.design_intent["seeded_random"])

    @property
    def diffraction_oriented(self) -> bool:
        return bool(self.design_intent["diffraction_oriented"])

    @property
    def orthogonal_basis(self) -> bool:
        return bool(self.design_intent["orthogonal_basis"])

    @property
    def recommended_for_capture(self) -> bool:
        return bool(self.design_intent["recommended_for_capture"])

    @property
    def recommended_for_optimization(self) -> bool:
        return bool(self.design_intent["recommended_for_optimization"])

    def to_dict(self) -> dict[str, object]:
        return {
            "family_id": self.family_id,
            "family_version": self.family_version,
            "status": self.status,
            "differentiability": dict(self.differentiability),
            "design_intent": dict(self.design_intent),
            "response_prior": dict(self.response_prior),
            "parameter_schema": dict(self.parameter_schema),
            "notes": self.notes,
        }


def list_families(*, status: str | None = None) -> tuple[str, ...]:
    from .families.registry import FAMILY_METADATA_REGISTRY

    if status is not None and status not in SUPPORTED_FAMILY_STATUSES:
        raise ValueError(f"unsupported family status: {status!r}")

    family_ids = (
        family_id
        for family_id, metadata in FAMILY_METADATA_REGISTRY.items()
        if status is None or metadata.status == status
    )
    return tuple(sorted(family_ids))


def get_family_metadata(family_id: str) -> dict[str, object]:
    from .families.registry import FAMILY_METADATA_REGISTRY

    try:
        return FAMILY_METADATA_REGISTRY[family_id].to_dict()
    except KeyError as exc:
        raise ValueError(f"unknown mask family: {family_id!r}") from exc
