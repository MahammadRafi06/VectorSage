from RAGwithSagemaker.entity.config_entity import (ContentHandlerEmbedding, 
                                                   ContentHandlerLLM,
                                                   SagemakerEndpointEmbeddingsJumpStart,
                                                   RagConfig)

from langchain.llms.sagemaker_endpoint import SagemakerEndpoint


class RAGEndPoints():
    def __init__(self,rag_config: RagConfig):
        self.embed_endpoint_name = rag_config.embed_endpoint_name
        self.llm_endpoint_name = rag_config.llm_endpoint_name
        self.parameters= rag_config.parameters
        self.region = rag_config.region
        self.content_handler_embedding = ContentHandlerEmbedding()
        self.content_handler_llm = ContentHandlerLLM()

    def create_rag_endpoints(self):    
        embeddings = SagemakerEndpointEmbeddingsJumpStart(
            endpoint_name=self.embed_endpoint_name,
            region_name=self.region,
            content_handler=self.content_handler_embedding
        )

        sm_llm = SagemakerEndpoint(
            endpoint_name=self.llm_endpoint_name,
            region_name=self.region,
            model_kwargs=self.parameters,
            content_handler=self.content_handler_llm,
        )
        return embeddings, sm_llm


