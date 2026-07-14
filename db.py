"""Neon (serverless Postgres) persistence layer.

The application was originally built around plain in-memory dicts in
``data_store.py``. Every blueprint reads and writes those dicts directly
(``ds.patients[id]``, ``.values()``, ``.get()``, ``del``, ``in``, ``len()``)
and frequently mutates records *in place* without reassigning them back into
the store, e.g.::

    agent = ds.ai_agents.get(agent_id)
    agent["status"] = "deployed"        # no ds.ai_agents[id] = agent afterwards

To add durable storage without touching any blueprint, this module provides a
drop-in replacement for those dicts: :class:`PersistentStore` behaves exactly
like a ``dict`` keyed by integer id, but every record it hands out is a
:class:`PersistentRecord` that transparently writes itself back to Neon on any
mutation. Each store maps to one table with an ``id`` primary key and a
``JSONB`` ``data`` column holding the record.

Persistence is enabled only when ``DATABASE_URL`` is set (point it at your Neon
connection string). When it is unset the app falls back to the original
in-memory behaviour, so local demos and tests need no database.
"""
from __future__ import annotations

import json
import os
from typing import Iterator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def _normalize_url(url: str) -> str:
    """Return a SQLAlchemy-friendly Postgres URL using the psycopg (v3) driver.

    Neon hands out connection strings that start with ``postgres://`` or
    ``postgresql://``. SQLAlchemy needs an explicit driver, and we ship
    ``psycopg`` (v3), so normalise to ``postgresql+psycopg://``.
    """
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://") and "+psycopg" not in url:
        url = "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


def make_engine(database_url: Optional[str] = None) -> Optional[Engine]:
    """Create the Neon engine, or return ``None`` if no ``DATABASE_URL`` is set."""
    database_url = database_url or os.environ.get("DATABASE_URL")
    if not database_url:
        return None
    # pool_pre_ping guards against Neon closing idle serverless connections.
    return create_engine(
        _normalize_url(database_url),
        pool_pre_ping=True,
        future=True,
    )


class PersistentRecord(dict):
    """A record dict that writes itself back to Neon whenever it is mutated.

    Blueprints mutate records in place without reassigning them to the store,
    so we intercept the mutating ``dict`` operations and flush the row.
    """

    __slots__ = ("_store",)

    def __init__(self, store: "PersistentStore", *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "_store", store)

    def _flush(self) -> None:
        store = object.__getattribute__(self, "_store")
        rid = self.get("id")
        if store is not None and rid is not None:
            store._persist(rid, self)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._flush()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._flush()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._flush()

    def setdefault(self, key, default=None):
        had = key in self
        result = super().setdefault(key, default)
        if not had:
            self._flush()
        return result

    def pop(self, key, *args):
        had = key in self
        result = super().pop(key, *args)
        if had:
            self._flush()
        return result


class PersistentStore:
    """Dict-like store backed by a Neon table (``id`` PK + ``JSONB`` payload).

    Implements the subset of the ``dict`` protocol the app relies on:
    ``store[id]``, ``store[id] = record``, ``del store[id]``, ``id in store``,
    ``len(store)``, ``.get()``, ``.values()``, ``.items()``, ``.keys()`` and
    iteration. Reads are served from an in-memory cache that is hydrated from
    the table on startup; writes go through to Postgres immediately.
    """

    def __init__(self, engine: Engine, table: str):
        self._engine = engine
        self._table = table
        self._cache: dict[int, PersistentRecord] = {}
        self._ensure_table()
        self._load()

    def _ensure_table(self) -> None:
        with self._engine.begin() as conn:
            conn.execute(text(
                f'CREATE TABLE IF NOT EXISTS "{self._table}" ('
                "id BIGINT PRIMARY KEY, "
                "data JSONB NOT NULL)"
            ))

    def _load(self) -> None:
        with self._engine.begin() as conn:
            rows = conn.execute(text(
                f'SELECT id, data FROM "{self._table}"'
            )).all()
        for rid, data in rows:
            if isinstance(data, str):
                data = json.loads(data)
            self._cache[rid] = PersistentRecord(self, data)

    def _persist(self, rid: int, data: dict) -> None:
        payload = json.dumps({k: v for k, v in data.items()})
        with self._engine.begin() as conn:
            conn.execute(
                text(
                    f'INSERT INTO "{self._table}" (id, data) VALUES (:id, CAST(:data AS JSONB)) '
                    "ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data"
                ),
                {"id": rid, "data": payload},
            )

    # --- dict protocol -------------------------------------------------
    def __getitem__(self, rid: int) -> PersistentRecord:
        return self._cache[rid]

    def __setitem__(self, rid: int, record: dict) -> None:
        rec = record if isinstance(record, PersistentRecord) else PersistentRecord(self, record)
        object.__setattr__(rec, "_store", self)
        self._cache[rid] = rec
        self._persist(rid, rec)

    def __delitem__(self, rid: int) -> None:
        del self._cache[rid]
        with self._engine.begin() as conn:
            conn.execute(
                text(f'DELETE FROM "{self._table}" WHERE id = :id'),
                {"id": rid},
            )

    def __contains__(self, rid: object) -> bool:
        return rid in self._cache

    def __len__(self) -> int:
        return len(self._cache)

    def __iter__(self) -> Iterator[int]:
        return iter(self._cache)

    def get(self, rid: int, default=None):
        return self._cache.get(rid, default)

    def keys(self):
        return self._cache.keys()

    def values(self):
        return self._cache.values()

    def items(self):
        return self._cache.items()

    def max_id(self) -> Optional[int]:
        """Highest id currently stored, or ``None`` when empty (for id counters)."""
        return max(self._cache.keys()) if self._cache else None
