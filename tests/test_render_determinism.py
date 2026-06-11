from pathlib import Path

import numpy as np

from lcd_mask_families import load_mask_instance_spec, render_mask_instance


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def test_repeated_example_rendering_produces_identical_arrays():
    for path in sorted(EXAMPLES_DIR.glob("*_instance.yaml")):
        spec = load_mask_instance_spec(path)

        first = render_mask_instance(spec)
        second = render_mask_instance(spec)

        np.testing.assert_array_equal(first.mask, second.mask)
        assert first.hash == second.hash
