# optic_system Handshake

`lcd_mask_families` provides a pure mask-generation contract. An `optic_system`
capture plan may reference a mask instance spec or mask sequence spec, but this
repository does not parse capture plans and does not control hardware.

`optic_system` owns the adapter that:

* loads a mask instance or sequence spec;
* renders display masks through `lcd_mask_families`;
* sends the display mask array to its LCD service;
* records the mask hash, family metadata, grid, projection, and renderer
  version in downstream artifacts.

`lcd_mask_families` must not import `optic_system`, `LCDService`, camera SDKs,
TLS SDKs, PSF dictionaries, reconstruction code, or surrogate models.

Minimal conceptual use:

```python
from lcd_mask_families import load_mask_instance_spec, render_mask_instance

spec = load_mask_instance_spec("examples/stripes_instance.yaml")
rendered = render_mask_instance(spec, backend="numpy")

mask = rendered.mask
mask_hash = rendered.hash
```

For a sequence, downstream code should call `load_mask_sequence_spec()` and
`render_mask_sequence()`; the returned list preserves spec order.
