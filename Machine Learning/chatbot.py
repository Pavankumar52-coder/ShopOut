# Importing necessary libraries for chatbot creation
import os
import json
import streamlit as st # For UI
from langchain.vectorstores import FAISS # Simple vector database
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Initializing the gemini api key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDfUtrnxNOiVYTXtEuav3xxQQLpR61iDlo"

# Load the translated text from translated.json
with open("translated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert translated text into LangChain documents
docs = [Document(page_content=item["text"]) for item in data]

# Split into smaller chunks if needed for better output
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Embeddings using Gemini LLM
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Build FAISS VectorDB
db = FAISS.from_documents(chunks, embeddings)

# Setting up retriever and gemini llm model
retriever = db.as_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
qa = RetrievalQA.from_llm(llm=llm, retriever=retriever)

# Streamlit UI
st.title("Telugu Translated Chatbot")
query = st.text_input("Ask a question based on your requirement:")

if query:
    with st.spinner("Getting answer from json file..."):
        answer = qa.run(query)
        st.success(answer)