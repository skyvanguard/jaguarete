"""Base Vis protocol class.

Minimal stub retained for the agent action system which uses Vis as a
render protocol type hint.
"""

from typing import Any, Optional


class Vis:
    """Base visualization protocol.

    Subclasses can override ``display`` / ``sync_display`` to render
    action outputs in a UI-friendly format.
    """

    @classmethod
    def vis_tag(cls) -> str:
        """Return the vis tag identifier."""
        return cls.__name__

    async def display(self, content: Any = None, **kwargs) -> str:
        """Async display of content. Returns rendered string."""
        return str(content) if content is not None else ""

    def sync_display(self, content: Any = None, **kwargs) -> str:
        """Synchronous display of content. Returns rendered string."""
        return str(content) if content is not None else ""
