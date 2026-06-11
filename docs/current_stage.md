# Current Stage

`lcd_mask_families` is stabilizing its v0.1 public mask-generation contract for
first downstream wrapping.

The current goal is not family expansion. The goal is to freeze the minimum API
and serialization contract that downstream repositories can reference without
this package depending on them.

## Active Family Set

* `stripes`
* `radial_zones`
* `fourier_lowfreq`
* `blocks`
* `seeded_lowfreq_noise`

## Current Priorities

* stabilize public exports;
* keep mask instance and sequence specs JSON/YAML serializable;
* keep hash identity deterministic within `CONTRACT_VERSION`;
* expose metadata for every active family;
* keep examples small and deterministic;
* document the `optic_system` handshake without implementing it.

## Non-Goals

* no capture-plan adapters;
* no LCD display services;
* no PSF dictionaries;
* no forward surrogate;
* no H-matrix diagnostics;
* no reconstruction code;
* no optimization loops;
* no hardware tests.
