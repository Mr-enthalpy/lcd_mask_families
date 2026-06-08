import numpy as np

from lcd_mask_families import GridSpec, render_continuous_mask


def test_blocks_render_is_deterministic_and_invertible():
    grid = GridSpec(coordinate_frame="pixel_index", shape_hw=(16, 20))
    params = {
        "block_h": 4,
        "block_w": 5,
        "offset_y": 0,
        "offset_x": 0,
        "invert": False,
    }

    mask = render_continuous_mask("blocks", params, grid)
    repeated = render_continuous_mask("blocks", params, grid)
    inverted = render_continuous_mask("blocks", {**params, "invert": True}, grid)

    assert mask.shape == (16, 20)
    np.testing.assert_array_equal(mask, repeated)
    assert not np.array_equal(mask, inverted)
    np.testing.assert_array_equal(inverted, 1.0 - mask)
