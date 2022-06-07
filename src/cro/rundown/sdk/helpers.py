# -*- coding: utf-8 -*-


__all__ = tuple(["flatten"])


def flatten(lst: list) -> list:
    """Flatten the given list."""
    return [item for sublist in lst for item in sublist]
