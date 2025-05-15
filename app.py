from flask import Flask, render_template, request
from RAGwithSagemaker.config.configuration import ConfigurationManager
from RAGwithSagemaker.cloud.embeddingmodel import DeployEmbeddingModel
from RAGwithSagemaker.cloud.textgenerationmodel import DeployTextGenerationModel
from RAGwithSagemaker.cloud.ragendpoints import RAGEndPoints
from RAGwithSagemaker.cloud.vectorize_docs import vectorizedocs
from RAGwithSagemaker.logging.logging import logger
from RAGwithSagemaker.cloud.mongo_connecton import mongo_setup

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
app = Flask(__name__)


# Initialize the RAG pipeline
logger.info("Setting up RAG pipeline...")

congfiguration = ConfigurationManager()
sagemaker_config = congfiguration.get_sagemakersession_config()
embeddings_config = congfiguration.get_embeddings_config()
textgeneration_config = congfiguration.get_textgeneration_config()
s3_config = congfiguration.get_s3_config()
rag_config = congfiguration.get_rag_config()
mongo_config = congfiguration.get_mongo_config()

# text_model_deploy =DeployTextGenerationModel(sagemaker_config, textgeneration_config)
# text_model_deploy.creat_and_deploy_model()

# embedding_model_deploy = DeployEmbeddingModel(sagemaker_config,embeddings_config )
# embedding_model_deploy.deploy_embedding_model()

rag_endpoints = RAGEndPoints(rag_config)
embeddings_endpoint, sm_llm_endpoint = rag_endpoints.create_rag_endpoints()

retriever = mongo_setup(embeddings_endpoint, mongo_config)

prompt = ChatPromptTemplate.from_template("""
Role: You are an assistant with deep expertise in chemical compounds and their properties...
<context>
{context}
</context>
Question: {input}
""")
document_chain = create_stuff_documents_chain(sm_llm_endpoint, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        user_input = request.form.get("question")
        if user_input:
            logger.info(f"User asked: {user_input}")
            try:
                result = retrieval_chain.invoke({"input": user_input})
                answer = result.get("answer", "No answer returned.")
            except Exception as e:
                logger.error(f"Error in retrieval chain: {e}")
                answer = "There was an error processing your request."
    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
