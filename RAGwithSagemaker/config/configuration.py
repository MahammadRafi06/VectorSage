from RAGwithSagemaker.constants import CONFIG_FILE_PATH, SCHEMA_FILE_PATH, PARAMS_FILE_PATH, ENV_FILE_PATH_EMBEDDINGS
from RAGwithSagemaker.utils.common import read_yaml, create_dir, read_envfile
from RAGwithSagemaker.entity.config_entity import (SagemakerSessionConfig,
                                                   EmbeddingsConfig, 
                                                   TextgenartionConfig,
                                                   S3Config
                                                   )
import os 
from pathlib import Path
class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, schema_file_path= SCHEMA_FILE_PATH, params_file_path=PARAMS_FILE_PATH,env_file_path_embeddings=ENV_FILE_PATH_EMBEDDINGS):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)
        self.envs = read_envfile(env_file_path_embeddings)  
        create_dir([self.config.artifacts_root])
        
    def get_sagemakersession_config(self)-> SagemakerSessionConfig:
        config = self.config.sagemaker
        sagemaker_config = SagemakerSessionConfig(
              role= config.role,
              bucket=config.bucket,
              default_bucket_prefix=config.default_bucket_prefix ,
        )
        return sagemaker_config
    
    def get_embeddings_config(self)-> EmbeddingsConfig:
        config = self.config.embeddings
        embeddings_config = EmbeddingsConfig(
            instance_type = config.instance_type,
            model_version = config.model_version,
            model_id = config.model_id,
            model_scope = config.model_scope,
            image_scope= config.image_scope,
            env = self.envs,
            role = config.role
        )
        return embeddings_config
    
    def get_textgeneration_config(self)-> TextgenartionConfig:
        config = self.config.textgenartion

        textgeneration_config = TextgenartionConfig(
            servingproperties= config.servingproperties,
            model=config.model,
            image = config.image,
            instance_type = config.instance_type,
            model_folder = config.model_folder,
            base_name_endpoint = config.base_name_endpoint,
            s3_code_prefix = config.s3_code_prefix
        )
        return textgeneration_config
    
    def get_s3_config(self)-> S3Config:
        config = self.config.s3
        s3_config = S3Config(
            s3_code_prefix= config.s3_code_prefix,
            bucket = config.bucket,
        )
        return s3_config
        