from RAGwithSagemaker.config.configuration import ConfigurationManager
from RAGwithSagemaker.cloud.embeddingmodel import DeployEmbeddingModel
from RAGwithSagemaker.cloud.textgenerationmodel import DeployTextGenerationModel
from RAGwithSagemaker.cloud.ragendpoints import RAGEndPoints
from RAGwithSagemaker.cloud.vectorize_docs import vectorizedocs
from RAGwithSagemaker.logging.logging import logger


congfiguration = ConfigurationManager()
sagemaker_config = congfiguration.get_sagemakersession_config()
embeddings_config = congfiguration.get_embeddings_config()
textgeneration_config = congfiguration.get_textgeneration_config()
s3_config = congfiguration.get_s3_config()
rag_config = congfiguration.get_rag_config()

text_model_deploy =DeployTextGenerationModel(sagemaker_config, textgeneration_config)
text_model_deploy.creat_and_deploy_model()

embedding_model_deploy = DeployEmbeddingModel(sagemaker_config,embeddings_config )
embedding_model_deploy.deploy_embedding_model()

rag_endpoints = RAGEndPoints(rag_config)
embeddings_endpoint, sm_llm_endpoint = rag_endpoints.create_rag_endpoints()

logger.info("Started vector db")
vector_store = vectorizedocs(embeddings_endpoint)



import os
import pickle
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import streamlit as st

llm = sm_llm_endpoint

# Load a pre-built FAISS vector store from a pickle file
# This vector store is likely a larger, pre-computed set of document embeddings

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Define a prompt template for the language model
# The template provides the context and structure for how the model should generate responses
prompt = ChatPromptTemplate.from_template("""
Role: You are an assistant with deep expertise in chemical compounds and their properties. The user is a researcher trying to find some trends in the chemical compounds.
You have been supplied with data, including drug adverse reaction reports, patient demographics, administered drugs, and observed reactions in patients.
Additionally, you have detailed information about each drug, including molecular structure, chemical properties (such as melting points), and more. 
Some of the drug names mentioned in the documents are Tobramycin, Opicapone, Zanubrutinib, and Levoleucovorin disodium. You can find the compound or drug name at the start of each document.
Some example reactions include nausea, vomiting, gastrointestinal discomfort, and disruptions in normal physiological processes.
Some example chemical properties include Molecular Formula, Molecular Weight, Hydrogen Bond Donor Count, Hydrogen Bond Acceptor Count, Polar Surface Area, and Formal Charge.
Using this wealth of information, provide accurate and insightful answers to user inquiries.
<context>
{context}
</context>
Question: {input}""")

# Create a document processing chain using the LLM and prompt
document_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Main entry point of the Streamlit app
if __name__ == "__main__":
    st.set_page_config(
        page_title="Drug Reaction Trends Analysis",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
            .main {
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 10px;
                font-family: Arial, sans-serif;
            }
            .reportview-container {
                padding-top: 0;
            }
            .stTextInput > div > div > input {
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                width: 100%;
            }
            .stButton button {
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            .stButton button:hover {
                background-color: #45a049;
            }
            .stTitle {
                color: #2c3e50;
                text-align: center;
                font-weight: bold;
            }
            .stMarkdown {
                font-size: 16px;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("💊 Drug Reaction Trends and Insights with AI")

    st.markdown("""
    Welcome to the Drug Reaction Trends Analysis app. This tool leverages advanced AI models to analyze drug reactions data 
    from OpenFDA combined with PubChem substance data to uncover trends and insights about compounds and drugs that cause adverse reactions.
    
    **Ask any question you have about drug reactions and get insightful answers generated by AI.**
    """)

    user_input = st.text_input("💬 Your Question:", placeholder="Type your question here...")

    if user_input:
        with st.spinner('Processing your question...'):
            response = retrieval_chain.invoke({"input": user_input})
        
        st.markdown("### Resonse:")
        st.markdown(f"{response['answer']}")
    
    st.markdown("""
    ---
    *Powered by LangChain, OpenAI, and Streamlit. Data sourced from OpenFDA and PubChem.*
    """)