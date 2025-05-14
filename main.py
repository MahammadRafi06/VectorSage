from RAGwithSagemaker.config.configuration import ConfigurationManager
from RAGwithSagemaker.cloud.embeddingmodel import DeployEmbeddingModel
from RAGwithSagemaker.cloud.textgenerationmodel import DeployTextGenerationModel


congfiguration = ConfigurationManager()
sagemaker_config = congfiguration.get_sagemakersession_config()
embeddings_config = congfiguration.get_embeddings_config()
textgeneration_config = congfiguration.get_textgeneration_config()
s3_config = congfiguration.get_s3_config()

text_model_deploy =DeployTextGenerationModel(sagemaker_config, textgeneration_config)
text_model_deploy.creat_and_deploy_model()

embedding_model_deploy = DeployEmbeddingModel(sagemaker_config,embeddings_config )
embedding_model_deploy.deploy_embedding_model()