import numpy as np

from lcd_mask_families import GridSpec, render_continuous_mask


def test_stripes_render_is_deterministic_and_bounded():
    grid = GridSpec(coordinate_frame="normalized_lcd_pupil", shape_hw=(64, 64))
    params = {
        "angle_rad": 0.785398163,
        "period": 0.25,
        "phase_rad": 0.0,
        "duty": 0.5,
        "softness": 0.0,
    }

    first = render_continuous_mask("stripes", params, grid)
    second = render_continuous_mask("stripes", params, grid)

    assert first.shape == (64, 64)
    assert np.all(np.isfinite(first))
    assert np.min(first) >= 0.0
    assert np.max(first) <= 1.0
    np.testing.assert_array_equal(first, second)
