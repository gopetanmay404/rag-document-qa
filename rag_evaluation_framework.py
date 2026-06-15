"""
rag_evaluation_framework.py
───────────────────────────
Lightweight internal RAG evaluation using the existing Groq LLM.
No external services. No RAGAS. Runs from the Streamlit UI.

Evaluates recent Q&A interactions on 4 dimensions:
  - Retrieval Quality   : Are the retrieved chunks relevant to the question?
  - Context Coverage    : Does the context fully cover what's needed to answer?
  - Source Grounding    : Is the answer grounded in the retrieved sources?
  - Hallucination Risk  : Does the answer introduce facts not in the context?

Returns an Overall Health Score = weighted average of the 4 dimensions.
"""

import json
import re
from typing import List, Dict, Optional


# ──────────────────────────────────────────────────────────────────────────────
# EVALUATION PROMPT
# ──────────────────────────────────────────────────────────────────────────────

EVAL_PROMPT = """You are an expert RAG system evaluator. Evaluate the quality of the following RAG interaction.

QUESTION:
{question}

RETRIEVED CONTEXT:
{context}

GENERATED ANSWER:
{answer}

Score each dimension from 0 to 10 (integers only):

1. retrieval_quality: How relevant are the retrieved chunks to the question?
   - 0 = completely irrelevant chunks
   - 5 = partially relevant
   - 10 = all chunks are highly relevant

2. context_coverage: Does the retrieved context contain enough information to fully answer the question?
   - 0 = context has nothing useful
   - 5 = partial information available
   - 10 = context fully covers what is needed

3. source_grounding: Is the generated answer supported by the retrieved context?
   - 0 = answer contradicts or ignores the context
   - 5 = answer partially uses context
   - 10 = every claim in the answer is directly supported by context

4. hallucination_risk: Does the answer introduce facts NOT present in the context? (LOWER = BETTER)
   - 0 = no hallucination, fully grounded
   - 5 = some unsupported claims present
   - 10 = answer contains significant invented content

Respond ONLY with valid JSON in this exact format (no extra text, no markdown):
{{
  "retrieval_quality": <integer 0-10>,
  "context_coverage": <integer 0-10>,
  "source_grounding": <integer 0-10>,
  "hallucination_risk": <integer 0-10>,
  "reasoning": "<one sentence explaining the scores>"
}}"""


# ──────────────────────────────────────────────────────────────────────────────
# EVALUATOR CLASS
# ──────────────────────────────────────────────────────────────────────────────

