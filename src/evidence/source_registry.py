from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SourceDefinition:
    """
    Defines a trusted medical evidence source.
    """

    name: str
    organization: str
    source_type: str
    authority_level: int
    description: str
    domains: List[str]


TRUSTED_SOURCES = [
    SourceDefinition(
        name="PubMed",
        organization="U.S. National Library of Medicine",
        source_type="peer_reviewed_research",
        authority_level=5,
        description=(
            "Biomedical literature database used to locate "
            "peer-reviewed research and clinical studies."
        ),
        domains=["pubmed.ncbi.nlm.nih.gov"],
    ),

    SourceDefinition(
        name="NIH",
        organization="National Institutes of Health",
        source_type="government_health_agency",
        authority_level=5,
        description=(
            "U.S. federal biomedical research and health information "
            "source."
        ),
        domains=["nih.gov"],
    ),

    SourceDefinition(
        name="CDC",
        organization="Centers for Disease Control and Prevention",
        source_type="government_health_agency",
        authority_level=5,
        description=(
            "U.S. public health agency providing evidence-based "
            "health information and guidance."
        ),
        domains=["cdc.gov"],
    ),

    SourceDefinition(
        name="FDA",
        organization="U.S. Food and Drug Administration",
        source_type="regulatory_agency",
        authority_level=5,
        description=(
            "U.S. regulatory agency providing information about "
            "medicines, medical devices, and safety."
        ),
        domains=["fda.gov"],
    ),

    SourceDefinition(
        name="WHO",
        organization="World Health Organization",
        source_type="international_health_organization",
        authority_level=5,
        description=(
            "International public health organization providing "
            "global health evidence and guidance."
        ),
        domains=["who.int"],
    ),

    SourceDefinition(
        name="Clinical Guidelines",
        organization="Recognized medical organizations",
        source_type="clinical_guideline",
        authority_level=5,
        description=(
            "Evidence-based clinical recommendations published by "
            "recognized professional medical organizations."
        ),
        domains=[],
    ),
]


def get_trusted_sources() -> List[SourceDefinition]:
    """
    Return all registered trusted sources.
    """

    return TRUSTED_SOURCES.copy()


def get_source_by_name(name: str) -> SourceDefinition:
    """
    Return a trusted source by name.
    """

    for source in TRUSTED_SOURCES:
        if source.name.lower() == name.lower():
            return source

    raise ValueError(
        f"Trusted source not found: {name}"
    )


if __name__ == "__main__":

    print("MedImpact AI - Trusted Source Registry")
    print("=" * 60)

    for source in TRUSTED_SOURCES:
        print(
            f"{source.name} | "
            f"{source.source_type} | "
            f"Authority: {source.authority_level}"
        )

    print("=" * 60)
    print(f"Registered sources: {len(TRUSTED_SOURCES)}")

