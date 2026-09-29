
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma

pdf_path = "data/Ebook-Agentic-AI.pdf"


def load_pdf():

    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        return documents

    except Exception as e:
        print("Error while loading PDF:", e)
        return []

def split_documents(documents):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
        )
    chunks=text_splitter.split_documents(documents)
    return chunks

def get_embedding_model():

    embedding_model = FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return embedding_model

def store_in_chroma(chunks, embedding_model):

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db",
        collection_name="agentic_ai"
    )

    return vector_store

documents = load_pdf()

if documents:

    chunks = split_documents(documents)

    embedding_model = get_embedding_model()

    store_in_chroma(
        chunks,
        embedding_model
    )

    print("Documents stored successfully in ChromaDB")

    