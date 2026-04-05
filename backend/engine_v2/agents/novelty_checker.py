"""
AI_MathMate V2 — Novelty Checker (참신성 검증)
역할: BEq PASS된 문제가 기존 생성 문제 및 기출과 구조적·텍스트적으로 충분히 다른지 판별합니다.

[LLM 없음 - 순수 Python]
Judge와 동일하게 외부 API를 호출하지 않습니다.

[2계층 참신성 검증]
Layer 1 (구조적): 모듈 조합의 tags Jaccard 유사도 → 같은 수학 구조 반복 방지
Layer 2 (텍스트): 지문 TF-IDF cosine similarity → 같은 서술 반복 방지
"""

from __future__ import annotations
import math
import re
import sqlite3
from collections import Counter
from typing import Any

from engine_v2.config import DB


class NoveltyChecker:
    """
    생성된 문제의 참신성을 구조적·텍스트적으로 검증합니다.

    임계값:
        structural_threshold: 0.70 — 모듈 tags Jaccard ≥ 0.70이면 구조 중복
        textual_threshold:    0.60 — 지문 TF-IDF cosine ≥ 0.60이면 텍스트 중복
    """

    def __init__(
        self,
        db_path: str = DB["v2_path"],
        structural_threshold: float = 0.70,
        textual_threshold: float = 0.60,
    ):
        self.db_path = db_path
        self.structural_threshold = structural_threshold
        self.textual_threshold = textual_threshold

    def check(
        self,
        narrative: str,
        module_ids: list[str],
        module_tags: dict[str, list[str]],
        max_comparisons: int = 50,
    ) -> dict[str, Any]:
        """
        생성된 문제의 참신성을 검증합니다.

        :param narrative: BEq PASS된 지문
        :param module_ids: 사용된 모듈 ID 목록
        :param module_tags: {module_id: [tag1, tag2, ...]} 딕셔너리
        :param max_comparisons: 비교할 기존 문제 수 (최신순)
        :return: {
            "novel": bool,
            "structural_max_sim": float,  # 가장 유사한 기존 문제와의 구조 유사도
            "textual_max_sim": float,     # 가장 유사한 기존 문제와의 텍스트 유사도
            "most_similar_id": int | None,
            "reason": str,
        }
        """
        # 현재 문제의 태그 집합
        current_tags = set()
        for mid in module_ids:
            current_tags.update(module_tags.get(mid, []))

        # DB에서 기존 문제들 조회 (최신순)
        existing = self._fetch_existing(max_comparisons)
        if not existing:
            return {
                "novel": True,
                "structural_max_sim": 0.0,
                "textual_max_sim": 0.0,
                "most_similar_id": None,
                "reason": "비교 대상 없음 (첫 번째 문제)",
            }

        # ── Layer 1: 구조적 유사도 (Tags Jaccard) ──────────────────────
        structural_results = []
        for row in existing:
            ex_id, ex_narrative, ex_modules_json = row
            ex_tags = self._extract_tags_from_modules_json(ex_modules_json)
            sim = self._jaccard(current_tags, ex_tags)
            structural_results.append((ex_id, sim))

        # ── Layer 2: 텍스트 유사도 (TF-IDF Cosine) ────────────────────
        textual_results = []
        current_tokens = self._tokenize(narrative)
        current_tf = self._tf(current_tokens)

        # IDF 계산을 위해 전체 문서 수집
        all_docs = [self._tokenize(row[1]) for row in existing]
        idf = self._idf(all_docs + [current_tokens])
        current_tfidf = self._tfidf(current_tf, idf)

        for i, row in enumerate(existing):
            ex_id = row[0]
            ex_tf = self._tf(all_docs[i])
            ex_tfidf = self._tfidf(ex_tf, idf)
            sim = self._cosine(current_tfidf, ex_tfidf)
            textual_results.append((ex_id, sim))

        # ── 판정 ──────────────────────────────────────────────────────
        struct_max_id, struct_max_sim = max(structural_results, key=lambda x: x[1])
        text_max_id, text_max_sim = max(textual_results, key=lambda x: x[1])

        # 두 계층 중 하나라도 임계값 초과 시 중복 판정
        reasons = []
        if struct_max_sim >= self.structural_threshold:
            reasons.append(
                f"구조 중복: variant #{struct_max_id}과 Jaccard={struct_max_sim:.3f} (임계={self.structural_threshold})"
            )
        if text_max_sim >= self.textual_threshold:
            reasons.append(
                f"텍스트 중복: variant #{text_max_id}과 cosine={text_max_sim:.3f} (임계={self.textual_threshold})"
            )

        novel = len(reasons) == 0
        most_similar = text_max_id if text_max_sim > struct_max_sim else struct_max_id

        return {
            "novel": novel,
            "structural_max_sim": round(struct_max_sim, 4),
            "textual_max_sim": round(text_max_sim, 4),
            "most_similar_id": most_similar,
            "reason": " | ".join(reasons) if reasons else "참신한 문제",
        }

    # ── DB 조회 ───────────────────────────────────────────────────────

    def _fetch_existing(self, limit: int) -> list[tuple]:
        """기존 PASS된 문제들을 (id, narrative, variables_json) 튜플로 반환."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                rows = conn.execute("""
                    SELECT id, narrative, variables_json
                    FROM variants
                    WHERE status = 'VERIFIED'
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (limit,)).fetchall()
            return rows
        except Exception:
            return []

    def _extract_tags_from_modules_json(self, modules_json: str) -> set[str]:
        """variants.variables_json에서 태그 관련 키워드를 추출합니다."""
        import json
        try:
            data = json.loads(modules_json) if isinstance(modules_json, str) else modules_json
            # variables_json의 키 이름 자체가 수학적 구조를 반영
            keywords = set()
            for key in data.keys():
                # 언더스코어로 분리하여 각각 태그로
                keywords.update(key.lower().replace("-", "_").split("_"))
            # 숫자만 있는 토큰 제거
            return {k for k in keywords if k and not k.isdigit()}
        except Exception:
            return set()

    # ── Layer 1: Jaccard 유사도 ───────────────────────────────────────

    @staticmethod
    def _jaccard(set_a: set, set_b: set) -> float:
        if not set_a and not set_b:
            return 0.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    # ── Layer 2: TF-IDF Cosine Similarity ─────────────────────────────

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """텍스트를 소문자 토큰으로 분리. LaTeX, 숫자는 보존."""
        text = text.lower()
        # LaTeX 명령어를 토큰으로 보존 (\frac, \sqrt 등)
        tokens = re.findall(r'\\[a-z]+|[a-z]{2,}|\d+', text)
        # 불용어 제거 (수학 문맥에 불필요한 일반 단어)
        stopwords = {
            "the", "and", "that", "for", "are", "this", "with", "from",
            "has", "was", "were", "been", "have", "will", "each", "which",
            "their", "said", "its", "than", "other", "into", "can", "all",
        }
        return [t for t in tokens if t not in stopwords]

    @staticmethod
    def _tf(tokens: list[str]) -> dict[str, float]:
        """Term Frequency (정규화)."""
        counts = Counter(tokens)
        total = len(tokens) if tokens else 1
        return {term: count / total for term, count in counts.items()}

    @staticmethod
    def _idf(docs: list[list[str]]) -> dict[str, float]:
        """Inverse Document Frequency."""
        n_docs = len(docs)
        df = Counter()
        for doc in docs:
            unique_terms = set(doc)
            for term in unique_terms:
                df[term] += 1
        return {
            term: math.log((n_docs + 1) / (count + 1)) + 1
            for term, count in df.items()
        }

    @staticmethod
    def _tfidf(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float]:
        return {term: tf_val * idf.get(term, 1.0) for term, tf_val in tf.items()}

    @staticmethod
    def _cosine(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
        """두 sparse 벡터의 코사인 유사도."""
        all_terms = set(vec_a.keys()) | set(vec_b.keys())
        dot = sum(vec_a.get(t, 0) * vec_b.get(t, 0) for t in all_terms)
        mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)
