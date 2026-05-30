# species-range-index

Zero-copy, mmap-backed index mapping [H3](https://h3geo.org) cells to sorted
`u32` ID lists, with O(log n) point lookup.

Given a latitude/longitude, `ids_at` returns the IDs associated with the H3
cell covering that point — a building block for any "what entities are relevant
at this location?" lookup. It is used by [observ-ing](https://github.com/observ-ing)
as a geographic prior over species ranges (lat/lon → candidate species IDs),
but the format is domain-agnostic (points of interest, region/coverage
membership, …).

## Usage

```rust,ignore
use species_range_index::SpeciesRangeIndex;

// `Some(n)` validates the file's declared count against `n` (catches a stale
// index whose IDs would point at the wrong rows); `None` skips that check.
let index = SpeciesRangeIndex::load(path, Some(num_labels))?;

for &id in index.ids_at(37.77, -122.42) {
    // ...
}
```

### Writing

`SpeciesRangeIndex::write` is the canonical writer for the format — cells are
sorted, IDs are sorted/deduplicated per cell, and duplicate cells are merged, so
the input need not be pre-normalized:

```rust,ignore
// `entries`: each H3 cell -> the IDs that fall in it.
SpeciesRangeIndex::write(path, num_labels as u32, resolution, entries)?;
```

## On-disk format

A compact `OGI1` binary (32-byte header + CSR `cells`/`offsets`/`ids` arrays),
documented in the crate root docs. The file is mmap'd, so only the pages
touched by a lookup are paged in — a multi-hundred-MB index costs a handful of
resident pages per query. Little-endian targets only (the slices are
reinterpreted zero-copy).

The format is typically produced by an offline build pipeline. This crate
provides both sides: `write` to produce an index and `load`/`ids_at` to read it.

## Python bindings

[`python/`](python/) provides PyO3 bindings (`pip install maturin && maturin
develop -m python/Cargo.toml`) so a Python producer/verifier can read the same
`OGI1` files through this Rust reader instead of a parallel hand-rolled parser.
See [python/README.md](python/README.md).
