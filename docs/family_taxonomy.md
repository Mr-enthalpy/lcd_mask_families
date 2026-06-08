# Mask Family Taxonomy

This document defines the intended mask-family taxonomy for
`lcd_mask_families`. It is normative documentation for future development, not a
claim that every listed family is already implemented.

The active implemented families are currently `blocks`, `fourier_lowfreq`,
`radial_zones`, and `stripes`.

## Design Motivation

Useful mask families should not be arbitrary image generators. They should be
low-dimensional, reproducible, and physically interpretable. A family should make
it possible to explain how a small parameter change moves through mask space and
why that movement might produce structured optical response changes.

For differentiable families, large changes in free variables should induce
structured changes in PSF or diffraction-peak distribution. They should not
primarily create high-frequency random-walk-like mask changes that make the
optical response return, stall, or become untrackable.

```text
good differentiable family:
  parameter changes control direction, period, phase, radial frequency,
  lattice geometry, or low-order basis coefficients;
  PSF changes form a structured trajectory in response space.

bad differentiable family:
  parameter changes mainly perturb local random high-frequency pixels;
  PSF changes resemble random walk in state space.
```

This repository does not measure or prove PSF sensitivity. It defines the pure
mask-generation map:

```text
family + parameters + grid + projection policy -> mask
```

Downstream systems measure, optimize, reconstruct, or evaluate the consequences
of those masks.

All consumers should use the same core functions:

```python
render_continuous_mask(...)
project_display_mask(...)
render_display_mask(...)
```

Do not design separate APIs for `optic_system`, `LCD_forward`, or
`reconstruction`. Each downstream repository wraps the same mathematical mask
map independently.

## Class 1: Diffraction-Oriented Differentiable Families

These are the primary future optimization families. They are designed to
interact with LCD diffraction structure and to change diffraction orders, peak
locations, peak strength, or peak-spread structure in a controlled way.

### `stripes`

Mathematical idea: a single periodic stripe grating over the coordinate grid.

Typical parameters: `angle_rad`, `period`, `phase_rad`, `duty`, and optional
`softness`.

Differentiability status: binary stripes are piecewise constant. The optional
soft relaxation is intended as a differentiable-oriented mathematical interface,
but its gradient shape and boundary behavior require dedicated downstream review
before optimization use.

Diffraction relevance: stripe direction and period are expected to control
dominant grating orientation and spacing.

Recommendation: active; recommended for capture and as an initial optimization
family, with softness-specific validation before serious differentiable use.

### `multi_stripes`

Mathematical idea: a low-cardinality sum or product of stripe components with
separate angles, periods, phases, and weights.

Typical parameters: component count, per-component angle, period, phase, duty,
weight, and combination mode.

Differentiability status: planned differentiable family if implemented with
continuous component weights and relaxed edges.

Diffraction relevance: multiple stripe components may produce multiple
structured diffraction directions or order groups.

Recommendation: planned; likely useful for both capture and optimization after
tests define deterministic composition and parameter bounds.

### `chirped_stripes`

Mathematical idea: stripe period varies smoothly across the mask, such as along
one axis or a radial coordinate.

Typical parameters: base period, chirp rate, direction, phase, duty, and
softness.

Differentiability status: planned differentiable family.

Diffraction relevance: a spatially varying period may spread or steer
diffraction orders in a structured way rather than producing a single fixed
grating frequency.

Recommendation: planned; promising for capture diversity and optimization, but
requires careful parameterization to avoid unstable high-frequency behavior.

### `lattice_grating`

Mathematical idea: a two-dimensional lattice generated from two or more basis
vectors, producing periodic dot, line, or cell structures.

Typical parameters: lattice basis vectors, periods, phase offsets, duty or fill
fraction, and optional edge softness.

Differentiability status: planned differentiable family if basis vectors and
fill parameters are continuous.

Diffraction relevance: lattice geometry can control two-dimensional diffraction
order placement and symmetry.

Recommendation: planned; likely useful for both capture and optimization after
metadata and parity tests are added.

### `radial_zones`

Mathematical idea: radial rings or zones whose values depend on distance from a
center point.

Typical parameters: center, radial period, phase, duty, radial scale, and
softness.

Differentiability status: active differentiable family. Hard zones are
piecewise constant; `softness > 0` provides a relaxed mathematical interface
that requires downstream differentiability review.

Diffraction relevance: radial structure may affect radial peak spread and
low-order circular diffraction features.

Recommendation: active; useful candidate for capture and optimization as design
intent, subject to downstream validation. This is not a claim of measured PSF
performance.

## Class 2: Orthogonal / Low-Dimensional Basis Families

These provide interpretable low-dimensional mask coordinates and baseline
optimization spaces. They may be less diffraction-specialized than stripe or
lattice families, but they are useful for systematic response-space exploration.

### `fourier_lowfreq`

Mathematical idea: a low-order Fourier basis over the grid with a bounded set of
spatial frequencies.

Typical parameters: sine and cosine coefficients for selected low-frequency
modes, optional bias, and output normalization policy.

Differentiability status: active differentiable family.

Diffraction relevance: low-frequency modes provide smooth, structured mask
changes and can probe broad optical response trends.

Recommendation: active; useful baseline for capture and optimization if
coefficient ranges and normalization are deterministic. This is not a claim of
measured optical performance.

### `zernike_amplitude`

Mathematical idea: amplitude or transmission-like masks parameterized by a small
set of Zernike basis coefficients over a pupil-like coordinate frame.

Typical parameters: selected Zernike mode coefficients, aperture radius, center,
and value normalization policy.

Differentiability status: planned differentiable family.

Diffraction relevance: low-order Zernike amplitude patterns may provide
interpretable pupil-shaped modulation.

