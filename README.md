# RAG Multi-Query Example

This project demonstrates an advanced Retrieval-Augmented Generation (RAG) pipeline using LangChain, OpenAI, and a vector store. It leverages a `MultiQueryRetriever` to enhance retrieval accuracy by generating multiple query variations from a single user question.

## Key Features

- **Multi-Query Retriever**: Automatically generates multiple perspectives on a user's query to find more comprehensive and relevant documents.
- **LangChain Expression Language (LCEL)**: Constructs a clean and modular RAG chain.
- **Azure OpenAI Integration**: Uses Azure's services for both embeddings and language model inference.
- **Vector Store**: Utilizes ChromaDB for efficient storage and retrieval of document embeddings.
- **Conceptual Evaluation**: Includes a placeholder for integrating retrieval evaluation tools like Galileo.

## How It Works

The main script, `rag_multi_query.py`, performs the following steps:
1.  **Loads Data**: Ingests a document from a web URL.
2.  **Splits and Embeds**: Splits the document into smaller chunks and converts them into vector embeddings using Azure OpenAI.
3.  **Stores Vectors**: Stores the embeddings in a Chroma vector store.
4.  **Retrieves Documents**: When a user asks a question, the `MultiQueryRetriever` generates several versions of the question, retrieves relevant documents for each, and combines the results.
5.  **Synthesizes Answer**: A RAG chain passes the retrieved documents and the original question to an LLM, which generates a final answer based on the provided context.

## Getting Started

### Prerequisites

- Python 3.8+
- An Azure account with access to Azure OpenAI service.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Install Dependencies

It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root of the project and add your Azure OpenAI credentials:

```env
AZURE_OPENAI_API_KEY="your_azure_openai_api_key"
AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
```

You will also need to update the `azure_deployment` names for the embedding model and the chat model inside `rag_multi_query.py` to match your deployment names in Azure.

-   `AzureOpenAIEmbeddings(azure_deployment="text-embedding-3-small", ...)`
-   `AzureChatOpenAI(azure_deployment="gpt-4.1", ...)`

### 4. Run the Script

Execute the script to see the RAG pipeline in action:

```bash
python rag_multi_query.py
```

The script will process a predefined question and print the retrieved answer to the console. You can modify the `original_query` in the `if __name__ == "__main__":` block to ask your own questions.
