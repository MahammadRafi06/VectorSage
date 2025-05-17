import os
import pytest
from flask import Flask
from mongomock import MongoClient
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv("template.env")

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        "MONGODB_URI": "mongodb://localhost:27017/",
        "MONGODB_DB": "test_db",
    })
    
    # Other setup can go here
    
    yield app
    
    # Clean up / reset resources here

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mock_mongo():
    """Create a mock MongoDB client."""
    return MongoClient()

@pytest.fixture
def mock_embedding_model():
    """Mock the embedding model for testing."""
    class MockEmbeddingModel:
        def encode(self, text):
            # Return mock embeddings of correct dimension
            return [0.0] * 4096
    
    return MockEmbeddingModel()

@pytest.fixture
def mock_llm():
    """Mock the LLM for testing."""
    class MockLLM:
        def generate(self, prompt):
            return "This is a mock response"
    
    return MockLLM() 