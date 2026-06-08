# Current Stage

`lcd_mask_families` has completed its v0.2 family core.

The repository is currently in a pre-integration stabilization stage. The main
goal is to keep the pure-function mask generation core stable while downstream
repositories define their own wrappers.

## Active Family Set

* `stripes`
* `blocks`
* `fourier_lowfreq`
* `radial_zones`
* `seeded_lowfreq_noise`

## Current Priorities

* stabilize the public API and metadata registry;
* keep examples JSON-only and dependency-free;
* keep tests deterministic and hardware-free;
* document consumer boundaries;
* prepare downstream wrapper guidance without implementing those wrappers;
* avoid starting v0.3 family expansion until downstream wrapper needs are
  clearer.

## Non-Goals

* no capture-plan adapters;
* no LCD display services;
* no PSF dictionaries;
* no forward surrogate;
* no H-matrix diagnostics;
* no reconstruction code;
* no optimization loops;
* no torch dependency unless a future optional backend is explicitly planned.
