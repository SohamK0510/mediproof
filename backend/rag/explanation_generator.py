from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List


_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")
_SPACE_PATTERN = re.compile(r"\s+")

_PRIORITY_SOURCE_KEYS = ("who", "cdc", "nhs")


def _normalize_text(value: Any) -> str:
	if value is None:
		return ""
	text = str(value).strip()
	return _SPACE_PATTERN.sub(" ", text)


def _split_sentences(text: str) -> List[str]:
	normalized = _normalize_text(text)
	if not normalized:
		return []
	parts = _SENTENCE_SPLIT_PATTERN.split(normalized)
	return [part.strip() for part in parts if part and part.strip()]


def _pick_key_sentence(claim: str, content: str) -> str:
	sentences = _split_sentences(content)
	if not sentences:
		return ""

	claim_terms = {
		token for token in re.findall(r"[a-zA-Z]{4,}", claim.lower())
	}

	if not claim_terms:
		return sentences[0]

	best_sentence = sentences[0]
	best_score = -1

	for sentence in sentences:
		lowered = sentence.lower()
		overlap = sum(1 for term in claim_terms if term in lowered)
		score = overlap * 100 + min(len(sentence), 220)
		if score > best_score:
			best_score = score
			best_sentence = sentence

	return best_sentence


def _select_top_evidence(evidence: Iterable[Dict[str, Any]], max_items: int = 3) -> List[Dict[str, Any]]:
	items = [item for item in evidence if isinstance(item, dict)]
	if not items:
		return []

	ranked = sorted(items, key=lambda item: float(item.get("score", 0.0)), reverse=True)
	return ranked[: max(1, min(max_items, 3))]


def _format_sources(evidence_items: List[Dict[str, Any]]) -> str:
	sources: List[str] = []
	seen: set[str] = set()

	for item in evidence_items:
		source = _normalize_text(item.get("source", ""))
		if not source:
			continue
		key = source.lower()
		if key in seen:
			continue
		seen.add(key)
		sources.append(source)

	if not sources:
		return "reliable public health sources"

	prioritized: List[str] = []
	remaining = sources[:]
	for priority in _PRIORITY_SOURCE_KEYS:
		for src in sources:
			if priority in src.lower() and src in remaining:
				prioritized.append(src)
				remaining.remove(src)

	ordered = prioritized + remaining
	return ", ".join(ordered[:3])


def generate_explanation(claim: str, evidence: List[Dict[str, Any]]) -> str:
	"""
	Generate a short evidence-based medical explanation from retrieved RAG evidence.

	Args:
		claim: User health claim.
		evidence: Retrieved evidence documents, each containing content/source/url/score.

	Returns:
		Concise explanation string grounded in top evidence items.
	"""
	claim_text = _normalize_text(claim)
	top_items = _select_top_evidence(evidence, max_items=3)

	if not top_items:
		return (
			"Insufficient supporting evidence was retrieved for this claim. "
			"Please verify with trusted public health sources such as WHO, CDC, or NHS."
		)

	picked_sentences: List[str] = []
	seen_sentences: set[str] = set()

	for item in top_items:
		sentence = _pick_key_sentence(claim_text, _normalize_text(item.get("content", "")))
		if not sentence:
			continue
		normalized_sentence = sentence.lower()
		if normalized_sentence in seen_sentences:
			continue
		seen_sentences.add(normalized_sentence)
		picked_sentences.append(sentence)
		if len(picked_sentences) >= 3:
			break

	if not picked_sentences:
		return (
			"Relevant evidence was found, but key details could not be summarized. "
			"Please consult WHO, CDC, or NHS guidance for clinical recommendations."
		)

	summary_body = " ".join(picked_sentences[:3])
	sources_text = _format_sources(top_items)

	return f"{summary_body} According to {sources_text}, current guidance should be based on evidence-based medical recommendations."


__all__ = ["generate_explanation"]
