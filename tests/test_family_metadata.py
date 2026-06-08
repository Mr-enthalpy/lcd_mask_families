import pytest

from lcd_mask_families import (
    FamilyMetadata,
    get_family_metadata,
    get_family_metadata_dict,
    list_families,
)
from lcd_mask_families.families import FAMILY_METADATA_REGISTRY, FAMILY_REGISTRY


def test_list_families_returns_active_implemented_families():
    assert list_families() == ("blocks", "fourier_lowfreq", "radial_zones", "stripes")
    assert list_families(status="active") == (
        "blocks",
        "fourier_lowfreq",
        "radial_zones",
        "stripes",
    )


def test_stripes_metadata():
    metadata = get_family_metadata("stripes")

    assert isinstance(metadata, FamilyMetadata)
    assert metadata.family_id == "stripes"
    assert metadata.status == "active"
    assert metadata.differentiable is True
    assert metadata.diffraction_oriented is True
    assert metadata.recommended_for_optimization is True


def test_blocks_metadata():
    metadata = get_family_metadata("blocks")

    assert metadata.family_id == "blocks"
    assert metadata.status == "active"
    assert metadata.differentiable is False
    assert metadata.recommended_for_capture is True
    assert metadata.recommended_for_optimization is False


def test_fourier_lowfreq_metadata():
    metadata = get_family_metadata("fourier_lowfreq")

    assert metadata.family_id == "fourier_lowfreq"
    assert metadata.status == "active"
    assert metadata.differentiable is True
    assert metadata.orthogonal_basis is True
    assert metadata.diffraction_oriented is False
    assert metadata.recommended_for_optimization is True


def test_radial_zones_metadata():
    metadata = get_family_metadata("radial_zones")

    assert metadata.family_id == "radial_zones"
    assert metadata.status == "active"
    assert metadata.differentiable is True
    assert metadata.diffraction_oriented is True
    assert metadata.orthogonal_basis is False
    assert metadata.recommended_for_capture is True
    assert metadata.recommended_for_optimization is True


def test_metadata_dict_is_plain_dict():
    metadata = get_family_metadata_dict("stripes")

    assert isinstance(metadata, dict)
    assert metadata["family_id"] == "stripes"
    assert metadata["status"] == "active"


def test_unknown_family_raises_value_error():
    with pytest.raises(ValueError):
        get_family_metadata("seeded_lowfreq_noise")


def test_unsupported_status_raises_value_error():
    with pytest.raises(ValueError):
        list_families(status="retired")


def test_metadata_registry_matches_rendering_registry():
    assert set(FAMILY_METADATA_REGISTRY) == set(FAMILY_REGISTRY)
    for family_id, metadata in FAMILY_METADATA_REGISTRY.items():
        assert metadata.family_id == family_id
        assert metadata.status == "active"
