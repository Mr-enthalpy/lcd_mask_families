# Downstream Readiness

`lcd_mask_families` v0.2 is ready for downstream wrapper design, not downstream
adapter implementation inside this repository.

All downstream repositories should treat this package as a pure mask rendering
kernel and consume the same core API.

## optic_system Readiness

`optic_system` should treat `lcd_mask_families` as a mask rendering kernel, not
as a capture-plan parser.

Expected downstream responsibilities:

* wrap `MaskInstanceSpec` or equivalent JSON specs in its own capture-plan or
  service layer;
* render display masks through `render_display_mask`;
* record mask spec, rendered mask hash, projection metadata, and library
  version/provenance in measured artifacts;
* decide how rendered masks are displayed on physical LCD hardware.

`lcd_mask_families` must not know about:

* `LCDService`;
* RawCapture HDF5 files;
* `FullFramePSFSurvey`;
* camera or TLS hardware;
* measured PSF artifacts;
* capture task state.

## LCD_forward Readiness

`LCD_forward` should treat family specs as the physical or mathematical mask
identity behind measured PSF dictionaries and operator models.

Expected downstream responsibilities:

* wrap active families for differentiable use where appropriate;
* decide whether to use a future optional differentiable backend;
* decide how masks connect to peak-cluster or operator representations;
* evaluate H-matrix/operator behavior and losses outside this package;
* use seeded families for surrogate generalization, not ordinary continuous
  gradient coordinates.

`lcd_mask_families` must not know about:

* peak-cluster operators;
* H-matrix diagnostics;
* reconstruction or operator losses;
* surrogate training;
* optimizer state;
* measured PSF dictionaries beyond portable mask identity.

## reconstruction Readiness

`reconstruction` may consume mask identity, mask sequences, or differentiable
family maps where available.

Expected downstream responsibilities:

* consume optical operators from `LCD_forward` or another operator-producing
  layer;
* decide reconstruction objectives, solvers, and datasets;
* record mask identity when evaluating task-level experiments.

`reconstruction` should not ask `lcd_mask_families` to build optical operators.
This package must not know about reconstruction solvers, datasets, or
experiment-specific evaluation protocols.

## Boundary Summary

This package owns:

```text
family + parameters + grid + projection policy -> mask
```

Downstream repositories own:

```text
capture plans
LCD display services
PSF measurement
operator modelling
H-matrix diagnostics
reconstruction
optimization loops
```
