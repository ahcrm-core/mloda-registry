"""Per-owner stack of open invocations, so a nested hook can find its own enclosing call."""

from __future__ import annotations

import contextvars
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Generic, TypeVar

T = TypeVar("T")


class OpenInvocationStack(Generic[T]):
    """Open invocations per owner; instantiate at module scope only (a ContextVar created per call leaks)."""

    def __init__(self, name: str) -> None:
        self._stack: contextvars.ContextVar[tuple[tuple[int, T], ...]] = contextvars.ContextVar(name, default=())

    @contextmanager
    def open(self, owner: object, invocation: T) -> Iterator[None]:
        token = self._stack.set(self._stack.get() + ((id(owner), invocation),))
        try:
            yield
        finally:
            self._stack.reset(token)

    def find(self, owner: object) -> T | None:
        """The owner's newest open invocation, else None."""
        owner_id = id(owner)
        for key, invocation in reversed(self._stack.get()):
            if key == owner_id:
                return invocation
        return None
