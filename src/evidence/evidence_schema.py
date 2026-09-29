from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EvidenceSource:
    """
    Represents a medical evidence source used by MedImpact AI.
    """

    title: str
    source_type: str
    organization: str
    url: str
    publication_date: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    identifier: Optional[str] = None


@dataclass
class EvidenceItem:
    """
    Represents a specific piece of evidence supporting or challenging
    a medical claim.
    """

    claim: str
    evidence_text: str
    source: EvidenceSource
    evidence_status: str
    confidence: str
    rationale: str = ""


@dataclass
class VerifiedClaim:
    """
    Represents the final evidence-verification result for a claim.
    """

    claim: str
    status: str
    confidence: str
    supporting_evidence: List[EvidenceItem] = field(
        default_factory=list
    )
    rationale: str = ""

