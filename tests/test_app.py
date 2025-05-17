import pytest
from flask import url_for

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"RAG on SageMaker" in response.data

def test_query_endpoint(client, mock_mongo, mock_embedding_model, mock_llm):
    """Test the query endpoint."""
    test_query = {
        "query": "What is RAG?",
        "context": "RAG stands for Retrieval Augmented Generation."
    }
    
    response = client.post('/query', json=test_query)
    assert response.status_code == 200
    assert response.is_json
    assert "answer" in response.json

def test_invalid_query(client):
    """Test the query endpoint with invalid data."""
    response = client.post('/query', json={})
    assert response.status_code == 400
    
    response = client.post('/query', json={"query": ""})
    assert response.status_code == 400

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

@pytest.mark.parametrize("test_input,expected", [
    ({"query": "test", "k": 2}, 200),
    ({"query": "test", "k": -1}, 400),
    ({"query": "", "k": 2}, 400),
])
def test_search_endpoint(client, test_input, expected):
    """Test the search endpoint with various inputs."""
    response = client.post('/search', json=test_input)
    assert response.status_code == expected 