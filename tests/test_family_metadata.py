import pytest

from lcd_mask_families import get_family_metadata, list_families
from lcd_mask_families.families.registry import FAMILY_METADATA_REGISTRY, FAMILY_REGISTRY


ACTIVE_FAMILIES = (
    "blocks",
    "fourier_lowfreq",
    "radial_zones",
    "seeded_lowfreq_noise",
    "stripes",
)


def test_list_families_returns_active_implemented_families():
    assert list_families() == ACTIVE_FAMILIES
    assert list_families(status="active") == ACTIVE_FAMILIES


def test_metadata_exists_for_all_active_families():
    for family_id in ACTIVE_FAMILIES:
        metadata = get_family_metadata(family_id)

        assert metadata["family_id"] == family_id
        assert metadata["status"] == "active"
        assert "differentiability" in metadata
        assert "design_intent" in metadata
        assert "response_prior" in metadata
        assert metadata["response_prior"]["validated_by_measured_psf"] is False
        assert metadata["differentiability"]["seed_is_optimization_variable"] is False


def test_metadata_registry_matches_rendering_registry():
    assert set(FAMILY_METADATA_REGISTRY) == set(FAMILY_REGISTRY)
    for family_id, metadata in FAMILY_METADATA_REGISTRY.items():
        assert metadata.family_id == family_id
        assert metadata.status == "active"


def test_unknown_family_raises_value_error():
    with pytest.raises(ValueError):
        get_family_metadata("multi_stripes")