Recommendation: planned; use the name `zernike_amplitude`. Do not call this a
phase Zernike family unless a future physical model explicitly supports phase
modulation. The current LCD mask output is a display/intensity/transmission-like
mask object, not a confirmed physical phase map.

### `radial_basis`

Mathematical idea: a small set of radial basis functions centered at fixed or
parameterized locations.

Typical parameters: basis weights, centers, radii, and normalization policy.

Differentiability status: planned differentiable family.

Diffraction relevance: smooth localized basis functions can create structured
but non-periodic mask changes for response-space exploration.

Recommendation: planned; useful for baseline optimization spaces and controlled
capture diversity.

## Class 3: Structured Non-Differentiable Capture Families

These support acquisition diversity and surrogate generalization, but are not
the main gradient optimization space. Some capture-useful families may not have
good differentiable forms.

### `blocks`

Mathematical idea: periodic rectangular block or checker patterns over the grid.

Typical parameters: `block_h`, `block_w`, `offset_y`, `offset_x`, and `invert`.

Differentiability status: active non-differentiable family.

Diffraction relevance: block structure can provide structured spatial diversity,
but parameter changes are discrete.

Recommendation: active; recommended for capture and generalization tests, not
ordinary gradient-based optimization.

### `binary_aperture_tiles`

Mathematical idea: a small tiled aperture pattern with binary open or closed
cells.

Typical parameters: tile size, tile pattern, offsets, and inversion.

Differentiability status: planned non-differentiable family.

Diffraction relevance: tiled aperture changes provide controlled acquisition
diversity with interpretable spatial support.

Recommendation: planned for capture, not gradient optimization.

### `hadamard_tiles`

Mathematical idea: tile masks generated from rows or columns of a Hadamard-like
binary pattern family.

Typical parameters: tile size, pattern index, ordering, offset, and inversion.

Differentiability status: planned non-differentiable family.

Diffraction relevance: orthogonal binary patterns can support systematic capture
diversity and surrogate training coverage.

Recommendation: planned for capture and generalization, not gradient
optimization.

### `walsh_tiles`

Mathematical idea: tiled binary masks derived from Walsh basis orderings.

Typical parameters: tile size, Walsh index, ordering, offset, and inversion.

Differentiability status: planned non-differentiable family.

Diffraction relevance: structured binary basis masks can provide repeatable
response-space probes.

Recommendation: planned for capture and generalization, not gradient
optimization.

## Class 4: Seeded Random / Pseudo-Random Families

These provide controlled diversity for forward-model generalization. They must
remain pure functions:

```text
seed + parameters + grid + projection -> mask
```

Seed changes are not continuous optimization variables. Seeded families may be
recommended for capture and generalization, but not for ordinary gradient-based
optimization.

### `seeded_binary_noise`

Mathematical idea: deterministic binary random masks generated from a seed and
fixed distribution parameters.

Typical parameters: seed, probability or fill fraction, optional tile size, and
inversion.

Differentiability status: planned non-differentiable seeded family.

Diffraction relevance: useful for broad capture diversity, not structured
gradient trajectories.

Recommendation: planned for capture and generalization, not optimization.

### `seeded_lowfreq_noise`

Mathematical idea: seeded random coefficients over a low-frequency basis,
producing smooth pseudo-random masks.

Typical parameters: seed, frequency cutoff, coefficient scale, bias, and
normalization policy.

Differentiability status: planned seeded family. Continuous parameters may exist,
but seed is not a continuous optimization variable.

Diffraction relevance: provides smoother random diversity than pixel noise and
may be useful for forward-model coverage.

Recommendation: planned for capture and generalization; ordinary gradient
optimization should operate on explicit continuous coefficients instead of seed
changes.

### `seeded_blue_noise`

Mathematical idea: deterministic blue-noise-like binary or grayscale patterns
generated from a seed and density parameters.

Typical parameters: seed, density, minimum-distance or spectrum-control
parameters, and optional tile size.

Differentiability status: planned non-differentiable seeded family.

Diffraction relevance: may provide high-spatial-diversity capture masks with
less low-frequency clustering than unstructured random noise.

Recommendation: planned for capture and generalization, not gradient
optimization.

## Active vs Planned Families

| family_id | status | differentiable | seeded | diffraction_oriented | orthogonal_basis | recommended_for_capture | recommended_for_optimization | implementation_priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `stripes` | active | yes | no | yes | no | yes | yes | v0.1 |
| `blocks` | active | no | no | no | no | yes | no | v0.1 |
| `multi_stripes` | planned | yes | no | yes | no | yes | yes | v0.3 |
| `chirped_stripes` | planned | yes | no | yes | no | yes | yes | v0.4 |
| `lattice_grating` | planned | yes | no | yes | no | yes | yes | v0.3 |
| `radial_zones` | active | yes | no | yes | no | yes | yes | v0.2 |
| `fourier_lowfreq` | active | yes | no | no | yes | yes | yes | v0.2 |
| `zernike_amplitude` | planned | yes | no | no | yes | yes | yes | v0.3 |
| `radial_basis` | planned | yes | no | no | yes | yes | yes | v0.4 |
| `binary_aperture_tiles` | planned | no | no | no | no | yes | no | v0.3+ |
| `hadamard_tiles` | planned | no | no | no | yes | yes | no | v0.4 |
| `walsh_tiles` | planned | no | no | no | yes | yes | no | v0.4 |
| `seeded_binary_noise` | planned | no | yes | no | no | yes | no | v0.3 |
| `seeded_lowfreq_noise` | planned | partial | yes | no | yes | yes | no | v0.2 |
| `seeded_blue_noise` | planned | no | yes | no | no | yes | no | v0.4 |

Planned families must not appear in the active registry until they are
implemented, documented, and tested.
