from dataclasses import dataclass
from pathlib import Path

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

@dataclass
class TextgenartionConfig:
    servingproperties: dict
    model: dict
    image: dict
    instance_type: str 
    model_folder: Path
    base_name_endpoint: str
    s3_code_prefix: Path
@dataclass
class S3Config:
    s3_code_prefix: str
    bucket: str