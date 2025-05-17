import os
import pickle
import re
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import torch
from langchain.vectorstores import Chroma, AtlasDB, FAISS
from RAGwithSagemaker.logging.logging import logger

def vectorizedocs(embeddings):
    logger.info("starting docs  loadig")
    loader = PyPDFDirectoryLoader("RAGwithSagemaker/data")
    docs = loader.load()
    logger.info("docs loaded")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    final_docs = text_splitter.split_documents(docs)
    logger.info("starting vector dbs")
    vector_store = FAISS.from_documents(final_docs, embeddings)
    # with open("vector_store.pth", "wb") as file:           # Optional. Helps in resuing the vectorspace directly without processing the files everytime
    #     vector_store = torch.save(vector_store,file)
    return vector_store