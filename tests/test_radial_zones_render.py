import numpy as np
import pytest

from lcd_mask_families import GridSpec, render_continuous_mask


def _params():
    return {
        "center_x": 0.0,
        "center_y": 0.0,
        "scale_x": 1.0,
        "scale_y": 1.0,
        "radial_frequency": 4.0,
        "quadratic_rate": 0.5,
        "phase_rad": 0.0,
        "duty": 0.5,
        "softness": 0.0,
    }


def test_radial_zones_render_is_deterministic_and_bounded():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    params = _params()

    first = render_continuous_mask("radial_zones", params, grid)
    second = render_continuous_mask("radial_zones", params, grid)

    assert first.shape == (64, 64)
    assert np.all(np.isfinite(first))
    assert np.min(first) >= 0.0
    assert np.max(first) <= 1.0
    np.testing.assert_array_equal(first, second)


def test_radial_frequency_change_changes_output():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    changed = _params()
    changed["radial_frequency"] = 5.0

    base_mask = render_continuous_mask("radial_zones", _params(), grid)
    changed_mask = render_continuous_mask("radial_zones", changed, grid)

    assert not np.array_equal(base_mask, changed_mask)


def test_center_change_changes_output():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    changed = _params()
    changed["center_x"] = 0.2
    changed["center_y"] = -0.1

    base_mask = render_continuous_mask("radial_zones", _params(), grid)
    changed_mask = render_continuous_mask("radial_zones", changed, grid)

    assert not np.array_equal(base_mask, changed_mask)


def test_radial_zones_softness_renders_bounded_output():
    grid = GridSpec("normalized_lcd_pupil", (32, 32))
    params = _params()
    params["softness"] = 0.05

    mask = render_continuous_mask("radial_zones", params, grid)

    assert mask.shape == (32, 32)
    assert np.all(np.isfinite(mask))
    assert np.min(mask) >= 0.0
    assert np.max(mask) <= 1.0


def test_radial_zones_elliptical_scaling_renders():
    grid = GridSpec("normalized_lcd_pupil", (32, 32))
    params = _params()
    params["scale_x"] = 0.75
    params["scale_y"] = 1.25

    mask = render_continuous_mask("radial_zones", params, grid)

    assert mask.shape == (32, 32)
    assert np.all(np.isfinite(mask))


def test_radial_zones_phase_convention_for_simple_radius():
    grid = GridSpec("normalized_lcd_pupil", (1, 4))
    params = {
        "center_x": 0.0,
        "center_y": 0.0,
        "scale_x": 1.0,
        "scale_y": 1.0,
        "radial_frequency": 1.0,
        "quadratic_rate": 0.0,
        "phase_rad": 0.0,
        "duty": 0.5,
        "softness": 0.0,
    }

    mask = render_continuous_mask("radial_zones", params, grid)
    x = np.array([[-0.75, -0.25, 0.25, 0.75]])
    y = np.array([[0.0, 0.0, 0.0, 0.0]])
    radius = np.sqrt(x * x + y * y)
    expected = (np.mod(radius, 1.0) < 0.5).astype(np.float64)

    np.testing.assert_array_equal(mask, expected)


@pytest.mark.parametrize("field", ["scale_x", "scale_y"])
def test_invalid_scale_raises_value_error(field):
    params = _params()
    params[field] = 0.0

    with pytest.raises(ValueError):
        render_continuous_mask("radial_zones", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_negative_radial_frequency_raises_value_error():
    params = _params()
    params["radial_frequency"] = -1.0

    with pytest.raises(ValueError):
        render_continuous_mask("radial_zones", params, GridSpec("normalized_lcd_pupil", (8, 8)))


@pytest.mark.parametrize("duty", [0.0, 1.0])
def test_invalid_duty_raises_value_error(duty):
    params = _params()
    params["duty"] = duty

    with pytest.raises(ValueError):
        render_continuous_mask("radial_zones", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_negative_softness_raises_value_error():
    params = _params()
    params["softness"] = -0.1

    with pytest.raises(ValueError):
        render_continuous_mask("radial_zones", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_zero_frequency_and_zero_quadratic_rate_raises_value_error():
    params = _params()
    params["radial_frequency"] = 0.0
    params["quadratic_rate"] = 0.0

    with pytest.raises(ValueError):
        render_continuous_mask("radial_zones", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_non_finite_parameter_raises_value_error():
    params = _params()
    params["center_x"] = float("nan")

    with pytest.raises(ValueError):
        render_continuous_mask("radial_zones", params, GridSpec("normalized_lcd_pupil", (8, 8)))
