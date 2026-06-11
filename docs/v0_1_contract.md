# v0.1 Contract

This document defines the v0.1 handoff contract for `lcd_mask_families`.

The package is a pure deterministic mask-generation kernel:

```text
family + parameters + grid + projection policy -> mask
```

It is not an experiment framework and does not own downstream capture,
forward-model, reconstruction, or optimization workflows.

## Stable Public API

Downstream consumers should use the top-level package exports documented in
`README.md`.

The rendering API is consumer-neutral. Do not add separate public APIs for
`optic_system`, `LCD_forward`, or `reconstruction`.

## Stable Behavior

The following behavior should remain stable within `CONTRACT_VERSION`:

* same mask instance spec gives the same mask instance hash;
* same sequence spec gives the same sequence hash;
* same family, parameters, grid, and projection policy gives the same rendered
  display mask;
* continuous masks are finite and clipped into `[0, 1]`;
* projection is explicitly separate from continuous rendering;
* display projection supports `uint8` and `float32`;
* NumPy is the required backend;
* no external repository dependency is allowed;
* active family metadata is available for all active families;
* YAML examples round-trip through `MaskInstanceSpec` or `MaskSequenceSpec`.

Hash identity must not depend on local filenames, capture-plan filenames,
timestamps, machine paths, or external repository paths.

## Non-Contract Behavior

The following are not promised by v0.1:

* no torch backend;
* no downstream adapter stability;
* no physical LCD display packing;
* no PSF response guarantee;
* no measured optical performance claim;
* no capture-plan parsing;
* no reconstruction or optimization interface.
