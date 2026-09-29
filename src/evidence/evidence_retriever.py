from dataclasses import dataclass
from typing import List

from src.evidence.source_registry import (
    SourceDefinition,
    get_trusted_sources,
)


@dataclass
class EvidenceCandidate:
    """
    Represents a potential evidence source returned by the retriever.
    """

    query: str
    source: SourceDefinition
    title: str
    url: str
    snippet: str


class EvidenceRetriever:
    """
    Initial evidence-retrieval interface for MedImpact AI.

    This version does not perform live web searches yet.
    It prepares structured candidates from the trusted-source registry.
    """

    def __init__(self):
        self.sources = get_trusted_sources()

    def get_available_sources(self) -> List[SourceDefinition]:
        """
        Return the currently configured trusted sources.
        """

        return self.sources.copy()

    def create_search_candidates(
        self,
        query: str
    ) -> List[EvidenceCandidate]:
        """
        Create structured search candidates for a medical query.

        Live retrieval will be connected in a later version.
        """

        if not query or not query.strip():
            raise ValueError(
                "Medical query cannot be empty."
            )

        query = query.strip()

        candidates = []

        for source in self.sources:

            candidates.append(
                EvidenceCandidate(
                    query=query,
                    source=source,
                    title=f"Search {source.name} for: {query}",
                    url=(
                        f"https://{source.domains[0]}"
                        if source.domains
                        else ""
                    ),
                    snippet=(
                        f"Evidence search candidate for '{query}' "
                        f"from {source.name}."
                    ),
                )
            )

        return candidates


def main():

    print("MedImpact AI - Evidence Retriever")
    print("=" * 60)

    query = "HbA1c diabetes management"

    retriever = EvidenceRetriever()

    candidates = retriever.create_search_candidates(query)

    print(f"Query: {query}")
    print(f"Sources configured: {len(candidates)}")
    print()

    for candidate in candidates:
        print(
            f"{candidate.source.name} | "
            f"{candidate.source.source_type}"
        )
        print(f"URL: {candidate.url}")
        print(f"Query: {candidate.query}")
        print()


if __name__ == "__main__":
    main()

