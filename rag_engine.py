from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_ollama import OllamaLLM


PROJECT_FOLDER = Path(__file__).resolve().parent
DOCUMENT_FOLDER = PROJECT_FOLDER / "documents"
VECTOR_FOLDER = PROJECT_FOLDER / "vectorstore" / "chroma_db"


def create_vectorstore():

    loader = DirectoryLoader(
        DOCUMENT_FOLDER,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_FOLDER)
    )

    return vectorstore


def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=str(VECTOR_FOLDER),
        embedding_function=embeddings
    )

    return vectorstore


def get_answer(question):

    if not VECTOR_FOLDER.exists():
        vectorstore = create_vectorstore()
    else:
        vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    relevant_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in relevant_docs
    )

    prompt = f"""
You are an AI assistant for sustainable rainwater harvesting.

Answer the user's question using the provided context.

Rules:
- Use the context as the primary source.
- Do not invent technical facts.
- If the context does not contain enough information, say so.
- Give practical and simple explanations.
- For engineering or site-specific decisions, advise the user
  to follow applicable local standards and professional guidance.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    llm = OllamaLLM(model="llama3.2")

    answer = llm.invoke(prompt)

    return answer, relevant_docs