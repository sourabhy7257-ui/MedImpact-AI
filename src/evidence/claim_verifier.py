import re
from typing import Dict, List

from src.evidence.evidence_schema import (
    EvidenceItem,
    VerifiedClaim,
)
from src.evidence.claim_schema import MedicalClaim
from src.evidence.pubmed_evidence import PubMedEvidenceBuilder


STOP_WORDS = {
    "the", "a", "an", "and", "or", "of", "in", "to",
    "for", "with", "on", "is", "are", "was", "were",
    "among", "combined",
}


DIRECTION_TERMS = {
    "decrease": {
        "reduce",
        "reduced",
        "reduces",
        "reduction",
        "decrease",
        "decreased",
        "decreases",
        "lower",
        "lowered",
        "lowering",
        "improved",
        "improvement",
        "decline",
        "declined",
        "decrement",
    },
    "increase": {
        "increase",
        "increased",
        "increases",
        "higher",
        "elevated",
        "elevation",
        "raising",
        "raised",
        "gain",
    },
}


class ClaimVerifier:
    """
    First-stage deterministic medical claim verifier.

    Checks population, intervention, outcome, and direction
    using transparent terminology-based rules.

    This component does not establish causality, clinical
    efficacy, or medical safety.
    """

    def verify(
        self,
        claim: MedicalClaim,
        evidence_items: List[EvidenceItem],
    ) -> VerifiedClaim:

        if not claim.claim_text.strip():
            raise ValueError("claim_text must not be empty")

        if not evidence_items:
            return VerifiedClaim(
                claim=claim.claim_text,
                status="INSUFFICIENT",
                confidence="LOW",
                supporting_evidence=[],
                rationale="No evidence was retrieved.",
            )

        assessments = []
        supporting_evidence = []

        for item in evidence_items:

            text = (
                f"{item.source.title} "
                f"{item.evidence_text}"
            ).lower()

            population_match = self._component_match(
                claim.population,
                text,
            )

            intervention_match = self._component_match(
                claim.intervention,
                text,
            )

            outcome_match = self._component_match(
                claim.outcome,
                text,
            )

            direction_match = self._direction_match(
                claim.expected_direction,
                text,
            )

            assessment = {
                "pmid": item.source.identifier,
                "population": population_match,
                "intervention": intervention_match,
                "outcome": outcome_match,
                "direction": direction_match,
            }

            assessments.append(assessment)

            if (
                population_match == "MATCH"
                and intervention_match == "MATCH"
                and outcome_match == "MATCH"
                and direction_match == "SUPPORTS"
            ):
                supporting_evidence.append(item)

        overall_status = self._overall_status(assessments)

        if overall_status == "SUPPORTED":
            confidence = "LOW"
        elif overall_status == "CONTRADICTED":
            confidence = "LOW"
        elif overall_status == "PARTIAL":
            confidence = "LOW"
        else:
            confidence = "LOW"

        rationale = self._build_rationale(
            assessments,
            overall_status,
        )

        best_assessment = self._select_best_assessment(
            assessments
        )

        return VerifiedClaim(
            claim=claim.claim_text,
            status=overall_status,
            confidence=confidence,
            supporting_evidence=supporting_evidence,
            population_match=best_assessment["population"],
            intervention_match=best_assessment["intervention"],
            outcome_match=best_assessment["outcome"],
            direction_match=best_assessment["direction"],
            rationale=rationale,
        )

    @staticmethod
    def _normalize(text: str) -> List[str]:
        words = re.findall(r"[a-z0-9]+", text.lower())

        return [
            word
            for word in words
            if word not in STOP_WORDS and len(word) > 2
        ]

    def _component_match(
        self,
        claim_component: str,
        evidence_text: str,
    ) -> str:

        claim_terms = set(self._normalize(claim_component))
        evidence_terms = set(self._normalize(evidence_text))

        if not claim_terms:
            return "NO_MATCH"

        matched_terms = claim_terms.intersection(evidence_terms)

        overlap = len(matched_terms) / len(claim_terms)

        if overlap >= 0.75:
            return "MATCH"

        if overlap >= 0.40:
            return "PARTIAL"

        return "NO_MATCH"

    @staticmethod
    def _direction_match(
        expected_direction: str,
        evidence_text: str,
    ) -> str:

        if expected_direction not in DIRECTION_TERMS:
            return "UNCLEAR"

        positive_terms = DIRECTION_TERMS[expected_direction]

        opposite_direction = (
            "increase"
            if expected_direction == "decrease"
            else "decrease"
        )

        opposite_terms = DIRECTION_TERMS[opposite_direction]

        text = re.sub(r"\s+", " ", evidence_text.lower())

        negation_patterns = [
            r"\bno\s+(?:significant\s+)?{term}\b",
            r"\bnot\s+(?:significantly\s+)?{term}\b",
            r"\bdid\s+not\s+{term}\b",
            r"\bdidn't\s+{term}\b",
            r"\bfailed\s+to\s+{term}\b",
            r"\bwithout\s+(?:a\s+)?{term}\b",
        ]

        for term in positive_terms:
            for pattern in negation_patterns:
                if re.search(
                    pattern.format(term=re.escape(term)),
                    text,
                ):
                    return "CONTRADICTS"

        positive_matches = [
            term
            for term in positive_terms
            if re.search(
                rf"\b{re.escape(term)}\b",
                text,
            )
        ]

        if positive_matches:
            return "SUPPORTS"

        opposite_matches = [
            term
            for term in opposite_terms
            if re.search(
                rf"\b{re.escape(term)}\b",
                text,
            )
        ]

        if opposite_matches:
            return "CONTRADICTS"

        return "UNCLEAR"

    @staticmethod
    def _overall_status(
        assessments: List[Dict[str, str]],
    ) -> str:

        if not assessments:
            return "INSUFFICIENT"

        for assessment in assessments:
            if (
                assessment["population"] == "MATCH"
                and assessment["intervention"] == "MATCH"
                and assessment["outcome"] == "MATCH"
                and assessment["direction"] == "SUPPORTS"
            ):
                return "SUPPORTED"

        for assessment in assessments:
            if (
                assessment["population"] == "MATCH"
                and assessment["intervention"] == "MATCH"
                and assessment["outcome"] == "MATCH"
                and assessment["direction"] == "CONTRADICTS"
            ):
                return "CONTRADICTED"

        for assessment in assessments:
            matched_components = sum(
                value in {"MATCH", "PARTIAL"}
                for key, value in assessment.items()
                if key != "pmid"
            )

            if matched_components >= 2:
                return "PARTIAL"

        return "INSUFFICIENT"

    @staticmethod
    def _select_best_assessment(
        assessments: List[Dict[str, str]],
    ) -> Dict[str, str]:

        if not assessments:
            return {
                "population": "UNCLEAR",
                "intervention": "UNCLEAR",
                "outcome": "UNCLEAR",
                "direction": "UNCLEAR",
            }

        def score(assessment):
            weights = {
                "MATCH": 2,
                "PARTIAL": 1,
                "NO_MATCH": 0,
                "SUPPORTS": 2,
                "CONTRADICTS": 2,
                "UNCLEAR": 0,
            }

            return sum(
                weights.get(
                    value,
                    0,
                )
                for key, value in assessment.items()
                if key != "pmid"
            )

        return max(assessments, key=score)

    @staticmethod
    def _build_rationale(
        assessments: List[Dict[str, str]],
        overall_status: str,
    ) -> str:

        lines = [
            f"Overall evidence assessment: {overall_status}.",
        ]

        for assessment in assessments:
            lines.append(
                f"PMID {assessment['pmid']}: "
                f"population={assessment['population']}, "
                f"intervention={assessment['intervention']}, "
                f"outcome={assessment['outcome']}, "
                f"direction={assessment['direction']}"
            )

        lines.append(
            "This assessment uses deterministic terminology "
            "matching and does not establish causality, "
            "clinical efficacy, or evidence quality."
        )

        return "\n".join(lines)


