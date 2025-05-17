import sagemaker
import boto3
import json
import time
from sagemaker import Model, image_uris, serializers, deserializers
import os
import subprocess
from RAGwithSagemaker.utils.common import read_envfile, read_yaml, create_dir, save_json, load_json, save_bin, load_bin
from RAGwithSagemaker.logging.logging import logger
from RAGwithSagemaker.entity.config_entity import SagemakerSessionConfig, TextgenartionConfig
from RAGwithSagemaker.logging.logging import logger


class DeployTextGenerationModel:
    def __init__(self,sm_config: SagemakerSessionConfig, txt_config:TextgenartionConfig):
        logger.info(f"config received {sm_config} {txt_config}")
        self.sm_config = sm_config
        self.txt_config = txt_config

    def creat_and_deploy_model(self):
        sess = sagemaker.Session()
        try:
            role = self.sm_config.role
        except ValueError:
            iam = boto3.client("iam")
            role = iam.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]
        bucket = self.sm_config.bucket
        default_bucket_prefix = self.sm_config.default_bucket_prefix
        region = boto3.Session().region_name
        sm_client = boto3.client("sagemaker")
        smr = boto3.client("sagemaker-runtime")
        
        
        
        model_folder = self.txt_config.model.model_name
        os.makedirs(model_folder, exist_ok=True)

        with open(f"{model_folder}/serving.properties", "w") as file:
            properties = self.txt_config.servingproperties
            for pro in properties.items():
                p,v = pro
                file.write(f"{p}={v}\n")
        # with open(f"{model_folder}/requirements.txt", "w") as file:
        #     file.write("lmi-dist")
        logger.info("Propteries file written to location")        
        archive_name = f"{model_folder}.tar.gz"
        subprocess.run(["tar", "czvf", archive_name, model_folder], check=True)
        subprocess.run(["rm", "-rf", model_folder], check=True)
        logger.info("Tar file generated")
        image_uri = image_uris.retrieve(framework=self.txt_config.image.framework, region=region, version=self.txt_config.image.version)
        #image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/djl-inference:0.23.0-deepspeed0.9.5-cu118"
        logger.info(f"image uri is : {image_uri}")
        s3_code_prefix = self.txt_config.s3_code_prefix

        if default_bucket_prefix:
            s3_code_prefix = f"{default_bucket_prefix}/{s3_code_prefix}"

        code_artifact = sess.upload_data(archive_name, bucket, s3_code_prefix)
        logger.info("code artificats pushed to s3")
        falcon_model_name = sagemaker.utils.name_from_base(self.txt_config.base_name_endpoint)
        logger.info(f"model name is: {falcon_model_name}")
        model = Model(
            sagemaker_session=sess,
            image_uri=image_uri,
            model_data=code_artifact,
            role=role,
            name=falcon_model_name,)
        instance_type = self.txt_config.instance_type
        endpoint_name = self.txt_config.endpoint_name
        logger.info("model generated")
        model.deploy(
            initial_instance_count=1,
            instance_type=instance_type,
            endpoint_name=endpoint_name,
            container_startup_health_check_timeout=600,
            wait=True,
        )