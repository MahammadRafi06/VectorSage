from sagemaker import image_uris, model_uris, script_uris, hyperparameters
from sagemaker.model import Model
from sagemaker.predictor import Predictor
import os
import time
import sagemaker
import boto3
from RAGwithSagemaker.utils.common import read_envfile, read_yaml, create_dir, save_json, load_json, save_bin, load_bin
from RAGwithSagemaker.logging.logging import logger
from RAGwithSagemaker.entity.config_entity import SagemakerSessionConfig, EmbeddingsConfig



class DeployEmbeddingModel:
    def __init__(self, sm_config: SagemakerSessionConfig, embd_config:EmbeddingsConfig):
        self.instance_type = embd_config.instance_type
        self.model_version = embd_config.model_version
        self.model_id = embd_config.model_id
        self.model_scope = embd_config.model_scope
        self.image_scope= embd_config.image_scope
        self.env = embd_config.env
        self.role = embd_config.role
    def deploy_embedding_model(self):
        sm_client = boto3.client("sagemaker")
        smr = boto3.client("sagemaker-runtime")
        instance_type = self.instance_type  # instance type to use for deployment
        model_version = self.model_version
        env = self.env
        model_scope = self.model_scope
        model_id = self.model_id
        model_uri = model_uris.retrieve(
            model_id=model_id, model_version=model_version, model_scope= model_scope
        )
        embed_endpoint_name = sagemaker.utils.name_from_base(model_id)

        # Retrieve the inference container uri. This is the base HuggingFace container image for the default model above.
        deploy_image_uri = image_uris.retrieve(
            region=None,
            framework=None,  # automatically inferred from model_id
            image_scope=self.image_scope,
            model_id=model_id,
            model_version=model_version,
            instance_type=instance_type,
        )
        model_inference = Model(
            image_uri=deploy_image_uri,
            model_data=model_uri,
            role=self.role,
            predictor_cls=Predictor,
            name=model_id,
            env=env,
        )
        # model_predictor_inference = model_inference.deploy(
        #     initial_instance_count=1,
        #     instance_type=instance_type,
        #     predictor_cls=Predictor,
        #     endpoint_name=embed_endpoint_name,
        #     wait=False,
        # )
        # print(f"Model {model_id} has been created successfully.")

        # # wait for the endpoint to be deployed successfully
        # def wait_for_endpoint(endpoint_name=None):
        #     describe_endpoint_response = sm_client.describe_endpoint(EndpointName=endpoint_name)

        #     while describe_endpoint_response["EndpointStatus"] == "Creating":
        #         describe_endpoint_response = sm_client.describe_endpoint(EndpointName=endpoint_name)
        #         print(describe_endpoint_response["EndpointStatus"])
        #         time.sleep(15)

        #     print(f"endpoint {endpoint_name} is in service now.")
        #     return
