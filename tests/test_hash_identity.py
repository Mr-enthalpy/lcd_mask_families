import numpy as np

from lcd_mask_families import (
    GridSpec,
    MaskInstanceSpec,
    ProjectionSpec,
    array_hash,
    mask_spec_hash,
    render_continuous_mask,
)


def test_spec_hash_is_stable_and_parameter_sensitive():
    spec = MaskInstanceSpec(
        family_id="stripes",
        family_version="0.1.0",
        parameters={"angle_rad": 0.0, "period": 0.25, "duty": 0.5},
        grid=GridSpec("normalized_lcd_pupil", (32, 32)),
        projection=ProjectionSpec(),
    )
    changed = MaskInstanceSpec(
        family_id="stripes",
        family_version="0.1.0",
        parameters={"angle_rad": 0.1, "period": 0.25, "duty": 0.5},
        grid=GridSpec("normalized_lcd_pupil", (32, 32)),
        projection=ProjectionSpec(),
    )

    assert mask_spec_hash(spec) == mask_spec_hash(spec)
    assert mask_spec_hash(spec) != mask_spec_hash(changed)


def test_array_hash_is_stable_for_same_rendered_array():
    grid = GridSpec("normalized_lcd_pupil", (16, 16))
    params = {"angle_rad": 0.0, "period": 0.25, "duty": 0.5}

    first = render_continuous_mask("stripes", params, grid)
    second = np.array(first, copy=True)

    assert array_hash(first) == array_hash(second)
