from src.api.services.retrieval import retrieve


def test_relevant_query_returns_expected_clause_with_source_id():
    result = retrieve("What is the maximum debt-to-income ratio for a personal loan?", scheme="Personal")
    assert result["retrieval_failed"] is False
    assert len(result["clauses"]) >= 1
    assert result["clauses"][0]["clause_id"] == "POL-PL-001"
    assert result["clauses"][0]["source_id"] == "POL-PL-001"
    assert result["clauses"][0]["scheme"] == "Personal"
    assert 0.0 < result["clauses"][0]["score"] <= 1.0


def test_unrelated_query_flags_retrieval_failed():
    result = retrieve("What is the weather forecast for tomorrow in outer space?")
    assert result["retrieval_failed"] is True
    assert result["clauses"] == []


def test_thin_file_query_matches_escalation_clause():
    result = retrieve("applicant has thin file short employment history bureau record")
    assert result["retrieval_failed"] is False
    assert result["clauses"][0]["clause_id"] == "POL-PL-004"


def test_scheme_filter_restricts_candidates_to_that_scheme():
    result = retrieve("what is the debt to income threshold", scheme="Education")
    assert result["retrieval_failed"] is False
    assert all(clause["scheme"] == "Education" for clause in result["clauses"])
    assert result["clauses"][0]["clause_id"] == "POL-ED-001"


def test_unknown_scheme_returns_retrieval_failed():
    result = retrieve("debt to income", scheme="Nonexistent Scheme")
    assert result["retrieval_failed"] is True
    assert result["clauses"] == []
