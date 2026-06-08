import numpy as np
import pytest

from lcd_mask_families import GridSpec, render_continuous_mask


def _params():
    return {
        "modes": [
            {"kx": 1, "ky": 0, "cos": 1.0, "sin": 0.0},
            {"kx": 0, "ky": 1, "cos": 0.25, "sin": 0.5},
        ],
        "bias": 0.0,
        "contrast": 1.0,
        "activation": "sigmoid",
    }


def test_fourier_lowfreq_render_is_deterministic_and_bounded():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    params = _params()

    first = render_continuous_mask("fourier_lowfreq", params, grid)
    second = render_continuous_mask("fourier_lowfreq", params, grid)

    assert first.shape == (64, 64)
    assert np.all(np.isfinite(first))
    assert np.min(first) >= 0.0
    assert np.max(first) <= 1.0
    np.testing.assert_array_equal(first, second)


def test_fourier_lowfreq_coefficient_change_changes_output():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    params = _params()
    changed = _params()
    changed["modes"] = [
        {"kx": 1, "ky": 0, "cos": 0.75, "sin": 0.0},
        {"kx": 0, "ky": 1, "cos": 0.25, "sin": 0.5},
    ]

    base_mask = render_continuous_mask("fourier_lowfreq", params, grid)
    changed_mask = render_continuous_mask("fourier_lowfreq", changed, grid)

    assert not np.array_equal(base_mask, changed_mask)


def test_fourier_lowfreq_linear_clip_activation():
    grid = GridSpec("normalized_lcd_pupil", (16, 16))
    params = {
        "modes": [{"kx": 1, "ky": 0, "cos": 0.5, "sin": 0.0}],
        "bias": 0.5,
        "contrast": 1.0,
        "activation": "linear_clip",
    }

    mask = render_continuous_mask("fourier_lowfreq", params, grid)

    assert mask.shape == (16, 16)
    assert np.min(mask) >= 0.0
    assert np.max(mask) <= 1.0


def test_fourier_lowfreq_phase_convention_uses_pi_over_normalized_grid():
    grid = GridSpec("normalized_lcd_pupil", (1, 4))
    params = {
        "modes": [{"kx": 1, "ky": 0, "cos": 0.25, "sin": 0.0}],
        "bias": 0.5,
        "contrast": 1.0,
        "activation": "linear_clip",
    }

    mask = render_continuous_mask("fourier_lowfreq", params, grid)
    x = np.array([[-0.75, -0.25, 0.25, 0.75]])
    expected = 0.5 + 0.25 * np.cos(np.pi * x)

    np.testing.assert_allclose(mask, expected)


def test_fourier_lowfreq_empty_modes_raise_value_error():
    with pytest.raises(ValueError):
        render_continuous_mask(
            "fourier_lowfreq",
            {"modes": [], "activation": "sigmoid"},
            GridSpec("normalized_lcd_pupil", (8, 8)),
        )


def test_fourier_lowfreq_non_integer_frequency_raises_value_error():
    with pytest.raises(ValueError):
        render_continuous_mask(
            "fourier_lowfreq",
            {"modes": [{"kx": 1.5, "ky": 0, "cos": 1.0}]},
            GridSpec("normalized_lcd_pupil", (8, 8)),
        )


def test_fourier_lowfreq_zero_frequency_mode_raises_value_error():
    with pytest.raises(ValueError):
        render_continuous_mask(
            "fourier_lowfreq",
            {"modes": [{"kx": 0, "ky": 0, "cos": 1.0}]},
            GridSpec("normalized_lcd_pupil", (8, 8)),
        )


def test_fourier_lowfreq_invalid_activation_raises_value_error():
    params = _params()
    params["activation"] = "relu"

    with pytest.raises(ValueError):
        render_continuous_mask("fourier_lowfreq", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_fourier_lowfreq_invalid_contrast_raises_value_error():
    params = _params()
    params["contrast"] = 0.0

    with pytest.raises(ValueError):
        render_continuous_mask("fourier_lowfreq", params, GridSpec("normalized_lcd_pupil", (8, 8)))
