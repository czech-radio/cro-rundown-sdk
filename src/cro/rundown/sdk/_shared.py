# -*- coding: utf-8 -*-

"""
The sharred code e.g constants, configuration.
"""

__all__ = tuple(["success_msg", "failure_msg"])


success_msg = (
    lambda text=None: f"SUCCESS{'' if str(text) is None else ': ' + str(text)}"
)

failure_msg = (
    lambda text=None: f"FAILURE{'' if str(text) is None else ': ' + str(text)}"
)
