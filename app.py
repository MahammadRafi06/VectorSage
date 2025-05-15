from flask import Flask, render_template, request
from RAGwithSagemaker.config.configuration import ConfigurationManager
from RAGwithSagemaker.cloud.embeddingmodel import DeployEmbeddingModel
from RAGwithSagemaker.cloud.textgenerationmodel import DeployTextGenerationModel
from RAGwithSagemaker.cloud.ragendpoints import RAGEndPoints
from RAGwithSagemaker.cloud.vectorize_docs import vectorizedocs
from RAGwithSagemaker.logging.logging import logger

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

app = Flask(__name__)

# Initialize the RAG pipeline
logger.info("Setting up RAG pipeline...")

config = ConfigurationManager()
sagemaker_config = config.get_sagemakersession_config()
embeddings_config = config.get_embeddings_config()
textgeneration_config = config.get_textgeneration_config()
rag_config = config.get_rag_config()

DeployTextGenerationModel(sagemaker_config, textgeneration_config).creat_and_deploy_model()
DeployEmbeddingModel(sagemaker_config, embeddings_config).deploy_embedding_model()
embeddings_endpoint, sm_llm_endpoint = RAGEndPoints(rag_config).create_rag_endpoints()
vector_store = vectorizedocs(embeddings_endpoint)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

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
