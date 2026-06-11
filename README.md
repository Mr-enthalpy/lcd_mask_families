# lcd_mask_families

`lcd_mask_families` is a small pure-function kernel library for deterministic,
parameterized LCD mask families.

It owns only the mathematical map:

```text
family + parameters + grid + projection policy -> mask
```

Downstream repositories decide how to use the rendered masks. `optic_system`
may wrap this package for capture plans and physical LCD display. `LCD_forward`
may wrap the same contract for differentiable mask generation and
LCD-to-operator modelling. `reconstruction` may consume mask identity or mask
sequences. This package must not import or understand those repositories.

## Install

```bash
pip install -e .
```

For tests:

```bash
pip install -e ".[dev]"
pytest -q
```

## v0.1 Stable Contract

v0.1 stable:

* spec structure for `MaskInstanceSpec` and `MaskSequenceSpec`;
* public pure rendering functions;
* deterministic hash identity for mask instances and sequences;
* active family registry;
* active family metadata shape;
* minimal JSON/YAML examples in `examples/`;
* JSON schema locations in `schemas/`.

Not stable:

* planned family list;
* downstream wrappers;
* physical PSF interpretation;
* optimization recipes;
* torch or other differentiable backend support.

Breaking spec changes require a `CONTRACT_VERSION` bump. New optional fields may
be added without breaking compatibility if defaults exist. Active family
parameter names should not change silently. Hash semantics must remain stable
within a contract version.

## Public API

```python
__version__
CONTRACT_VERSION

MaskFamilySpec
MaskInstanceSpec
MaskSequenceSpec
GridSpec
ProjectionSpec
MaskIdentity
RenderedMask

render_continuous_mask
project_display_mask
render_display_mask
render_mask_instance
render_mask_sequence

canonicalize_spec
hash_mask_instance
hash_mask_sequence

load_mask_instance_spec
load_mask_sequence_spec
dump_mask_instance_spec
dump_mask_sequence_spec

list_families
get_family_metadata
```

## Minimal Usage

```python
from lcd_mask_families import load_mask_instance_spec, render_mask_instance

spec = load_mask_instance_spec("examples/stripes_instance.yaml")
rendered = render_mask_instance(spec, backend="numpy")

mask = rendered.mask
mask_hash = rendered.hash
```

## Active Families

The v0.1 active registry includes only implemented, documented, tested
families:

* `stripes`
* `radial_zones`
* `fourier_lowfreq`
* `blocks`
* `seeded_lowfreq_noise`

Planned families may be discussed in design documents, but they must not appear
in `list_families()` until they have a renderer, metadata, examples, and tests.

## Contract Files

Examples:

* `examples/stripes_instance.yaml`
* `examples/radial_zones_instance.yaml`
* `examples/fourier_lowfreq_instance.yaml`
* `examples/blocks_instance.yaml`
* `examples/seeded_lowfreq_noise_instance.yaml`
* `examples/simple_sequence.yaml`

Schemas:

* `schemas/mask_instance_spec.schema.json`
* `schemas/mask_sequence_spec.schema.json`
* `schemas/family_metadata.schema.json`

See `docs/optic_system_handshake.md` for the first downstream handoff contract.
