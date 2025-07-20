# EMR-RAG: Production-Ready RAG System on AWS SageMaker

A comprehensive Retrieval-Augmented Generation (RAG) platform built on AWS SageMaker with MongoDB Atlas integration, designed for enterprise-scale document intelligence and question answering.

## Overview

EMR-RAG demonstrates a complete production-ready RAG implementation that leverages AWS SageMaker for model deployment, MongoDB Atlas for vector storage, and LangChain for orchestration. The system provides both Flask and Streamlit interfaces for versatile user interaction while maintaining enterprise-grade scalability and security.

## Key Features

- **Enterprise-Grade Infrastructure**: Full AWS SageMaker integration with managed endpoints
- **Scalable Vector Storage**: MongoDB Atlas vector search with optimized indexing
- **Dual Model Deployment**: Separate embedding and text generation endpoints
- **Multi-Interface Support**: Both Flask API and Streamlit web interface
- **Production-Ready Architecture**: Comprehensive logging, monitoring, and error handling
- **Docker & Kubernetes Ready**: Complete containerization and orchestration support
- **Configurable Pipeline**: YAML-based configuration for different environments

## Architecture Overview

```
Documents → Embedding Model → Vector Store → Retrieval → LLM → Response
    ↓           ↓               ↓           ↓         ↓       ↓
  PDF Files  SageMaker      MongoDB    LangChain  SageMaker  User
            (GPT-J-6B)     Atlas      Framework  (Llama-2)  Interface
```

## System Components

### 1. Embedding Pipeline
- **Model**: Hugging Face GPT-J-6B (4096 dimensions)
- **Instance**: ml.g5.4xlarge SageMaker endpoint
- **Processing**: Document chunking and vectorization
- **Storage**: MongoDB Atlas vector collections

### 2. Text Generation Pipeline
- **Model**: Llama-2-7b-fp16
- **Instance**: ml.g5.12xlarge SageMaker endpoint
- **Configuration**: Optimized for context-aware generation
- **Integration**: LangChain document chain orchestration

### 3. Vector Search System
- **Database**: MongoDB Atlas with vector search capabilities
- **Index**: Optimized for 4096-dimensional embeddings
- **Similarity**: Cosine similarity with configurable thresholds
- **Performance**: Sub-second retrieval for production workloads

## Project Structure

```
vector-sage/
├── VectorSage/                 # Main package
│   ├── cloud/                  # AWS and MongoDB integration
│   │   ├── embeddingmodel.py   # SageMaker embedding deployment
│   │   ├── textgenerationmodel.py # SageMaker LLM deployment
│   │   ├── ragendpoints.py     # Endpoint management
│   │   ├── vectorize_docs.py   # Document processing
│   │   └── mongo_connecton.py  # MongoDB Atlas integration
│   ├── config/                 # Configuration management
│   │   └── configuration.py    # YAML-based configuration
│   ├── entity/                 # Data entities and models
│   │   └── config_entity.py    # Configuration classes
│   ├── logging/                # Logging infrastructure
│   │   └── logger.py           # Structured logging
│   └── utils/                  # Utility functions
│       └── common.py           # Common utilities
├── config/
│   └── config.yaml             # Main configuration
├── data/                       # Document storage
├── templates/                  # HTML templates
├── static/                     # Static web assets
├── app.py                      # Flask application
├── main.py                     # Main entry point
├── docker-compose.yml          # Multi-container setup
├── Dockerfile                  # Container configuration
├── params.yaml                 # Model parameters
└── requirements.txt            # Dependencies
```

## Installation

### Prerequisites

- AWS Account with SageMaker access
- MongoDB Atlas account
- Python 3.9+
- Docker (optional)
- AWS CLI configured

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MahammadRafi06/vector-sage.git
   cd vector-sage
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp embedding.env.example embedding.env
   # Edit embedding.env with your credentials
   ```

   Required environment variables:
   ```env
   MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://username:password@cluster.mongodb.net/
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_DEFAULT_REGION=us-east-1
   ```

5. **Update configuration:**
   ```bash
   # Edit config/config.yaml and params.yaml with your settings
   ```

## Configuration

### Main Configuration (`config/config.yaml`)
```yaml
artifacts_root: artifacts
sagemaker:
  region: us-east-1
  role: arn:aws:iam::account:role/SageMakerRole
  instance_type: ml.g5.4xlarge
```

### Model Parameters (`params.yaml`)
```yaml
rag:
  region: us-east-1
  embedding:
    embed_endpoint_name: huggingface-textembedding-gpt-j-6b-fp16
  llm:
    llm_endpoint_name: Llama-2-7b-fp16
    parameters:
      max_new_tokens: 500
      temperature: 0.1

mongo:
  DB_NAME: "langchain_test_db"
  COLLECTION_NAME: "langchain_test_vectorstores"
  ATLAS_VECTOR_SEARCH_INDEX_NAME: "langchain-test-index-vectorstores"
  embedding_dimenssion: 4096
  k: 2
  score: 0.2
```

## Deployment

### 1. Deploy SageMaker Models

```bash
# Deploy embedding model
python -c "
from VectorSage.config.configuration import ConfigurationManager
from VectorSage.cloud.embeddingmodel import DeployEmbeddingModel

config = ConfigurationManager()
sagemaker_config = config.get_sagemakersession_config()
embeddings_config = config.get_embeddings_config()

