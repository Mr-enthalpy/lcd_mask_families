from pathlib import Path

from lcd_mask_families import load_mask_instance_spec, render_mask_instance


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"
ACTIVE_FAMILIES = (
    "blocks",
    "fourier_lowfreq",
    "radial_zones",
    "seeded_lowfreq_noise",
    "stripes",
)


def test_all_active_family_yaml_examples_load_and_render():
    for family_id in ACTIVE_FAMILIES:
        spec = load_mask_instance_spec(EXAMPLES_DIR / f"{family_id}_instance.yaml")
        rendered = render_mask_instance(spec)

        assert spec.family_id == family_id
        assert rendered.family_id == family_id
        assert rendered.mask.shape == spec.grid.shape_hw
        assert rendered.hash
        assert rendered.mask_id == spec.identity.mask_id
