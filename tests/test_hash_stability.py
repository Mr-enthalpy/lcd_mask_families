from pathlib import Path

from lcd_mask_families import (
    MaskIdentity,
    MaskInstanceSpec,
    hash_mask_instance,
    hash_mask_sequence,
    load_mask_instance_spec,
    load_mask_sequence_spec,
)


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def test_mask_instance_hash_is_stable_and_metadata_insensitive():
    spec = load_mask_instance_spec(EXAMPLES_DIR / "stripes_instance.yaml")
    changed_metadata = MaskInstanceSpec(
        family_id=spec.family_id,
        family_version=spec.family_version,
        parameters=spec.parameters,
        grid=spec.grid,
        projection=spec.projection,
        identity=MaskIdentity(mask_id="another_local_label"),
        metadata={"created_by": "local_test"},
    )

    assert hash_mask_instance(spec) == hash_mask_instance(spec)
    assert hash_mask_instance(spec) == hash_mask_instance(changed_metadata)


def test_mask_instance_hash_changes_when_parameters_change():
    spec = load_mask_instance_spec(EXAMPLES_DIR / "stripes_instance.yaml")
    changed = MaskInstanceSpec(
        family_id=spec.family_id,
        family_version=spec.family_version,
        parameters={**dict(spec.parameters), "angle_rad": 0.1},
        grid=spec.grid,
        projection=spec.projection,
        identity=spec.identity,
        metadata=spec.metadata,
    )

    assert hash_mask_instance(spec) != hash_mask_instance(changed)


def test_mask_sequence_hash_is_stable():
    spec = load_mask_sequence_spec(EXAMPLES_DIR / "simple_sequence.yaml")

    assert hash_mask_sequence(spec) == hash_mask_sequence(spec)
