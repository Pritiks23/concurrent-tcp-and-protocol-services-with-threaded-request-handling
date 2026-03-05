from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_ai_eval_endpoint() -> None:
    response = client.post(
        '/api/ai/evaluate',
        json={
            'prompt': 'Explain UDP',
            'model_output': 'UDP is connectionless and low-latency',
            'expected_keywords': ['connectionless', 'low-latency'],
            'latency_ms': 120,
            'contains_sensitive_data': False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert 'correctness_score' in body
    assert 'summary' in body
