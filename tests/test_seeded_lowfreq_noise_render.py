import numpy as np
import pytest

from lcd_mask_families import GridSpec, render_continuous_mask


def _params():
    return {
        "seed": 1234,
        "max_frequency": 3,
        "spectrum_decay": 1.0,
        "coefficient_scale": 1.0,
        "bias": 0.0,
        "contrast": 1.0,
        "activation": "sigmoid",
    }


def test_seeded_lowfreq_noise_render_is_deterministic_and_bounded():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    params = _params()

    first = render_continuous_mask("seeded_lowfreq_noise", params, grid)
    second = render_continuous_mask("seeded_lowfreq_noise", params, grid)

    assert first.shape == (64, 64)
    assert np.all(np.isfinite(first))
    assert np.min(first) >= 0.0
    assert np.max(first) <= 1.0
    np.testing.assert_array_equal(first, second)


def test_seed_change_changes_output():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    changed = _params()
    changed["seed"] = 5678

    base_mask = render_continuous_mask("seeded_lowfreq_noise", _params(), grid)
    changed_mask = render_continuous_mask("seeded_lowfreq_noise", changed, grid)

    assert not np.array_equal(base_mask, changed_mask)


def test_max_frequency_change_changes_output():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    changed = _params()
    changed["max_frequency"] = 2

    base_mask = render_continuous_mask("seeded_lowfreq_noise", _params(), grid)
    changed_mask = render_continuous_mask("seeded_lowfreq_noise", changed, grid)

    assert not np.array_equal(base_mask, changed_mask)


def test_coefficient_scale_change_changes_output():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    changed = _params()
    changed["coefficient_scale"] = 0.25

    base_mask = render_continuous_mask("seeded_lowfreq_noise", _params(), grid)
    changed_mask = render_continuous_mask("seeded_lowfreq_noise", changed, grid)

    assert not np.array_equal(base_mask, changed_mask)


def test_seeded_lowfreq_noise_linear_clip_activation():
    grid = GridSpec("normalized_lcd_pupil", (32, 32))
    params = _params()
    params["bias"] = 0.5
    params["coefficient_scale"] = 0.25
    params["activation"] = "linear_clip"

    mask = render_continuous_mask("seeded_lowfreq_noise", params, grid)

    assert mask.shape == (32, 32)
    assert np.all(np.isfinite(mask))
    assert np.min(mask) >= 0.0
    assert np.max(mask) <= 1.0


def test_zero_coefficient_scale_renders_bias_only_field():
    grid = GridSpec("normalized_lcd_pupil", (8, 8))
    params = _params()
    params["coefficient_scale"] = 0.0
    params["bias"] = 0.25
    params["contrast"] = 2.0

    mask = render_continuous_mask("seeded_lowfreq_noise", params, grid)
    expected = 1.0 / (1.0 + np.exp(-0.5))

    np.testing.assert_allclose(mask, np.full((8, 8), expected))


def test_seeded_lowfreq_noise_is_spatially_smooth_at_default_frequency():
    grid = GridSpec("normalized_lcd_pupil", (64, 64))
    mask = render_continuous_mask("seeded_lowfreq_noise", _params(), grid)

    horizontal_mad = np.mean(np.abs(np.diff(mask, axis=1)))
    vertical_mad = np.mean(np.abs(np.diff(mask, axis=0)))

    assert horizontal_mad < 0.25
    assert vertical_mad < 0.25


@pytest.mark.parametrize("seed", [1.5, True])
def test_invalid_seed_raises_value_error(seed):
    params = _params()
    params["seed"] = seed

    with pytest.raises(ValueError):
        render_continuous_mask("seeded_lowfreq_noise", params, GridSpec("normalized_lcd_pupil", (8, 8)))


@pytest.mark.parametrize("max_frequency", [0, 1.5, True])
def test_invalid_max_frequency_raises_value_error(max_frequency):
    params = _params()
    params["max_frequency"] = max_frequency

    with pytest.raises(ValueError):
        render_continuous_mask("seeded_lowfreq_noise", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_negative_spectrum_decay_raises_value_error():
    params = _params()
    params["spectrum_decay"] = -1.0

    with pytest.raises(ValueError):
        render_continuous_mask("seeded_lowfreq_noise", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_negative_coefficient_scale_raises_value_error():
    params = _params()
    params["coefficient_scale"] = -1.0

    with pytest.raises(ValueError):
        render_continuous_mask("seeded_lowfreq_noise", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_invalid_contrast_raises_value_error():
    params = _params()
    params["contrast"] = 0.0

    with pytest.raises(ValueError):
        render_continuous_mask("seeded_lowfreq_noise", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_invalid_activation_raises_value_error():
    params = _params()
    params["activation"] = "relu"

    with pytest.raises(ValueError):
        render_continuous_mask("seeded_lowfreq_noise", params, GridSpec("normalized_lcd_pupil", (8, 8)))


def test_non_finite_parameter_raises_value_error():
    params = _params()
    params["bias"] = float("nan")

    with pytest.raises(ValueError):
        render_continuous_mask("seeded_lowfreq_noise", params, GridSpec("normalized_lcd_pupil", (8, 8)))
