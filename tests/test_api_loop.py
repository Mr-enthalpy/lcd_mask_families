import numpy as np

from lcd_mask_families import (
    GridSpec,
    MaskInstanceSpec,
    ProjectionSpec,
    array_hash,
    mask_spec_hash,
    project_display_mask,
    render_continuous_mask,
    render_display_mask,
)


def test_spec_to_display_mask_to_hash_loop():
    spec = MaskInstanceSpec(
        family_id="stripes",
        family_version="0.1.0",
        parameters={
            "angle_rad": 0.0,
            "period": 0.25,
            "phase_rad": 0.0,
            "duty": 0.5,
        },
        grid=GridSpec(coordinate_frame="normalized_lcd_pupil", shape_hw=(64, 64)),
        projection=ProjectionSpec(output_dtype="uint8"),
        mask_id="loop_test",
    )

    continuous = render_continuous_mask(spec.family_id, spec.parameters, spec.grid)
    manual_display = project_display_mask(continuous, spec.projection)
    composed_display = render_display_mask(
        spec.family_id,
        spec.parameters,
        spec.grid,
        spec.projection,
    )

    np.testing.assert_array_equal(manual_display, composed_display)
    assert isinstance(mask_spec_hash(spec), str)
    assert len(mask_spec_hash(spec)) > 0
    assert isinstance(array_hash(composed_display), str)
    assert len(array_hash(composed_display)) > 0
