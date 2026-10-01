from dataclasses import dataclass


@dataclass
class MedicalClaim:
    claim_text: str
    population: str
    intervention: str
    outcome: str
    expected_direction: str

