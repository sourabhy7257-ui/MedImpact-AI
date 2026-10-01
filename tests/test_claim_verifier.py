from src.evidence.claim_verifier import ClaimVerifier


def test_decrease_positive():
    text = "The intervention reduced HbA1c significantly."
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "SUPPORTS"


def test_decrease_negative():
    text = "The intervention did not reduce HbA1c."
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "CONTRADICTS"


def test_no_reduction():
    text = "There was no reduction in HbA1c."
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "CONTRADICTS"


def test_increase_positive():
    text = "The intervention increased HbA1c."
    result = ClaimVerifier._direction_match("increase", text)
    assert result == "SUPPORTS"


def test_unclear():
    text = "The study evaluated HbA1c outcomes."
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "UNCLEAR"


def test_no_significant_reduction():
    text = "There was no significant reduction in HbA1c."
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "CONTRADICTS"


def test_negated_intervention_effect():
    text = (
        "The intervention did not reduce HbA1c, "
        "but the control group showed a reduction."
    )
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "CONTRADICTS"


def test_no_significant_reduction():
    text = "There was no significant reduction in HbA1c."
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "CONTRADICTS"


def test_negated_intervention_effect():
    text = (
        "The intervention did not reduce HbA1c, "
        "but the control group showed a reduction."
    )
    result = ClaimVerifier._direction_match("decrease", text)
    assert result == "CONTRADICTS"


def test_overall_status_supported():
    assessments = [
        {
            "pmid": "1",
            "population": "MATCH",
            "intervention": "MATCH",
            "outcome": "MATCH",
            "direction": "SUPPORTS",
        }
    ]

    result = ClaimVerifier._overall_status(assessments)

    assert result == "SUPPORTED"


def test_overall_status_contradicted():
    assessments = [
        {
            "pmid": "2",
            "population": "MATCH",
            "intervention": "MATCH",
            "outcome": "MATCH",
            "direction": "CONTRADICTS",
        }
    ]

    result = ClaimVerifier._overall_status(assessments)

    assert result == "CONTRADICTED"


def test_overall_status_partial():
    assessments = [
        {
            "pmid": "3",
            "population": "MATCH",
            "intervention": "PARTIAL",
            "outcome": "MATCH",
            "direction": "SUPPORTS",
        }
    ]

    result = ClaimVerifier._overall_status(assessments)

    assert result == "PARTIAL"


def test_overall_status_insufficient():
    assessments = [
        {
            "pmid": "4",
            "population": "NO_MATCH",
            "intervention": "NO_MATCH",
            "outcome": "NO_MATCH",
            "direction": "UNCLEAR",
        }
    ]

    result = ClaimVerifier._overall_status(assessments)

    assert result == "INSUFFICIENT"
