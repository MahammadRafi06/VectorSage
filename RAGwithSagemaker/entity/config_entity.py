from dataclasses import dataclass
from pathlib import Path
from langchain_community.embeddings.sagemaker_endpoint import EmbeddingsContentHandler
from langchain_community.embeddings import SagemakerEndpointEmbeddings
# from langchain.llms.sagemaker_endpoint import ContentHandlerBase
from typing import Any, Dict, List, Optional
import json
from langchain.llms.sagemaker_endpoint import LLMContentHandler


@dataclass
class SagemakerSessionConfig:
  bucket: str
  default_bucket_prefix: str
  role: str

@dataclass
class EmbeddingsConfig:
  instance_type: str
  model_version: str
  model_id: str
  model_scope: str
  image_scope: str
  env: dict
  role: str
  endpoint_name: str

@dataclass
class TextgenartionConfig:
    servingproperties: dict
    model: dict
    image: dict
    instance_type: str 
    model_folder: Path
    base_name_endpoint: str
    s3_code_prefix: Path
    endpoint_name: str
@dataclass
class S3Config:
    s3_code_prefix: str
    bucket: str
@dataclass
class RagConfig:
    embed_endpoint_name: str
    llm_endpoint_name: str
    parameters: dict
    region: str  

@dataclass
class MongoConfig:
    DB_NAME: str
    COLLECTION_NAME: str
    ATLAS_VECTOR_SEARCH_INDEX_NAME: str
    datafolder: Path
    embedding_dimenssion: int
    k: int
    score: float


class SagemakerEndpointEmbeddingsJumpStart(SagemakerEndpointEmbeddings):
    def embed_documents(self, texts: List[str], chunk_size: int = 5) -> List[List[float]]:
        """Compute doc embeddings using a SageMaker Inference Endpoint.

        Args:
            texts: The list of texts to embed.
            chunk_size: The chunk size defines how many input texts will
                be grouped together as request. If None, will use the
                chunk size specified by the class.

        Returns:
            List of embeddings, one for each text.
        """
        results = []
        _chunk_size = len(texts) if chunk_size > len(texts) else chunk_size
        for i in range(0, len(texts), _chunk_size):
            response = self._embedding_func(texts[i : i + _chunk_size])
            print
            results.extend(response)
        return results


class ContentHandlerEmbedding(EmbeddingsContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs={}) -> bytes:
        input_str = json.dumps({"text_inputs": prompt, **model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        embeddings = response_json["embedding"]
        return embeddings


class ContentHandlerLLM(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs={}) -> bytes:
        input_str = json.dumps({"inputs": prompt, "parameters": {**model_kwargs}})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = output.read()
        res = json.loads(response_json)
        ans = res["generated_text"]
        return ans