class RAGEvaluator:
    """
    Lightweight RAG evaluator using an existing LangChain-compatible LLM.
    Uses a single structured LLM call per interaction for fast, cheap evaluation.
    """

    def __init__(self, llm):
        """
        Args:
            llm: Any LangChain-compatible LLM (e.g. ChatGroq instance).
        """
        self.llm = llm

    def evaluate_interaction(
        self,
        question: str,
        answer: str,
        retrieved_docs: list,
        sources: Optional[List[str]] = None
    ) -> Dict:
        """
        Evaluate a single RAG interaction.

        Args:
            question: The user's question.
            answer: The LLM-generated answer.
            retrieved_docs: List of LangChain Document objects from retrieval.
            sources: Optional list of source filenames (derived from docs if None).

        Returns:
            dict with keys:
                retrieval_quality (0-10)
                context_coverage  (0-10)
                source_grounding  (0-10)
                hallucination_risk (0-10, lower = better)
                overall_health     (0-100, weighted)
                faithfulness_score (0-100, alias for source_grounding*10)
                reasoning          (str)
                error              (str, only if evaluation failed)
        """
        # Build context string from retrieved docs (truncate to keep prompt manageable)
        context_parts = []
        for i, doc in enumerate(retrieved_docs[:6]):
            src = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "")
            page_str = f" | Page {page}" if page else ""
            content = doc.page_content[:500]  # Truncate per chunk
            context_parts.append(f"[Chunk {i+1} — {src}{page_str}]\n{content}")

        context_str = "\n\n".join(context_parts) if context_parts else "No context retrieved."
        answer_str = answer[:1000] if answer else "No answer generated."

        prompt = EVAL_PROMPT.format(
            question=question[:500],
            context=context_str,
            answer=answer_str
        )

        try:
            response = self.llm.invoke(prompt)
            raw = response.content.strip()

            # Parse JSON (handle markdown code blocks if LLM wraps it)
            raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("```").strip()
            scores = json.loads(raw)

            # Validate and clamp all scores to 0-10
            rq = max(0, min(10, int(scores.get("retrieval_quality", 5))))
            cc = max(0, min(10, int(scores.get("context_coverage", 5))))
            sg = max(0, min(10, int(scores.get("source_grounding", 5))))
            hr = max(0, min(10, int(scores.get("hallucination_risk", 5))))
            reasoning = str(scores.get("reasoning", "No reasoning provided."))

            # Keyword overlap faithfulness (non-LLM, bias-free)
            kw = keyword_overlap_score(answer_str, retrieved_docs)

            # Blended faithfulness: 60% LLM source_grounding + 40% keyword overlap
            blended_sg = round(sg * 0.6 + kw * 0.4, 1)

            # Overall health: weighted average (hallucination inverted)
            # Weights: retrieval 25%, coverage 25%, grounding 30%, hallucination 20%
            hallucination_inverted = 10 - hr
            overall_raw = (rq * 0.25 + cc * 0.25 + blended_sg * 0.30 + hallucination_inverted * 0.20)
            overall_health = round(overall_raw * 10)  # Scale to 0-100

            return {
                "retrieval_quality": rq,
                "context_coverage": cc,
                "source_grounding": sg,
                "hallucination_risk": hr,
                "keyword_faithfulness": round(kw * 10),   # 0-100 scale
                "faithfulness_score": round(blended_sg * 10),  # 0-100 blended
                "overall_health": overall_health,
                "reasoning": reasoning,
                "error": None
            }

        except json.JSONDecodeError as e:
            return _fallback_scores(f"JSON parse error: {str(e)}")
        except Exception as e:
            return _fallback_scores(f"Evaluation error: {str(e)}")

    def evaluate_batch(
        self,
        interactions: List[Dict]
    ) -> Dict:
        """
        Evaluate a batch of interactions and return aggregated scores.

        Args:
            interactions: List of dicts, each with:
                - question (str)
                - answer (str)
                - retrieved_docs (list of Document objects)

        Returns:
            dict with aggregated scores + list of per-interaction results.
        """
        if not interactions:
            return {
                "overall_health": 0,
                "retrieval_quality": 0,
                "context_coverage": 0,
                "source_grounding": 0,
                "hallucination_risk": 0,
                "faithfulness_score": 0,
                "count": 0,
                "results": [],
                "error": "No interactions to evaluate."
            }

        results = []
        for interaction in interactions:
            result = self.evaluate_interaction(
                question=interaction.get("question", ""),
                answer=interaction.get("answer", ""),
                retrieved_docs=interaction.get("retrieved_docs", []),
            )
            results.append(result)

        # Aggregate (ignore errored results)
        valid = [r for r in results if r.get("error") is None]

        if not valid:
            return {
                "overall_health": 0,
                "retrieval_quality": 0,
                "context_coverage": 0,
                "source_grounding": 0,
                "hallucination_risk": 0,
                "faithfulness_score": 0,
                "count": len(interactions),
                "results": results,
                "error": "All evaluations failed."
            }

        def avg(key):
            return round(sum(r[key] for r in valid) / len(valid), 1)

        return {
            "overall_health": round(sum(r["overall_health"] for r in valid) / len(valid)),
            "retrieval_quality": avg("retrieval_quality"),
            "context_coverage": avg("context_coverage"),
            "source_grounding": avg("source_grounding"),
            "hallucination_risk": avg("hallucination_risk"),
            "keyword_faithfulness": round(sum(r["keyword_faithfulness"] for r in valid) / len(valid)),
            "faithfulness_score": round(sum(r["faithfulness_score"] for r in valid) / len(valid)),
            "count": len(valid),
            "results": results,
            "error": None
        }


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def _fallback_scores(error_msg: str) -> Dict:
    """Return neutral fallback scores when evaluation fails."""
    return {
        "retrieval_quality": 5,
        "context_coverage": 5,
        "source_grounding": 5,
        "hallucination_risk": 5,
        "keyword_faithfulness": 50,
        "faithfulness_score": 50,
        "overall_health": 50,
        "reasoning": "Evaluation could not be completed.",
        "error": error_msg
    }


def keyword_overlap_score(answer: str, retrieved_docs: list) -> int:
    """
    Non-LLM faithfulness signal: measures what fraction of the answer's
    content words appear in the retrieved context.
    Returns 0–10 (10 = fully grounded in context).

    Rationale: LLM self-scoring is biased toward its own outputs. This
    provides an independent lexical grounding check. Blended 60/40 with
    the LLM score for a less biased faithfulness estimate.
    """
    stop = {"the", "a", "an", "is", "are", "was", "were", "in", "on",
            "at", "to", "for", "of", "and", "or", "not", "it", "this",
            "that", "be", "have", "has", "do", "does", "with", "by"}
    # Build context word set
    ctx_words: set = set()
    for doc in retrieved_docs:
        ctx_words.update(w.lower().strip(".,;:!?") for w in doc.page_content.split())
    # Extract content words from answer
    ans_words = {
        w.lower().strip(".,;:!?") for w in answer.split()
        if len(w) > 3 and w.lower() not in stop
    }
    if not ans_words:
        return 5  # Neutral when answer is too short to evaluate
    overlap = len(ans_words & ctx_words) / len(ans_words)
    return round(overlap * 10)


def score_to_label(score: float, invert: bool = False) -> str:
    """Convert a 0-10 score to a human-readable label."""
    if invert:
        score = 10 - score  # For hallucination risk (lower = better)
    if score >= 8:
        return "🟢 Excellent"
    elif score >= 6:
        return "🔵 Good"
    elif score >= 4:
        return "🟡 Moderate"
    else:
        return "🔴 Poor"


def health_to_label(health: int) -> str:
    """Convert overall health (0-100) to label."""
    if health >= 80:
        return "🟢 Healthy"
    elif health >= 60:
        return "🔵 Good"
    elif health >= 40:
        return "🟡 Needs Improvement"
    else:
        return "🔴 Critical"
