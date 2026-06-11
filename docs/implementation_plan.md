# Implementation Plan

This plan keeps `lcd_mask_families` focused on a pure, deterministic mask
generation kernel.

## v0.1 Contract Stabilization

Current work freezes the first downstream handoff contract:

* explicit package exports;
* `MaskInstanceSpec` and `MaskSequenceSpec`;
* deterministic mask instance and sequence hashes;
* JSON/YAML loading and dumping;
* active family metadata;
* minimal examples and schemas;
* hardware-free tests.

This repository should not implement `optic_system` capture-plan adapters,
`LCD_forward` differentiable wrappers, reconstruction interfaces, PSF/H-matrix
logic, or optimization loops.

## Active Families

The active v0.1 registry is intentionally small:

* `stripes`
* `radial_zones`
* `fourier_lowfreq`
* `blocks`
* `seeded_lowfreq_noise`

## Future Work

Future families may be added only after the v0.1 contract has been integrated
or reviewed by downstream wrappers. A family becomes active only when it has:

* a renderer;
* metadata;
* examples;
* deterministic tests;
* documentation.

Optional backend work, such as torch support, must remain optional and must not
make torch a required dependency.