embedding_deploy = DeployEmbeddingModel(sagemaker_config, embeddings_config)
embedding_deploy.deploy_embedding_model()
"
```

```bash
# Deploy text generation model
python -c "
from VectorSage.config.configuration import ConfigurationManager
from VectorSage.cloud.textgenerationmodel import DeployTextGenerationModel

config = ConfigurationManager()
sagemaker_config = config.get_sagemakersession_config()
textgen_config = config.get_textgeneration_config()

text_deploy = DeployTextGenerationModel(sagemaker_config, textgen_config)
text_deploy.creat_and_deploy_model()
"
```

### 2. Initialize Vector Store

```bash
# Process documents and create vector store
python main.py
```

### 3. Run Applications

**Flask API:**
```bash
python app.py
```
Access at `http://localhost:5000`

**Streamlit Interface:**
```bash
streamlit run main.py
```
Access at `http://localhost:8501`

## Docker Deployment

### Single Container
```bash
docker build -t vector-sage .
docker run -p 5000:5000 --env-file embedding.env vector-sage
```

### Multi-Container with Docker Compose
```bash
docker-compose up -d
```

This starts:
- Flask application (port 5000)
- Streamlit application (port 8501)
- MongoDB instance (port 27017)

## API Reference

### Flask Endpoints

#### Query Endpoint
```bash
POST /
Content-Type: application/json

{
  "question": "What are the key features of this system?"
}
```

#### Health Check
```bash
GET /health
```

### Programmatic Usage

```python
from VectorSage.config.configuration import ConfigurationManager
from VectorSage.cloud.ragendpoints import RAGEndPoints
from VectorSage.cloud.mongo_connecton import mongo_setup

# Initialize configuration
config = ConfigurationManager()
rag_config = config.get_rag_config()
mongo_config = config.get_mongo_config()

# Create RAG endpoints
rag_endpoints = RAGEndPoints(rag_config)
embeddings_endpoint, llm_endpoint = rag_endpoints.create_rag_endpoints()

# Setup retriever
retriever = mongo_setup(embeddings_endpoint, mongo_config)

# Process query
response = retrieval_chain.invoke({"input": "Your question here"})
```

## Performance Optimization

### SageMaker Endpoints
- **Auto-scaling**: Configured for variable workloads
- **Instance Types**: Optimized for GPU-accelerated inference
- **Batch Processing**: Efficient handling of multiple requests

### MongoDB Atlas
- **Vector Indexing**: Optimized for 4096-dimensional embeddings
- **Sharding**: Horizontal scaling for large datasets
- **Caching**: Intelligent query result caching

### Application Layer
- **Connection Pooling**: Efficient database connection management
- **Async Processing**: Non-blocking request handling
- **Error Handling**: Comprehensive error recovery and logging

## Monitoring and Observability

### CloudWatch Integration
- SageMaker endpoint metrics
- Application performance monitoring
- Custom business metrics

### Application Logging
```python
from VectorSage.logging.logger import logger

logger.info("Processing user query")
logger.error("Model inference failed", extra={"error": str(e)})
```

### Health Checks
- SageMaker endpoint health
- MongoDB connection status
- Application readiness probes

## Security Best Practices

### AWS Security
- IAM roles with least privilege
- VPC endpoints for secure communication
- Encryption at rest and in transit

### MongoDB Security
- Connection string encryption
- Network access control
- Authentication and authorization

### Application Security
- Input validation and sanitization
- API rate limiting
- Security headers and CORS configuration

## Cost Optimization

### SageMaker Costs
- Use spot instances for development
- Implement auto-scaling policies
- Monitor and optimize instance usage

### MongoDB Atlas Costs
- Configure appropriate cluster tiers
- Implement data retention policies
- Monitor storage and compute usage

## Troubleshooting

### Common Issues

1. **SageMaker Endpoint Deployment Failures**
   ```bash
   # Check CloudWatch logs
   aws logs describe-log-groups --log-group-name-prefix /aws/sagemaker
   ```

2. **MongoDB Connection Issues**
   ```bash
   # Test connection
   python -c "
   from VectorSage.cloud.mongo_connecton import mongo_setup
   # Check connection logs
   "
   ```

3. **Memory Issues**
   ```bash
   # Monitor memory usage
   docker stats
   ```

### Debug Mode
```bash
export LOG_LEVEL=DEBUG
python app.py
```

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Write comprehensive tests**
4. **Ensure code quality** (run linters and tests)
5. **Update documentation**
6. **Commit changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linters
flake8 VectorSage/
black VectorSage/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**MahammadRafi**
- GitHub: [@MahammadRafi06](https://github.com/MahammadRafi06)
- Email: mrafi@uw.edu

## Acknowledgments

- **AWS SageMaker** team for managed ML infrastructure
- **MongoDB Atlas** for vector search capabilities
- **LangChain** for RAG framework
- **Hugging Face** for transformer models
- **Open source AI community** for continuous innovation

## Support

For questions, issues, or support:
- Open an issue on GitHub
- Check the comprehensive documentation
- Review existing discussions
- Contact the maintainer

## Roadmap

- [ ] Multi-modal document processing (images, tables)
- [ ] Advanced RAG techniques (hybrid search, reranking)
- [ ] Enterprise SSO integration
- [ ] Real-time document ingestion
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Cost optimization tools
- [ ] Performance benchmarking suite
