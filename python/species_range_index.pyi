"""Type stubs for the `species_range_index` PyO3 extension.

Read/write the `OGI1` H3-cell → `u32`-ID index. See the package README.
"""

import os

__version__: str

class SpeciesRangeIndex:
    """Read-only handle to an mmap'd `OGI1` cell → ID index."""

    @staticmethod
    def load(
        path: str | os.PathLike[str],
        expected_count: int | None = ...,
    ) -> SpeciesRangeIndex:
        """Load an index file via mmap.

        If `expected_count` is given it must equal the index's declared
        `count`, else `ValueError` is raised (stale-index guard). A
        bad/corrupt file also raises `ValueError`.
        """
        ...

    @staticmethod
    def write(
        path: str | os.PathLike[str],
        count: int,
        resolution: int,
        entries: dict[int, list[int]],
    ) -> None:
        """Build and write an `OGI1` index.

        `count` is the ID-space size (header `count`). `entries` maps each H3
        cell to the IDs in it; cells are sorted and IDs are sorted/deduplicated
        per cell. Raises `ValueError` on an invalid resolution or write error.
        """
        ...

    def ids_at(self, lat: float, lon: float) -> list[int]:
        """IDs for the H3 cell covering `(lat, lon)`; empty list if none."""
        ...

    @property
    def count(self) -> int:
        """Number of distinct IDs the index was built for (header `count`)."""
        ...

    @property
    def resolution(self) -> int:
        """H3 resolution the cells are indexed at."""
        ...

    @property
    def num_cells(self) -> int:
        """Number of distinct H3 cells in the index."""
        ...

    @property
    def num_entries(self) -> int:
        """Total number of `(cell, id)` entries."""
        ...

    def __repr__(self) -> str: ...
