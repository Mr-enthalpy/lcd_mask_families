# Family Metadata Policy

Family metadata records the intended mathematical role of a mask family. It is
descriptive and operationally useful, but it is not a substitute for empirical
validation.

## Current Implementation

The first metadata registry covers active implemented families only:

```text
blocks
fourier_lowfreq
radial_zones
stripes
```

Planned family metadata remains documentation-only until the family is
implemented, registered, and tested.

## Minimal Shape

Every active family should expose a metadata object close to this shape:

```python
FAMILY_METADATA = FamilyMetadata(
    family_id="...",
    family_version="0.1.0",
    status="active",
    differentiable=True,
    continuous_parameters=True,
    seeded=False,
    diffraction_oriented=True,
    orthogonal_basis=False,
    recommended_for_capture=True,
    recommended_for_optimization=True,
    notes="...",
)
```

The exact representation may evolve, but the semantics should remain stable.

## Field Meanings

`family_id`: stable registry id used by `render_continuous_mask`.

`family_version`: semantic version for the family definition. Bump this when the
same parameters would produce materially different masks.

`status`: one of `active`, `planned`, or `experimental`.

`differentiable`: whether the mathematical family is intended to support a
continuous path under a differentiable backend.

`continuous_parameters`: whether ordinary parameter changes are continuous.
Seeds, pattern indices, tile indices, and ordering selectors are not continuous
optimization coordinates.

`seeded`: whether a seed is part of the family identity.

`diffraction_oriented`: whether the family is designed around grating, lattice,
radial, or related structures expected to produce interpretable diffraction
changes.

`orthogonal_basis`: whether the family is based on an orthogonal or
low-dimensional basis coordinate system.

`recommended_for_capture`: whether the family is intended to be useful for
repeatable acquisition diversity.

`recommended_for_optimization`: whether the family is intended to be an ordinary
gradient-optimization space. This should be false for seed changes and most
structured binary capture families.

`notes`: concise human-readable caveats.

## Validation Boundary

Metadata may label the intended mathematical role of a family. It must not claim
measured optical performance as fact.

Whether a family actually produces useful PSF diversity must be evaluated by
downstream systems:

```text
optic_system:
  physical measurements and capture metadata

LCD_forward:
  mask-to-operator surrogate diagnostics and H-matrix/operator evaluation

reconstruction:
  task-level reconstruction experiments
```

This library should not include PSF sensitivity claims as facts. Phrases such as
"diffraction-oriented" or "recommended_for_capture" describe design intent, not
validated experimental performance.

## Registry Policy

Every active family should expose metadata.

Planned families may be listed in documentation, but they must not appear in the
active family registry unless they are implemented and tested.

Experimental families should be clearly marked. They should not be silently
recommended for optimization or capture.

If a family is seeded, the seed is part of the deterministic input spec. Changing
the seed creates another deterministic mask instance; it is not a continuous
optimization step.

## Consumer Boundary

Metadata must remain independent of downstream repository internals. It may say
that a family is intended for capture or optimization, but it must not encode
capture-plan structure, LCD service details, PSF artifact paths, surrogate
checkpoint ids, reconstruction losses, or experiment-local filenames.
