from pathlib import Path

from lcd_mask_families import load_mask_sequence_spec, render_mask_sequence


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def test_sequence_render_preserves_order():
    sequence = load_mask_sequence_spec(EXAMPLES_DIR / "simple_sequence.yaml")
    rendered = render_mask_sequence(sequence)

    assert [item.mask_id for item in rendered] == [
        "sequence_stripes_000",
        "sequence_blocks_001",
    ]
    assert [item.family_id for item in rendered] == ["stripes", "blocks"]
