import json
from pathlib import Path

import yaml
from jsonschema import validate

from lcd_mask_families import get_family_metadata, list_families


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"
SCHEMAS_DIR = ROOT / "schemas"


def _load_schema(name):
    with (SCHEMAS_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_yaml_examples_validate_against_json_schemas():
    instance_schema = _load_schema("mask_instance_spec.schema.json")
    sequence_schema = _load_schema("mask_sequence_spec.schema.json")

    for path in EXAMPLES_DIR.glob("*_instance.yaml"):
        validate(_load_yaml(path), instance_schema)
    sequence_payload = _load_yaml(EXAMPLES_DIR / "simple_sequence.yaml")
    validate(sequence_payload, sequence_schema)
    for mask_payload in sequence_payload["masks"]:
        validate(mask_payload, instance_schema)


def test_family_metadata_validates_against_schema():
    schema = _load_schema("family_metadata.schema.json")

    for family_id in list_families():
        validate(get_family_metadata(family_id), schema)
