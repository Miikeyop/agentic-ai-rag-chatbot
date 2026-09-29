from langgraph.graph import START, END, StateGraph
from langchain_groq import ChatGroq
from typing import TypedDict
import os

from rag.retriver import retrive_document
from dotenv import load_dotenv


load_dotenv()


class State(TypedDict, total=False):
    question: str
    context: list
    scores: list
    confidence: float
    answer: str


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)


def retrieve_node(state: State):

    question = state["question"]

    results = retrive_document(question)

    context = []
    scores = []

    for doc, score in results:

        context.append({
            "text": doc.page_content,
            "page": doc.metadata.get("page"),
            "score": float(score)
        })

        scores.append(float(score))

    
    average_distance = sum(scores) / len(scores)

    confidence = max(0.0, 1.0 - average_distance)

    return {
        "context": context,
        "scores": scores,
        "confidence": confidence
    }


def generate_node(state: State):

    context = ""

    for item in state["context"]:
        context += (
            f"Page: {item['page']}\n"
            f"Text: {item['text']}\n\n"
        )

    prompt = f"""
You are an AI assistant answering questions about Agentic AI.

Answer ONLY using the provided context.

Do not use outside knowledge.

If the answer is not available in the context, respond exactly:

"I could not find enough information in the provided knowledge base."

Context:
{context}

Question:
{state["question"]}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


graph_builder = StateGraph(State)

graph_builder.add_node(
    "retrieve",
    retrieve_node
)

graph_builder.add_node(
    "generate",
    generate_node
)

graph_builder.add_edge(
    START,
    "retrieve"
)

graph_builder.add_edge(
    "retrieve",
    "generate"
)

graph_builder.add_edge(
    "generate",
    END
)

graph = graph_builder.compile()


if __name__ == "__main__":

    result = graph.invoke({
        "question": "What is Agentic AI?"
    })

    print("\nAnswer:")
    print(result["answer"])

    print("\nConfidence:")
    print(result["confidence"])

    print("\nRetrieved Context:")

    for i, item in enumerate(result["context"]):

        print(f"\nChunk {i + 1}")
        print("Page:", item["page"])
        print("Score:", item["score"])
        print(item["text"])