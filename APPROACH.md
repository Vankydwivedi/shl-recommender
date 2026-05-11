# SHL Assessment Recommender — Approach Document

## Design Overview

A stateless FastAPI service backed by pre-computed semantic embeddings + an LLM agent. Each `/chat` call is self-contained: the full conversation history is processed, the catalog is searched, and a structured JSON response is returned. Stateless design means any number of concurrent conversations are supported without server-side session storage.

---

## Retrieval

**Catalog:** 377 Individual Test Solutions scraped from `shl.com/products/product-catalog/` (32 pages × 12 items), stored in `catalog.json`. Key assessments include enriched descriptions; others rely on name + test-type expansion.

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` (22 MB ONNX). Each item is encoded as:
`"{name} {type_descriptions} {description} {job_levels}"`.
Type codes are expanded to natural language (e.g. `A` → `"Ability Aptitude cognitive reasoning intelligence"`) to improve semantic matching for soft-skill queries that don't use SHL terminology.

**Offline pre-computation:** Embeddings for all 377 items are computed once locally (`build_embeddings.py`) and stored in `catalog.json`. At runtime, only numpy is needed to load the matrix — no model inference on the catalog.

**Query encoding:** `fastembed` (ONNX-based, no PyTorch) embeds only the query at runtime. The ONNX model is bundled in the repo (`models/`) so there is no download on startup.

**Similarity search:** Pure numpy matrix multiply (`catalog_matrix @ query_vec`) on L2-normalised vectors gives cosine similarity. Top-20 candidates are passed to the LLM. For 377 items this is faster than a vector DB with zero operational overhead.

**Why not FAISS or a hosted vector DB:** FAISS is unnecessary at this scale — numpy matrix multiply over 377×384 floats takes under 1ms. A hosted vector DB adds network latency and an external dependency. Pre-computing embeddings cuts cold-start memory from ~500 MB (PyTorch) to ~150 MB (onnxruntime), which fits the Render free tier.

---

## Agent Design

**LLM:** Groq `llama-3.3-70b-versatile` via REST API — low latency (~1–2s), free tier, `json_object` response mode for reliable structured output. Google Gemini 2.0 Flash supported as alternative via `LLM_PROVIDER=google`.

**Prompt strategy:**
- System instruction includes the retrieved top-20 catalog items and explicit behavioral rules.
- Rules cover all five required behaviors: CLARIFY, RECOMMEND, REFINE, COMPARE, REFUSE.
- The current **turn number** is injected into the prompt so the LLM knows when it must stop clarifying and recommend even with incomplete context.
- Output is forced to `json_object` mode, eliminating parse failures on structured fields.

**Anti-hallucination (post-LLM validation):**
Every URL in the LLM's response is validated against the retrieved catalog set. Three-stage recovery:
1. URL matches catalog exactly → accept.
2. URL wrong but name matches a catalog item → substitute correct URL.
3. Neither matches → silently drop with a log line.

**Injection detection (pre-LLM guard):** Regex checks for patterns like "ignore previous instructions", "act as", "you are now", etc. If triggered, the LLM is never called and a safe refusal is returned.

**EOC guard:** `end_of_conversation: true` is suppressed if the response contains no recommendations — prevents the agent from ending the conversation before delivering any value.

---

## Evaluation

**Unit tests** (`test_agent.py`) with a mock LLM verify eight behaviors without an API key. Each test has explicit `assert` statements that will raise on failure:

1. Vague query → clarify (zero recommendations, no EOC)
2. Specific role → recommendations with valid shl.com URLs
3. Refinement → updated shortlist includes requested type
4. Off-topic → polite refusal, zero recommendations
5. Prompt injection → LLM never called (verified by call counter)
6. Comparison → factual answer, zero recommendations
7. Hallucinated URL → filtered; valid catalog URL passes through
8. EOC without recommendations → suppressed

**Manual spot-checks:**
- "Java developer, stakeholder interaction" → Java 8, Core Java Advanced, Verify G+, OPQ32r
- "Sales manager" → OPQ MQ Sales Report, Sales Transformation, Management Scenarios
- "I need an assessment" (vague) → clarifying question, no recommendations

---

## What Didn't Work

- **Larger embedding models** (`all-mpnet-base-v2`): marginally better recall but 2× model size — not worth it given the catalog is only 377 items.
- **Returning all 20 candidates directly** (without LLM ranking): poor precision; LLM re-ranking to 1–10 is essential.
- **Multiple clarifying questions per turn**: over-engineered; the evaluator rewards reaching recommendations faster. One question per turn is sufficient.

---

## Stack

| Component | Choice | Reason |
|---|---|---|
| Web framework | FastAPI + Pydantic v2 | Async, typed, request validation |
| Embeddings (offline) | sentence-transformers all-MiniLM-L6-v2 | Compact, well-tested |
| Embeddings (runtime) | fastembed (ONNX) | No PyTorch, ~150 MB RAM |
| Similarity search | numpy cosine (matrix multiply) | <1ms for 377 items, zero deps |
| LLM | Groq llama-3.3-70b-versatile | Fast, free, JSON mode |
| Deployment | Render free tier (512 MB) | Public URL, auto-deploy from GitHub |

---

## AI Tool Usage

Claude Code (Anthropic) was used for agentic coding assistance: scaffolding the FastAPI structure, generating the catalog scraper, and iterating on the system prompt. All design decisions and architectural choices were made and reviewed by the author.
