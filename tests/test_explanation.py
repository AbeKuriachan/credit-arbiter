from types import SimpleNamespace

from src.api.services import explanation as explanation_module
from src.api.services.explanation import generate_explanation

SAMPLE_EVIDENCE = {
    "risk_band": "Low",
    "risk_score": 0.12,
    "risk_factors": [{"label": "Average external credit bureau score", "impact": -0.5}],
    "loan_scheme": "Personal",
    "retrieved_clauses": [
        {"clause_id": "POL-PL-001", "title": "Debt-to-Income (DTI) Threshold", "text": "DTI must not exceed 50%."}
    ],
    "policy_failed_rules": [],
    "regulatory_status": "PASS",
    "thin_file_flag": False,
}


class _FakeMessage:
    def __init__(self, content):
        self.content = content


class _FakeChoice:
    def __init__(self, content):
        self.message = _FakeMessage(content)


class _FakeUsage:
    def __init__(self, prompt_tokens=40, completion_tokens=60):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class _FakeResponse:
    def __init__(self, content, usage=None):
        self.choices = [_FakeChoice(content)]
        self.usage = usage or _FakeUsage()


class _FakeCompletions:
    def __init__(self, content):
        self._content = content

    def create(self, **kwargs):
        return _FakeResponse(self._content)


class _FakeChat:
    def __init__(self, content):
        self.completions = _FakeCompletions(content)


class _FakeClient:
    def __init__(self, content):
        self.chat = _FakeChat(content)


def test_no_client_configured_uses_template(monkeypatch):
    monkeypatch.setattr(explanation_module, "_get_client", lambda: None)
    result = generate_explanation(SAMPLE_EVIDENCE, "Approve")
    assert result["source"] == "template"
    assert result["cost_usd"] == 0.0
    assert "Approve" in result["narrative"]


def test_grounded_citation_is_accepted(monkeypatch):
    fake = _FakeClient("Approved based on strong credit history per POL-PL-001.")
    monkeypatch.setattr(explanation_module, "_get_client", lambda: fake)
    result = generate_explanation(SAMPLE_EVIDENCE, "Approve")
    assert result["source"] == "llm"
    assert result["cost_usd"] > 0.0
    assert "POL-PL-001" in result["narrative"]


def test_ungrounded_citation_falls_back_to_template(monkeypatch):
    fake = _FakeClient("Approved per POL-XX-999, a clause that was never retrieved.")
    monkeypatch.setattr(explanation_module, "_get_client", lambda: fake)
    result = generate_explanation(SAMPLE_EVIDENCE, "Approve")
    assert result["source"] == "template"
    assert result["blocked_reason"] == "ungrounded_citation"


def test_cost_guardrail_skips_call_when_worst_case_exceeds_budget(monkeypatch):
    fake = _FakeClient("should never be called")
    monkeypatch.setattr(explanation_module, "_get_client", lambda: fake)
    monkeypatch.setattr(explanation_module, "COST_GUARDRAIL_USD", 0.0)  # force any estimate to breach
    result = generate_explanation(SAMPLE_EVIDENCE, "Approve")
    assert result["source"] == "template"
    assert result["blocked_reason"] == "cost_guardrail"


def test_llm_failure_falls_back_to_template(monkeypatch):
    class _BrokenClient:
        class chat:
            class completions:
                @staticmethod
                def create(**kwargs):
                    raise RuntimeError("network error")

    monkeypatch.setattr(explanation_module, "_get_client", lambda: _BrokenClient())
    result = generate_explanation(SAMPLE_EVIDENCE, "Refer")
    assert result["source"] == "template"
    assert result["blocked_reason"] == "llm_call_failed"
