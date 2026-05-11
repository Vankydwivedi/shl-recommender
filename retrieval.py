"""
FAISS-based semantic retrieval over the SHL catalog.
Loaded once at application startup; queries are fast (~5ms).
"""

import json
from pathlib import Path
from typing import Optional

import numpy as np

from models import CatalogItem

_CATALOG_PATH = Path(__file__).parent / "catalog.json"


class CatalogRetriever:
    def __init__(self) -> None:
        self._items: list[CatalogItem] = []
        self._index = None  # faiss.Index
        self._embedder = None  # SentenceTransformer

    def load(self, catalog_path: Path = _CATALOG_PATH) -> None:
        import faiss
        from sentence_transformers import SentenceTransformer

        if not catalog_path.exists():
            raise FileNotFoundError(
                f"catalog.json not found at {catalog_path}. "
                "Run `python scraper.py` first."
            )

        with open(catalog_path, encoding="utf-8") as f:
            raw = json.load(f)

        self._items = [CatalogItem(**item) for item in raw]
        if not self._items:
            raise ValueError("catalog.json is empty")

        print(f"Loaded {len(self._items)} catalog items")

        self._embedder = SentenceTransformer("all-MiniLM-L6-v2")
        texts = [item.to_search_text() for item in self._items]

        print("Building FAISS index...")
        embeddings = self._embedder.encode(
            texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True
        )
        embeddings = embeddings.astype(np.float32)

        dim = embeddings.shape[1]
        self._index = faiss.IndexFlatIP(dim)  # inner product = cosine on normalized vecs
        self._index.add(embeddings)
        print(f"FAISS index built: {self._index.ntotal} vectors, dim={dim}")

    def search(self, query: str, top_k: int = 20) -> list[CatalogItem]:
        if self._index is None or self._embedder is None:
            raise RuntimeError("Retriever not loaded. Call load() first.")

        q_vec = self._embedder.encode(
            [query], normalize_embeddings=True
        ).astype(np.float32)

        scores, indices = self._index.search(q_vec, min(top_k, len(self._items)))
        results = []
        for idx in indices[0]:
            if idx >= 0:
                results.append(self._items[idx])
        return results

    def get_by_name(self, name: str) -> Optional[CatalogItem]:
        name_lower = name.lower()
        for item in self._items:
            if item.name.lower() == name_lower:
                return item
        # Fuzzy: check if name is a substring
        for item in self._items:
            if name_lower in item.name.lower() or item.name.lower() in name_lower:
                return item
        return None

    def get_all(self) -> list[CatalogItem]:
        return self._items

    @property
    def is_loaded(self) -> bool:
        return self._index is not None
