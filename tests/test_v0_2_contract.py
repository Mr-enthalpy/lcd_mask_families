from dataclasses import fields

import numpy as np
import pytest

import lcd_mask_families as public_api
from lcd_mask_families import (
    GridSpec,
    MaskInstanceSpec,
    ProjectionSpec,
    array_hash,
    get_family_metadata,
    list_families,
    mask_spec_hash,
    render_continuous_mask,
    render_display_mask,
)
from lcd_mask_families.families import FAMILY_METADATA_REGISTRY, FAMILY_REGISTRY
from lcd_mask_families.metadata import FamilyMetadata


ACTIVE_FAMILIES = (
    "blocks",
    "fourier_lowfreq",
    "radial_zones",
    "seeded_lowfreq_noise",
    "stripes",
)


def test_public_api_exports_v0_2_contract_names():
    expected = {
        "GridSpec",
        "ProjectionSpec",
        "MaskInstanceSpec",
        "render_continuous_mask",
        "project_display_mask",
        "render_display_mask",
        "mask_spec_hash",
        "array_hash",
        "list_families",
        "get_family_metadata",
    }

    assert expected.issubset(set(public_api.__all__))
    for name in expected:
        assert hasattr(public_api, name)


def test_active_family_registry_matches_v0_2_contract():
    assert list_families() == ACTIVE_FAMILIES
    assert tuple(sorted(FAMILY_REGISTRY)) == ACTIVE_FAMILIES
    assert tuple(sorted(FAMILY_METADATA_REGISTRY)) == ACTIVE_FAMILIES


def test_active_metadata_fields_are_complete_and_consistent():
    required_fields = {field.name for field in fields(FamilyMetadata)}

    for family_id in ACTIVE_FAMILIES:
        metadata = get_family_metadata(family_id)
        metadata_dict = metadata.to_dict()

        assert required_fields.issubset(metadata_dict)
        assert metadata.family_id == family_id
        assert metadata.family_version
        assert metadata.status == "active"
        for field_name in required_fields - {"family_id", "family_version", "status", "notes"}:
            assert isinstance(metadata_dict[field_name], bool)
        assert isinstance(metadata.notes, str)


def test_projection_change_changes_spec_hash():
    spec = MaskInstanceSpec(
        family_id="stripes",
        family_version="0.1.0",
        parameters={"angle_rad": 0.0, "period": 0.25, "duty": 0.5},
        grid=GridSpec("normalized_lcd_pupil", (16, 16)),
        projection=ProjectionSpec(output_dtype="uint8"),
    )
    changed = MaskInstanceSpec(
        family_id="stripes",
        family_version="0.1.0",
        parameters={"angle_rad": 0.0, "period": 0.25, "duty": 0.5},
        grid=GridSpec("normalized_lcd_pupil", (16, 16)),
        projection=ProjectionSpec(output_dtype="float32", value_range=(0.0, 1.0), quantization="none"),
    )

    assert mask_spec_hash(spec) == mask_spec_hash(spec)
    assert mask_spec_hash(spec) != mask_spec_hash(changed)


def test_grid_shape_change_changes_spec_hash():
    spec = MaskInstanceSpec(
        family_id="seeded_lowfreq_noise",
        family_version="0.1.0",
        parameters={"seed": 1234},
        grid=GridSpec("normalized_lcd_pupil", (16, 16)),
        projection=ProjectionSpec(),
        seed=1234,
    )
    changed = MaskInstanceSpec(
        family_id="seeded_lowfreq_noise",
        family_version="0.1.0",
        parameters={"seed": 1234},
        grid=GridSpec("normalized_lcd_pupil", (32, 16)),
        projection=ProjectionSpec(),
        seed=1234,
    )

    assert mask_spec_hash(spec) != mask_spec_hash(changed)


def test_same_spec_renders_same_display_mask_and_array_hash():
    spec = MaskInstanceSpec(
        family_id="seeded_lowfreq_noise",
        family_version="0.1.0",
        parameters={"seed": 1234, "max_frequency": 2},
        grid=GridSpec("normalized_lcd_pupil", (16, 16)),
        projection=ProjectionSpec(),
        seed=1234,
    )

    first = render_display_mask(spec.family_id, spec.parameters, spec.grid, spec.projection)
    second = render_display_mask(spec.family_id, spec.parameters, spec.grid, spec.projection)

    np.testing.assert_array_equal(first, second)
    assert array_hash(first) == array_hash(second)


def test_numpy_is_only_required_backend_for_v0_2():
    with pytest.raises(ValueError):
        render_continuous_mask(
            "stripes",
            {"angle_rad": 0.0, "period": 0.25, "duty": 0.5},
            GridSpec("normalized_lcd_pupil", (8, 8)),
            backend="torch",
        )
