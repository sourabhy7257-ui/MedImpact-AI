from typing import List

from src.evidence.evidence_schema import (
    EvidenceItem,
    VerifiedClaim,
)

from src.evidence.pubmed_evidence import PubMedEvidenceBuilder


class ClaimVerifier:
    """
    First-stage deterministic claim verifier.

    This component identifies whether retrieved evidence is
    relevant to a claim. It does not establish medical causality
    or clinical efficacy.
    """

    def verify(
        self,
        claim: str,
        evidence_items: List[EvidenceItem],
    ) -> VerifiedClaim:

        if not claim or not claim.strip():
            raise ValueError("claim must not be empty")

        if not evidence_items:
            return VerifiedClaim(
                claim=claim,
                status="INSUFFICIENT",
                confidence="LOW",
                supporting_evidence=[],
                rationale="No evidence was retrieved.",
            )

        claim_terms = self._extract_terms(claim)
        relevant_evidence = []

        for item in evidence_items:
            evidence_text = (
                f"{item.source.title} "
                f"{item.evidence_text}"
            ).lower()

            matched_terms = [
                term
                for term in claim_terms
                if term in evidence_text
            ]

            if matched_terms:
                relevant_evidence.append(item)

        if not relevant_evidence:
            return VerifiedClaim(
                claim=claim,
                status="INSUFFICIENT",
                confidence="LOW",
                supporting_evidence=[],
                rationale=(
                    "Retrieved evidence did not contain "
                    "sufficient matching terminology."
                ),
            )

        return VerifiedClaim(
            claim=claim,
            status="RELEVANT_EVIDENCE_FOUND",
            confidence="LOW",
            supporting_evidence=relevant_evidence,
            rationale=(
                f"{len(relevant_evidence)} retrieved source(s) "
                "contained terminology relevant to the claim. "
                "This does not establish that the claim is "
                "causally or clinically supported."
            ),
        )

    @staticmethod
    def _extract_terms(claim: str) -> List[str]:
        stop_words = {
            "the", "a", "an", "and", "or", "of",
            "in", "to", "for", "with", "on", "is", "are",
        }

        terms = [
            word.strip(".,:;!?()[]{}").lower()
            for word in claim.split()
        ]

        return [
            term
            for term in terms
            if len(term) > 2 and term not in stop_words
        ]


def main():
    claim = "HbA1c diabetes management"

    print("=" * 60)
    print("MedImpact AI - Claim Verifier")
    print("=" * 60)

    builder = PubMedEvidenceBuilder(max_results=5)

    evidence_items = builder.build_evidence(claim)

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
    print(f"Rationale: {result.rationale}")

    for item in result.supporting_evidence:
        print("\n" + "-" * 60)
        print(f"PMID: {item.source.identifier}")
        print(f"Title: {item.source.title}")
        print(f"URL: {item.source.url}")


if __name__ == "__main__":
    main()