def main():

    claim = MedicalClaim(
        claim_text=(
            "Low-carbohydrate diet combined with exercise "
            "reduces HbA1c in adults with type 2 diabetes."
        ),
        population="Adults with type 2 diabetes",
        intervention=(
            "Low-carbohydrate diet combined with exercise"
        ),
        outcome="HbA1c",
        expected_direction="decrease",
    )

    print("=" * 60)
    print("MedImpact AI - Claim Verifier")
    print("=" * 60)

    builder = PubMedEvidenceBuilder(max_results=5)

    evidence_items = builder.build_evidence(
        claim.claim_text
    )

    print(f"\nEvidence retrieved: {len(evidence_items)}")

    verifier = ClaimVerifier()

    result = verifier.verify(
        claim=claim,
        evidence_items=evidence_items,
    )

    print(f"\nClaim: {result.claim}")
    print(f"Status: {result.status}")
    print(f"Confidence: {result.confidence}")

    print("\nBest evidence assessment:")
    print(f"Population: {result.population_match}")
    print(f"Intervention: {result.intervention_match}")
    print(f"Outcome: {result.outcome_match}")
    print(f"Direction: {result.direction_match}")

    print(
        f"\nSupporting evidence: "
        f"{len(result.supporting_evidence)}"
    )

    print("\nRationale:")
    print(result.rationale)

    for item in result.supporting_evidence:
        print("\n" + "-" * 60)
        print(f"PMID: {item.source.identifier}")
        print(f"Title: {item.source.title}")
        print(f"URL: {item.source.url}")


if __name__ == "__main__":
    main()
