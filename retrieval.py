"""
Numpy-based semantic retrieval over the SHL catalog.
Catalog embeddings are pre-computed (build_embeddings.py) and stored in catalog.json.
Query embedding uses fastembed (ONNX backend — no PyTorch required at runtime).
"""

import json
from pathlib import Path
from typing import Optional

import numpy as np

from models import CatalogItem

_CATALOG_PATH = Path(__file__).parent / "catalog.json"
_MODELS_DIR = Path(__file__).parent / "models"
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class CatalogRetriever:
    def __init__(self) -> None:
        self._items: list[CatalogItem] = []
        self._matrix: Optional[np.ndarray] = None  # shape (N, 384), L2-normalised
        self._embedder = None  # fastembed TextEmbedding

    def load(self, catalog_path: Path = _CATALOG_PATH) -> None:
        if not catalog_path.exists():
            raise FileNotFoundError(
                f"catalog.json not found at {catalog_path}. "
                "Run `python build_catalog.py && python build_embeddings.py` first."
            )

        with open(catalog_path, encoding="utf-8") as f:
            raw = json.load(f)

        embeddings = []
        items = []
        for entry in raw:
            emb = entry.pop("embedding", None)
            items.append(CatalogItem(**entry))
            if emb is not None:
                embeddings.append(emb)

        self._items = items
        if not self._items:
            raise ValueError("catalog.json is empty")

        if embeddings and len(embeddings) == len(items):
            self._matrix = np.array(embeddings, dtype=np.float32)
            print(f"Loaded {len(self._items)} items, embeddings shape={self._matrix.shape}")
        else:
            self._matrix = None
            print(f"Loaded {len(self._items)} items (no pre-computed embeddings)")

        # Load fastembed (ONNX-based, no PyTorch) — use bundled model if present
        try:
            from fastembed import TextEmbedding
            cache_dir = str(_MODELS_DIR) if _MODELS_DIR.exists() else None
            self._embedder = TextEmbedding(model_name=_MODEL_NAME, cache_dir=cache_dir)
            print("fastembed embedder loaded.")
        except Exception as exc:
            print(f"Warning: fastembed unavailable: {exc}. Falling back to keyword search.")

    def search(self, query: str, top_k: int = 20) -> list[CatalogItem]:
        if not self._items:
            raise RuntimeError("Retriever not loaded. Call load() first.")

        if self._matrix is not None and self._embedder is not None:
            q_vec = np.array(
                list(self._embedder.embed([query])), dtype=np.float32
            )[0]
            # Normalize query vector (fastembed may or may not normalize)
            norm = np.linalg.norm(q_vec)
            if norm > 0:
                q_vec /= norm
            scores = self._matrix @ q_vec  # cosine similarity
            top_indices = np.argsort(scores)[::-1][:top_k]
            return [self._items[i] for i in top_indices]

        # Fallback: BM25-style keyword overlap
        query_tokens = set(query.lower().split())
        scored = []
        for i, item in enumerate(self._items):
            text = (item.name + " " + item.description).lower()
            score = sum(text.count(w) for w in query_tokens)
            scored.append((score, i))
        scored.sort(reverse=True)
        return [self._items[i] for _, i in scored[:top_k]]

    def get_by_name(self, name: str) -> Optional[CatalogItem]:
        name_lower = name.lower()
        for item in self._items:
            if item.name.lower() == name_lower:
                return item
        for item in self._items:
            if name_lower in item.name.lower() or item.name.lower() in name_lower:
                return item
        return None

    def get_all(self) -> list[CatalogItem]:
        return self._items

    @property
    def is_loaded(self) -> bool:
        return bool(self._items)
