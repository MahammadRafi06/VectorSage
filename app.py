import os
import pickle
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import streamlit as st
import torch

load_dotenv()

os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

loader = PyPDFDirectoryLoader("./drive/MyDrive/myDrive/")
docs = loader.load()

# Split the documents into smaller chunks for better processing
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
final_docs = text_splitter.split_documents(docs)

with open("docs.pkl", "wb") as file:  #optinal
    pickle.dump(final_docs, file)

with open('docs.pkl', 'rb') as file: #optional
    final_docs = pickle.load(file)

### Add context to each documnet
for doc in final_docs:
    match = re.search(r'/([^/]+)\.pdf$', doc.metadata['source'])
    if match:
        filename = match.group(1)
        if filename != "Reports":
            formatted_filename = filename.split("_", 1)[1]
            doc.metadata['source'] = formatted_filename
            doc.page_content = "This document talks about the chemical " + formatted_filename + ". " + doc.page_content

vector_store = FAISS.from_documents(final_docs, embeddings)

with open("vector_store.pth", "wb") as file:           # Optional. Helps in resuing the vectorspace directly without processing the files everytime
    vector_store = torch.save(vector_store,file)


llm = ChatOpenAI(model_name="gpt-4o")

# Load a pre-built FAISS vector store from a pickle file
# This vector store is likely a larger, pre-computed set of document embeddings
with open("vector_store.pth", "rb") as file:            # optional(only required when you want to reuse the saved vector store. If you have GPU then remove the maplocation argument)
    vector_store = torch.load(file, map_location=torch.device('cpu'))

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
