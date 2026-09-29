from typing import List

from src.evidence.evidence_schema import (
    EvidenceItem,
    EvidenceSource,
)
from src.evidence.pubmed_retriever import PubMedRetriever


class PubMedEvidenceBuilder:
    """Convert PubMed records into MedImpact AI evidence objects."""

    def __init__(self, max_results: int = 5):
        self.retriever = PubMedRetriever(max_results=max_results)

    def build_evidence(
        self,
        query: str,
    ) -> List[EvidenceItem]:

        records = self.retriever.search_and_fetch(query)

        evidence_items = []

        for record in records:
            abstract = record.get("abstract", "")

            if not abstract:
                continue

            source = EvidenceSource(
                title=record["title"],
                source_type="peer_reviewed_research",
                organization="PubMed / NCBI",
                url=record["url"],
                publication_date=record["publication_date"],
                authors=record["authors"],
                identifier=record["pmid"],
            )

            evidence_item = EvidenceItem(
                claim=query,
                evidence_text=abstract,
                source=source,
                evidence_status="retrieved",
                confidence="unassessed",
                rationale=(
                    "PubMed record retrieved successfully. "
                    "Claim support has not yet been verified."
                ),
            )

            evidence_items.append(evidence_item)

        return evidence_items


def main():
    query = "HbA1c diabetes management"

    builder = PubMedEvidenceBuilder(max_results=5)

    evidence = builder.build_evidence(query)

    print("=" * 60)
    print("MedImpact AI - PubMed Evidence Builder")
    print("=" * 60)

    print(f"\nQuery: {query}")
    print(f"Evidence items created: {len(evidence)}")

    for item in evidence:
        print("\n" + "-" * 60)

        print(f"Claim: {item.claim}")
        print(f"PMID: {item.source.identifier}")
        print(f"Title: {item.source.title}")
        print(f"Status: {item.evidence_status}")
        print(f"Confidence: {item.confidence}")
        print(f"URL: {item.source.url}")


if __name__ == "__main__":
    main()
