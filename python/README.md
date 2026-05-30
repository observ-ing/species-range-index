# species-range-index (Python bindings)

PyO3 bindings for the [`species-range-index`](../) Rust crate — read the `OGI1`
H3-cell → `u32`-ID index from Python through the same Rust code the production
service uses.

## Why

The `OGI1` format would otherwise be parsed in multiple places: the Rust reader
plus hand-rolled Python parsers (`struct.unpack` + `np.frombuffer`) in the
`bioclip-models` pipeline. These bindings let the Python producer/verifier read
the format through the Rust reader, so verification exercises the real code path
and the read side has one source of truth.

## Build & use

```bash
pip install maturin
maturin develop -m python/Cargo.toml   # builds + installs into the active venv
```

```python
from species_range_index import SpeciesRangeIndex

# Write: `entries` maps each H3 cell -> the IDs in it. Cells are sorted and IDs
# are sorted/deduplicated per cell, so the mapping need not be pre-normalized.
SpeciesRangeIndex.write("species_geo_index.bin", num_labels, resolution, entries)

# Read
idx = SpeciesRangeIndex.load("species_geo_index.bin", expected_count=num_labels)
idx.count, idx.resolution, idx.num_cells, idx.num_entries
ids = idx.ids_at(37.77, -122.42)   # list[int]
```

A bad / stale / corrupt file raises `ValueError`.

Requires Python >= 3.11 (the wheel targets the `abi3-py311` stable ABI, so one
wheel works across all CPython 3.11+).

## Tests

```bash
maturin develop -m python/Cargo.toml
pytest python/tests/
```

## Packaging notes

- This crate is a **standalone (nested) cargo workspace** so it resolves
  independently of the root Rust crate; it's a PyO3 `extension-module` (doesn't
  link libpython), built with maturin rather than plain `cargo`.
- The dependency on the root crate is imported as `index_core` (renamed)
  because this crate's own library name **is** `species_range_index` (the Python
  module), which would otherwise collide.
- All deps (`h3o`/`memmap2`/`bytemuck`) are pure Rust, so wheels are
  self-contained — no C library to bundle.
