# Implementation Plan

This plan stages the growth of `lcd_mask_families` while preserving its role as
a pure, deterministic mask-generation kernel library.

## Current Stage

v0.2 is complete.

Active v0.2 family set:

* `stripes`
* `blocks`
* `fourier_lowfreq`
* `radial_zones`
* `seeded_lowfreq_noise`

Current work is pre-integration stabilization:

* keep public API stable;
* keep metadata registry stable;
* keep JSON examples aligned with `MaskInstanceSpec`;
* keep tests deterministic and hardware-free;
* prepare documentation for downstream wrappers;
* avoid adding consumer-specific logic;
* avoid starting v0.3 family expansion.

This repository should not implement `optic_system` capture-plan adapters,
`LCD_forward` differentiable wrappers, reconstruction experiment interfaces,
PSF/H-matrix logic, or optimization loops.

## Completed v0.1

Initial core:

* `GridSpec`, `ProjectionSpec`, and `MaskInstanceSpec`;
* `render_continuous_mask`;
* `project_display_mask`;
* `render_display_mask`;
* `stripes`;
* `blocks`;
* active family metadata registry;
* NumPy backend;
* projection and quantization;
* deterministic spec and array hashing;
* hardware-free tests.

## Completed v0.2

v0.2 completed the first planned family expansion:

* `fourier_lowfreq`;
* `radial_zones`;
* `seeded_lowfreq_noise`;
* deterministic render tests for each active family;
* metadata tests for each active family;
* JSON examples for each active family.

v0.2 closure criteria:

* active metadata registry exists;
* `fourier_lowfreq` implemented;
* `radial_zones` implemented;
* `seeded_lowfreq_noise` implemented;
* all active families have deterministic render tests, metadata tests, and JSON
  examples.

## Pre-Integration Stabilization

The next phase is not v0.3 implementation. The next phase is to stabilize the
v0.2 API and documentation so that downstream repositories can consume the
library through their own adapter layers.

Stabilization work may include:

* tightening documentation around public API behavior;
* checking that JSON examples round-trip cleanly through `MaskInstanceSpec`;
* reviewing metadata wording so design intent is not mistaken for empirical
  optical validation;
* improving tests around deterministic identity and parameter validation;
* documenting downstream integration expectations without implementing
  downstream adapters.

Stabilization work must not add capture-plan parsing, LCD display integration,
PSF artifact handling, surrogate training, H-matrix diagnostics, reconstruction
code, or optimization loops.

## Future v0.3

v0.3 is planned, not current. It should not begin until the v0.2 API has been
used or reviewed by at least one downstream wrapper design.

Candidate v0.3 families:

* `multi_stripes`;
* `lattice_grating`;
* `zernike_amplitude`;
* `seeded_binary_noise`.

`zernike_amplitude` should remain amplitude or transmission oriented. Do not
rename it to a phase Zernike family unless the physical LCD model supports phase
modulation.

## Future v0.4 And Optional Work

Later candidate families:

* `chirped_stripes`;
* `hadamard_tiles` / `walsh_tiles`;
* `radial_basis`;
* `seeded_blue_noise`.

Optional backend work after the core remains stable:

* torch backend as an optional extra;
* differentiability parity tests;
* relaxed projection policies.

Torch must not become a required dependency. Differentiable projection policies
must remain separate from hard display projection and should not introduce
downstream optimization objectives into this package.

## Release Discipline

Each new active family should include:

* family metadata;
* deterministic rendering;
* parameter validation;
* JSON example if useful;
* tests for shape, bounds, determinism, and meaningful parameter changes;
* hash compatibility through `MaskInstanceSpec`.

Planned family names should not imply active API support. A family becomes active
only when it is registered, documented, and tested.
