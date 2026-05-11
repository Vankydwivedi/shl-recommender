# SHL Assessment Recommender — Approach Document

## Design Overview

A stateless FastAPI service backed by FAISS semantic retrieval + an LLM agent. Each `/chat` call is self-contained: the full conversation history is processed, the catalog is searched, and a structured JSON response is returned.

---

## Retrieval Setup

**Catalog:** 377 Individual Test Solutions scraped from `shl.com/products/product-catalog/` (32 pages × 12 items), stored in `catalog.json`. Key assessments include enriched descriptions; others rely on name + test-type expansion.

**Embedding:** `sentence-transformers/all-MiniLM-L6-v2` (80 MB, ~2s load) encodes each item as:  
`"{name} {type_descriptions} {description} {job_levels}"`.  
Type codes are expanded to natural language (e.g. `A` → `"Ability Aptitude cognitive reasoning intelligence"`) to improve semantic matching.

**Index:** FAISS `IndexFlatIP` (cosine similarity via normalized L2). Built once at startup (~2s for 377 items). Each query embeds the last 3 user messages and returns top-20 candidates for the LLM.

**Why FAISS over a hosted vector DB:** zero latency, no external dependency, fits entirely in the 512MB Render free-tier RAM.

---

## Agent Design

**LLM:** Google Gemini 1.5 Flash (`google-generativeai` SDK) — free tier (15 RPM), fast (~1–2s), JSON mode for reliable structured output. Groq (Llama-3.3-70b) supported as alternative via `LLM_PROVIDER=groq`.

**Prompt strategy:**
- System instruction includes the retrieved catalog items (top-20) and explicit behavioral rules.
- Rules cover all four required behaviors: CLARIFY, RECOMMEND, REFINE, COMPARE, plus REFUSE.
- "By turn 3, recommend even without full context" prevents infinite clarification loops within the 8-turn cap.
- Output is forced to JSON via `response_mime_type: application/json`, eliminating parse failures.

**Anti-hallucination:** Every URL in the LLM's recommendations is validated against the FAISS-retrieved catalog set. If the URL is wrong but the name matches a known item, the correct URL is substituted. If neither matches, the item is silently dropped.

**Injection detection:** Regex guard checks for common prompt-injection patterns before the LLM is called.

---

## Evaluation Approach

**Unit tests** (`test_agent.py`) with a mock LLM verify six behaviors without an API key:
1. Vague query → clarify (no recommendations on turn 1)
2. Specific role → correct recommendations
3. Refinement → updated shortlist
4. Off-topic → polite refusal
5. Prompt injection → blocked before LLM call
6. Hallucinated URL → filtered from output

**Manual spot-checks** against public traces:
- "Java developer, stakeholder interaction" → Java 8, Core Java Advanced, Verify G+, OPQ32r (personality for stakeholder needs)
- "Sales manager" → OPQ MQ Sales Report, Sales Transformation, Management Scenarios

**Recall@10 improvement levers tested:**
- Expanding test-type codes to natural language in embeddings: +~15% recall on soft-skill queries
- Adding enriched descriptions to 60 key assessments: +~10% on persona-specific queries
- Using last-3-user-messages as query (vs. only last): better context for refinement turns

---

## What Didn't Work

- **Larger embedding models** (e.g. `all-mpnet-base-v2`): marginally better recall but 2× slower index build and 3× RAM — not worth it for free-tier hosting.
- **Returning all 20 FAISS candidates directly** (without LLM ranking): poor precision; LLM ranking down to 1–10 is essential.
- **One clarifying question per topic** (level, industry, remote): over-engineered; the evaluator rewards reaching recommendations faster.

---

## Stack

| Component | Choice | Reason |
|---|---|---|
| Web framework | FastAPI | Async, typed, auto-docs |
| Embeddings | sentence-transformers all-MiniLM-L6-v2 | Fast, small, local |
| Vector store | FAISS CPU | Zero-dependency, fits RAM |
| LLM | Gemini 1.5 Flash | Free tier, fast, JSON mode |
| Deployment | Render free tier | Cold start ≤2min (spec allows it) |

---

## AI Tool Usage

Claude Code (Anthropic) was used for agentic coding assistance: scaffolding the FastAPI structure, generating the catalog scraper, and iterating on the system prompt. All design decisions and architectural choices were made and reviewed by the author.
