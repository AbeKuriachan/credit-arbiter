def test_metrics_requires_auth(client):
    response = client.get("/api/metrics")
    assert response.status_code == 401


def test_metrics_returns_zeroed_shape_with_no_assessments(client, auth_headers):
    response = client.get("/api/metrics", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["throughput"] == 0
    assert body["acceptance_rate"] is None
    assert body["cost_guardrail_usd"] == 0.08
    assert body["fairness_hard_block_pp"] == 5.0


def test_metrics_reflects_assessments_and_decisions(client, auth_headers, seeded_application):
    assess_response = client.post(
        "/api/assess", json={"application_id": seeded_application.id}, headers=auth_headers
    )
    assessment_id = assess_response.json()["id"]
    client.post(
        f"/api/assessments/{assessment_id}/decision",
        json={"action": "accept"},
        headers=auth_headers,
    )

    response = client.get("/api/metrics", headers=auth_headers)
    body = response.json()
    assert body["throughput"] == 1
    assert body["decided_count"] == 1
    assert body["acceptance_rate"] == 1.0
    assert body["override_rate"] == 0.0
