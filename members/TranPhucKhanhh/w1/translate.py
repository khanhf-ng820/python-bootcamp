"""Expose the instructor entrypoint without breaking merge.merge_sort."""

from .merge import merge_sort as merge_sorted

__all__ = ["merge_sorted"]
