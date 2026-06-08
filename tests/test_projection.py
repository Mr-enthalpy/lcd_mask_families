import numpy as np

from lcd_mask_families import ProjectionSpec, project_display_mask


def test_uint8_projection_maps_unit_interval():
    mask = np.array([[0.0, 0.5, 1.0], [-1.0, 2.0, 0.25]])
    projection = ProjectionSpec(output_dtype="uint8", value_range=(0, 255))

    projected = project_display_mask(mask, projection)

    assert projected.dtype == np.uint8
    assert projected.min() >= 0
    assert projected.max() <= 255
    np.testing.assert_array_equal(projected[0], np.array([0, 128, 255], dtype=np.uint8))


def test_float_projection_preserves_float32_output():
    mask = np.array([[0.0, 0.5, 1.0]])
    projection = ProjectionSpec(
        output_dtype="float32",
        value_range=(0.0, 1.0),
        quantization="none",
    )

    projected = project_display_mask(mask, projection)

    assert projected.dtype == np.float32
    np.testing.assert_allclose(projected, mask.astype(np.float32))
