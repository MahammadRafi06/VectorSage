from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from RAGwithSagemaker.logging.logging import logger


load_dotenv()


def mongo_setup(embeddings):
  MONGODB_ATLAS_CLUSTER_URI = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
  client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
  try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
      print(e)
  logger.info("starting docs  loadig")
  loader = PyPDFDirectoryLoader("RAGwithSagemaker/data")
  docs = loader.load()
  logger.info("docs loaded")
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
  final_docs = text_splitter.split_documents(docs)
  logger.info("starting vector dbs")
  
  return vector_store

