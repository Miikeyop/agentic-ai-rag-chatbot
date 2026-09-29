from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma

EMBEDDING_MODEL = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

COLLECTION_NAME="agentic_ai"

CHROMA_PATH="chroma_db"

vector_store=Chroma(
    persist_directory=CHROMA_PATH,
    collection_name=COLLECTION_NAME,
    embedding_function=EMBEDDING_MODEL
)

def retrive_document(question,k=4):
    documents=vector_store.similarity_search_with_score(
        query=question,
        k=k
    )
    return documents

if __name__=="__main__":
    question="What is agentic AI?"
    documents=retrive_document(question)

    for i , (doc,score) in enumerate(documents):
        print(f"\nChunk {i + 1}")
        print("Page:", doc.metadata.get("page"))
        print("Score:", score)
        print(doc.page_content)



