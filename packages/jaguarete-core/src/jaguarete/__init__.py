"""Jaguarete: Next Generation Data Interaction Solution with LLMs."""

from jaguarete.component import BaseComponent, SystemApp  # noqa: F401

from ._version import version as __version__  # noqa: F401

_CORE_LIBS = ["core", "rag", "model", "agent", "storage", "util", "component"]
_LIBS = _CORE_LIBS

__ALL__ = ["__version__", "SystemApp", "BaseComponent"]


def __getattr__(name: str):
    # Lazy load
    import importlib

    if name in _LIBS:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
