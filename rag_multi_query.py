# --- 1. Installation and Setup ---
# Ensure you have the required libraries installed.
# pip install langchain langchain-openai chromadb openai python-dotenv beautifulsoup4

import os
from dotenv import load_dotenv
from typing import List
import logging

# Import key components from LangChain
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 2. Configuration and Environment ---

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from a .env file for security
load_dotenv()

# Check for required Azure OpenAI environment variables
required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"{var} is not set in the environment. Please add it to your .env file.")

# --- 3. Data Ingestion and Vector Store Preparation ---

# Use a real-world, detailed document for a robust example.
# Lilian Weng's blog on autonomous agents is an excellent source.
try:
    logging.info("Loading documents from the web...")
    loader = WebBaseLoader(web_path="https://lilianweng.github.io/posts/2023-06-23-agent/")
    documents = loader.load()
    logging.info(f"Successfully loaded {len(documents)} document(s).")

    # Split the document into smaller, manageable chunks for effective retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    doc_splits = text_splitter.split_documents(documents)
    logging.info(f"Document split into {len(doc_splits)} chunks.")

    # Create Azure OpenAI embeddings and initialize the Chroma vector store
    # This process converts text chunks into vectors and stores them for similarity search.
    logging.info("Creating embeddings and initializing vector store...")
    embedding_function = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-3-small",  # Replace with your deployment name
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-15-preview"  # Use appropriate API version
    )
    vector_store = Chroma.from_documents(documents=doc_splits, embedding=embedding_function)
    logging.info("Vector store created successfully.")

except Exception as e:
    logging.error(f"Failed during data ingestion or vector store setup: {e}")
    exit()


# --- 4. The Multi-Query Retriever ---

# Define the LLM to be used for generating query variations
# Using Azure OpenAI with gpt-4o-mini deployment
llm = AzureChatOpenAI(
    temperature=0,
    azure_deployment="gpt-4.1",  # Replace with your deployment name
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview"  # Use appropriate API version
)

# Set up the MultiQueryRetriever
# This retriever uses the LLM to generate multiple queries from different perspectives
# for a given user input. It then retrieves documents for all queries, and combines
# the unique results.
base_retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 docs per query
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever, llm=llm
)
logging.info("Multi-Query Retriever initialized.")


# --- 5. The RAG Chain for Answer Synthesis ---

# This prompt template structures the final call to the LLM, ensuring it uses the
# retrieved context to form a comprehensive and accurate answer.
RAG_PROMPT_TEMPLATE = """
You are an advanced AI assistant designed to answer questions based on a given context.
Please use the context provided below to answer the question. Your answer should be
concise, accurate, and directly derived from the information in the context.
If the context does not contain the answer, state that you cannot answer based on the
information provided.

Context:
{context}

Question:
{question}

Answer:
"""
rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

def format_docs(docs: List) -> str:
    """A utility function to format the retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

# Construct the final RAG chain using LangChain Expression Language (LCEL)
# This chain defines the flow:
# 1. The user's question is passed to the multi_query_retriever.
# 2. The retrieved documents are formatted into a single context string.
# 3. The context and original question are passed to the prompt template.
# 4. The formatted prompt is sent to the LLM.
# 5. The LLM's response is parsed into a string.
rag_chain = (
    {"context": multi_query_retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
logging.info("RAG chain constructed.")


# --- 6. Execution and Output ---

def run_query(question: str):
    """
    Executes the RAG chain with a given question and prints the results.
    """
    logging.info(f"\n--- Processing Query: '{question}' ---")

    # To see the generated queries, you can enable LangChain's debug mode:
    # import langchain
    # langchain.debug = True

    try:
        # Invoke the chain to get the final answer
        final_answer = rag_chain.invoke(question)

        # langchain.debug = False # Disable debug mode after the call

        print("\n[Final Answer]")
        print(final_answer)

    except Exception as e:
        logging.error(f"An error occurred while processing the query: {e}")


# --- 7. Conceptual Integration of Evaluation (e.g., Galileo) ---

def evaluate_retrieved_context(query: str, documents: List):
    """
    This is a conceptual function demonstrating where an evaluation tool like
    Galileo's Context Adherence metric would fit into the pipeline.
    """
    logging.info("\n--- [Conceptual Evaluation Step] ---")
    logging.info(f"Evaluating context for original query: '{query}'")
    logging.info(f"Retrieved {len(documents)} unique documents to be evaluated.")

    # In a production system, you would make an API call here:
    #
    # from galileo_sdk import Galileo
    # galileo = Galileo(api_key="YOUR_GALILEO_API_KEY")
    #
    # response = galileo.evaluate_retrieval(
    #     query=query,
    #     retrieved_documents=[doc.page_content for doc in documents]
    # )
    # adherence_score = response.context_adherence_score
    #
    # logging.info(f"Galileo Context Adherence Score: {adherence_score}")
    # if adherence_score < 0.7:
    #     logging.warning("Low context adherence detected. The retrieved context may not be relevant.")
    #
    # This score would be logged and used to monitor and improve the retriever's performance.
    print("This is where you would call an external service to score retrieval quality.")
    print("--------------------------------------")


# --- Main Execution Block ---
if __name__ == "__main__":
    # Define a somewhat vague or high-level user query that can benefit from rewriting
    original_query = "what are the challenges with LLM-powered autonomous agents?"

    # Run the main RAG process
    run_query(original_query)

    # Demonstrate the conceptual evaluation step
    # First, retrieve the documents without synthesizing an answer
    retrieved_docs = multi_query_retriever.invoke(original_query)
    evaluate_retrieved_context(original_query, retrieved_docs)
