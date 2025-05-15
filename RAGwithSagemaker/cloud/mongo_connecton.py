from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from uuid import uuid4

from RAGwithSagemaker.logging.logging import logger


load_dotenv()


def mongo_setup(embeddings, mongo_config):
    
    MONGODB_ATLAS_CLUSTER_URI = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
    client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    db = mongo_config.DB_NAME
    collection = mongo_config.COLLECTION_NAME
    index_ = mongo_config.ATLAS_VECTOR_SEARCH_INDEX_NAME
    MONGODB_COLLECTION = client[db][collection]
    
    existing_indexes = MONGODB_COLLECTION.index_information()
    index_exists = any(index_ in idx for idx in existing_indexes)
    
    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=embeddings,
        index_name=index_,
        relevance_score_fn="cosine",
        )
    
    if not index_exists:
        logger.info(f"Index '{index_}' does not exist. Creating and adding documents...")
        
        loader = PyPDFDirectoryLoader(mongo_config.datafolder)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
        final_docs = text_splitter.split_documents(docs)
        
        vector_store.create_vector_search_index(dimensions=mongo_config.embedding_dimenssion)
        uuids = [str(uuid4()) for _ in range(len(final_docs))]
        vector_store.add_documents(documents=final_docs, ids=uuids)   
    else:
         logger.info((f"Index '{index_}' already exists. Skipping creation and document insertion."))
    retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": mongo_config.k, "score_threshold": mongo_config.score},
    )
    
    return retriever

