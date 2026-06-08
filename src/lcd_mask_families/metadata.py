from __future__ import annotations

from dataclasses import asdict, dataclass


SUPPORTED_FAMILY_STATUSES = frozenset({"active", "planned", "experimental"})


@dataclass(frozen=True)
class FamilyMetadata:
    family_id: str
    family_version: str
    status: str
    differentiable: bool
    continuous_parameters: bool
    seeded: bool
    diffraction_oriented: bool
    orthogonal_basis: bool
    recommended_for_capture: bool
    recommended_for_optimization: bool
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.family_id:
            raise ValueError("family_id must be non-empty")
        if not self.family_version:
            raise ValueError("family_version must be non-empty")
        if self.status not in SUPPORTED_FAMILY_STATUSES:
            raise ValueError(f"unsupported family status: {self.status!r}")

        for field_name in (
            "differentiable",
            "continuous_parameters",
            "seeded",
            "diffraction_oriented",
            "orthogonal_basis",
            "recommended_for_capture",
            "recommended_for_optimization",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise ValueError(f"{field_name} must be a bool")

        if not isinstance(self.notes, str):
            raise ValueError("notes must be a string")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def list_families(*, status: str | None = None) -> tuple[str, ...]:
    from .families import FAMILY_METADATA_REGISTRY

    if status is not None and status not in SUPPORTED_FAMILY_STATUSES:
        raise ValueError(f"unsupported family status: {status!r}")

    family_ids = (
        family_id
        for family_id, metadata in FAMILY_METADATA_REGISTRY.items()
        if status is None or metadata.status == status
    )
    return tuple(sorted(family_ids))


def get_family_metadata(family_id: str) -> FamilyMetadata:
    from .families import FAMILY_METADATA_REGISTRY

    try:
        return FAMILY_METADATA_REGISTRY[family_id]
    except KeyError as exc:
        raise ValueError(f"unknown mask family: {family_id!r}") from exc


def get_family_metadata_dict(family_id: str) -> dict[str, object]:
    return get_family_metadata(family_id).to_dict()
