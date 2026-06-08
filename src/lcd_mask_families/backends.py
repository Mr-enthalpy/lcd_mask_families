from __future__ import annotations


def require_numpy_backend(backend: str) -> None:
    if backend != "numpy":
        raise ValueError(f"unsupported backend: {backend!r}")
