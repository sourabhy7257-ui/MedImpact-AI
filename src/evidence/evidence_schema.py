from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EvidenceSource:
    title: str
    source_type: str
    organization: str
    url: str
    publication_date: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    identifier: Optional[str] = None


@dataclass
class EvidenceItem:
    claim: str
    evidence_text: str
    source: EvidenceSource
    evidence_status: str
    confidence: str
    rationale: str = ""


@dataclass
class VerifiedClaim:
    claim: str
    status: str
    confidence: str
    supporting_evidence: List[EvidenceItem] = field(
        default_factory=list
    )

    population_match: str = "UNCLEAR"
    intervention_match: str = "UNCLEAR"
    outcome_match: str = "UNCLEAR"
    direction_match: str = "UNCLEAR"

    rationale: str = ""
