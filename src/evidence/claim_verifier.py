import re
from typing import Dict, List

from src.evidence.evidence_schema import (
    EvidenceItem,
    VerifiedClaim,
)
from src.evidence.claim_schema import MedicalClaim
from src.evidence.pubmed_evidence import PubMedEvidenceBuilder


STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "in",
    "to",
    "for",
    "with",
    "on",
    "is",
    "are",
    "was",
    "were",
    "among",
    "combined",
}


class ClaimVerifier:
    """
    First-stage deterministic claim verifier.

    Checks population, intervention, and outcome separately.
    It does not establish causality or clinical efficacy.
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

        relevant_evidence = []
        assessments = []

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

            assessment = {
                "pmid": item.source.identifier,
                "population": population_match,
                "intervention": intervention_match,
                "outcome": outcome_match,
            }

            assessments.append(assessment)

            if (
                population_match == "MATCH"
                and intervention_match == "MATCH"
                and outcome_match == "MATCH"
            ):
                relevant_evidence.append(item)

        if not relevant_evidence:
            rationale = self._build_rationale(assessments)

            return VerifiedClaim(
                claim=claim.claim_text,
                status="INSUFFICIENT",
                confidence="LOW",
                supporting_evidence=[],
                rationale=rationale,
            )

        rationale = (
            f"{len(relevant_evidence)} source(s) matched "
            "the population, intervention, and outcome. "
            "Direction of effect has not yet been verified."
        )

        return VerifiedClaim(
            claim=claim.claim_text,
            status="RELEVANT_EVIDENCE_FOUND",
            confidence="LOW",
            supporting_evidence=relevant_evidence,
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
    def _build_rationale(
        assessments: List[Dict[str, str]],
    ) -> str:

        lines = [
            "No retrieved source matched all required "
            "claim components."
        ]

        for assessment in assessments:
            lines.append(
                f"PMID {assessment['pmid']}: "
                f"population={assessment['population']}, "
                f"intervention={assessment['intervention']}, "
                f"outcome={assessment['outcome']}"
            )

        lines.append(
            "This assessment checks terminology overlap only "
            "and does not establish causality or clinical efficacy."
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
    print(
        f"Supporting evidence: "
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
