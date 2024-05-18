import streamlit as st

from langchain_community.document_loaders import WebBaseLoader

from langchain_community.vectorstores import Chroma

from langchain_community import embeddings

from langchain_community.llms import Ollama

from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

from langchain.text_splitter import CharacterTextSplitter 

from langsmith import traceable, wrappers

from langsmith import Client

from langchain_community.vectorstores import Qdrant

from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from qdrant_client import QdrantClient


def get_vector_store():
    model_name = "BAAI/bge-large-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    url = "http://localhost:6333"

    client = QdrantClient(
        url=url, prefer_grpc=False
    )

    print(client)
    print("##############")

    vector_store = Qdrant(client=client, embeddings=embeddings, collection_name="vector_db")
    return vector_store

def process_input(question):
    model_local = Ollama(model="llama2", temperature = 0.5)

    vectorstore = get_vector_store()
    
    retriever = vectorstore.as_retriever(search_kwargs={"k" : 3})
    
    #perform the RAG 
    after_rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )
    # Extract keywords from the question
    answer = after_rag_chain.invoke(question) 
    keywords = question.lower().split()

    # Filter the answer based on keyword presence
    filtered_answer = ""
    for sentence in answer.split("."):
      if any(keyword in sentence.lower() for keyword in keywords):
        filtered_answer += sentence + ". "

    return filtered_answer.strip() if filtered_answer else "Sorry, I couldn't find a relevant answer."

# STREAMLIT
st.title("Chatbot for Developers")
st.write("Enter your query.")

# Input fields
question = st.text_input("Question")

# Button to process input
if st.button('Submit'):
    with st.spinner('Processing...'):
        answer = process_input(question)
        st.text_area("Answer", value=answer, height=300, disabled=True)