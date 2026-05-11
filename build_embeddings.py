"""
Pre-compute sentence embeddings for all catalog items and store them in catalog.json.
Run once locally: python build_embeddings.py
This eliminates the need for sentence-transformers + PyTorch at runtime.
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

CATALOG_PATH = Path(__file__).parent / "catalog.json"
MODEL_NAME = "all-MiniLM-L6-v2"


def to_search_text(item: dict) -> str:
    type_map = {
        "A": "Ability Aptitude Cognitive Reasoning",
        "B": "Biodata Situational Judgement",
        "C": "Competencies",
        "D": "Development 360 Feedback",
        "E": "Assessment Exercises Simulation",
        "K": "Knowledge Skills",
        "P": "Personality Behavior",
        "S": "Simulations",
    }
    type_words = " ".join(type_map.get(t, t) for t in item.get("test_types", []))
    return f"{item['name']} {type_words} {item.get('description', '')}".strip()


def main():
    with open(CATALOG_PATH, encoding="utf-8") as f:
        items = json.load(f)

    print(f"Loaded {len(items)} items. Building embeddings with {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    texts = [to_search_text(item) for item in items]
    embeddings = model.encode(
        texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True
    )
    embeddings = embeddings.astype(np.float32)

    for item, emb in zip(items, embeddings):
        item["embedding"] = emb.tolist()

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"Done. Embeddings shape: {embeddings.shape}")
    print(f"Updated {CATALOG_PATH}")


if __name__ == "__main__":
    main()
