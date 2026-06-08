import json
from pathlib import Path

import numpy as np

from lcd_mask_families import (
    MaskInstanceSpec,
    array_hash,
    mask_spec_hash,
    project_display_mask,
    render_continuous_mask,
    render_display_mask,
)
from lcd_mask_families.families import FAMILY_REGISTRY


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def _active_example_paths():
    expected = {f"{family_id}_instance.json" for family_id in FAMILY_REGISTRY}
    paths = {path.name: path for path in EXAMPLES_DIR.glob("*_instance.json")}
    assert set(paths) == expected
    return tuple(paths[name] for name in sorted(paths))


def test_active_json_examples_round_trip_and_render_deterministically():
    for path in _active_example_paths():
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        spec = MaskInstanceSpec.from_dict(payload)
        assert spec.family_id in FAMILY_REGISTRY

        continuous_a = render_continuous_mask(spec.family_id, spec.parameters, spec.grid)
        continuous_b = render_continuous_mask(spec.family_id, spec.parameters, spec.grid)
        display_manual = project_display_mask(continuous_a, spec.projection)
        display_composed = render_display_mask(
            spec.family_id,
            spec.parameters,
            spec.grid,
            spec.projection,
        )
        display_repeated = render_display_mask(
            spec.family_id,
            spec.parameters,
            spec.grid,
            spec.projection,
        )

        assert continuous_a.shape == spec.grid.shape_hw
        assert continuous_a.dtype == np.float64
        assert np.all(np.isfinite(continuous_a))
        assert np.min(continuous_a) >= 0.0
        assert np.max(continuous_a) <= 1.0
        np.testing.assert_array_equal(continuous_a, continuous_b)
        np.testing.assert_array_equal(display_manual, display_composed)
        np.testing.assert_array_equal(display_composed, display_repeated)

        if spec.projection.output_dtype == "uint8":
            assert display_composed.dtype == np.uint8
        elif spec.projection.output_dtype == "float32":
            assert display_composed.dtype == np.float32

        assert display_composed.shape == spec.grid.shape_hw
        assert isinstance(mask_spec_hash(spec), str)
        assert isinstance(array_hash(display_composed), str)
        assert mask_spec_hash(spec)
        assert array_hash(display_composed)
