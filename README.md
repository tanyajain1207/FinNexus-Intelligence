# FinNexus-Intelligence 🚀

This project implements a **full-stack** Graph-based Retrieval Augmented Generation (RAG) system using Neo4j, LangChain, and various LLM techniques to analyze and query Apple Inc.'s 2024 annual report data. It features a modern React frontend and FastAPI backend with chart generation capabilities. 📊

## Project Overview 🎯

This project combines traditional vector-based retrieval with graph-based knowledge extraction to provide more accurate and contextual answers to queries about Apple's financial and business information. It uses a hybrid approach that leverages both structured (graph) and unstructured (vector) data for comprehensive information retrieval.

**Key Highlights:**
- 🌐 **Web Interface**: Modern React-based chat UI for interactive queries
- 🔌 **REST API**: FastAPI backend with two endpoints for text and chart queries
- 📈 **Chart Generation**: Automatic visualization of financial data
- 🕸️ **Hybrid RAG**: Combines graph and vector search for better accuracy
- 💬 **Chat History**: Context-aware conversations with memory

## Features ✨

### Core RAG Features
- **Document Processing**: 📄
  - PDF document ingestion and chunking
  - Recursive text splitting with configurable chunk sizes
  - Graph document transformation using LLMGraphTransformer

- **Knowledge Graph Construction**: 🕸️
  - Neo4j graph database integration
  - Entity extraction and relationship mapping
  - Graph document storage with source tracking

- **Vector Store Integration**: 🔍
  - HuggingFace embeddings integration
  - Hybrid search capabilities
  - Vector indexing for efficient retrieval

- **Query Processing**: 💡
  - Natural language query understanding
  - Entity extraction from queries
  - Context-aware response generation
  - Chat history management

### Web Application Features
- **Modern UI**: 🎨
  - Professional financial-themed design
  - Responsive layout (desktop, tablet, mobile)
  - Real-time chat interface
  - Image support for chart visualization

- **Chart Generation**: 📊
  - Automatic chart creation from queries
  - Multiple chart types (bar, line, pie, area)
  - Base64 image rendering in chat
  - Smart data extraction from RAG responses

- **API Endpoints**: 🔌
  - `/api/query` - Text-based Q&A
  - `/api/chart` - Chart generation endpoint
  - Automatic routing based on query content

## Technical Architecture 🏗️

### System Components

1. **Frontend (React)**
   - React 18 with functional components
   - Axios for API communication
   - Modern CSS with animations
   - Port: 3000

2. **Backend (FastAPI)**
   - RESTful API with CORS support
   - RAG chain integration
   - Chart generation service
   - Port: 5000

3. **Document Processing Pipeline**
   - PyPDFLoader for PDF ingestion
   - RecursiveCharacterTextSplitter for text chunking
   - LLMGraphTransformer for graph document creation

4. **Storage Layer**
   - Neo4j Graph Database for structured data
   - Vector store for embeddings
   - Pickle-based document caching

5. **Retrieval System**
   - Hybrid retrieval combining graph and vector search
   - Entity-aware structured queries
   - Context-based response generation

### Key Technologies 💻

- **Frontend**: React, Axios, CSS3
- **Backend**: FastAPI, Uvicorn
- **Databases**: Neo4j 🗄️
- **Embeddings**: HuggingFace (sentence-transformers/all-mpnet-base-v2) 🤗
- **LLM Integration**: Gemini (gemini-2.5-flash) 🧠
- **Framework**: LangChain ⚡
- **Visualization**: Matplotlib 📊
- **Development**: Python, Jupyter Notebook, Node.js 🐍

## Setup Requirements 🛠️

### Prerequisites

1. **Python 3.8+** installed
2. **Node.js 14+** installed (for frontend)
3. **Neo4j Database** (Aura or local instance)
4. **API Keys**:
   - Google Gemini API key
   - Neo4j credentials

### Environment Variables

Create a `.env` file in the project root:

```env
# Neo4j Configuration
NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AURA_INSTANCEID=xxxxxxxx
AURA_INSTANCENAME=InstanceXX

# LLM API Keys
OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
groq_api_key=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Note**: The project uses Gemini by default. `OPENAI_API_KEY` and `groq_api_key` are optional depending on your LLM configuration.

### Python Dependencies 📦

Install all required Python packages:

```bash
pip install fastapi uvicorn python-dotenv langchain langchain-community langchain-google-genai langchain-neo4j langchain-experimental pydantic matplotlib numpy faiss-cpu sentence-transformers pypdf
```

Or install individually:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variable management
- `langchain` - Core LangChain framework
- `langchain-community` - Community integrations
- `langchain-google-genai` - Gemini integration
- `langchain-neo4j` - Neo4j integration
- `langchain-experimental` - Experimental features (LLMGraphTransformer)
- `pydantic` - Data validation
- `matplotlib` - Chart generation
- `numpy` - Numerical operations
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Embeddings
- `pypdf` - PDF processing
- `neo4j` - Neo4j driver

### Frontend Dependencies 📦

Navigate to the `frontend` directory and install:

```bash
cd frontend
npm install
```

This installs:
- `react` & `react-dom` - React framework
- `react-scripts` - Build tools
- `axios` - HTTP client

## Installation & Setup 🚀

### Step 1: Clone and Setup Environment

1. Clone the repository
2. Create `.env` file with your credentials (see Environment Variables above)
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt  # If available, or use pip install command above
   ```

### Step 2: Import Graph Data to Neo4j

1. Ensure `graph_documents.pkl` is in the project root
2. Run the import script:
   ```bash
   python import_data.py
   ```
   This loads the graph documents into your Neo4j database.

### Step 3: Start Backend API

Navigate to the `backend_api` directory:

```bash
cd backend_api
python backend_api.py
```

The backend will start at `http://localhost:5000`

**Verify**: Visit `http://localhost:5000` - you should see:
```json
{"status": "Hybrid Graph RAG backend running successfully!"}
```

### Step 4: Start Frontend

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
npm install  # First time only
npm start
```

The frontend will start at `http://localhost:3000` and open automatically in your browser.

### Step 5: Use the Application

1. Open `http://localhost:3000` in your browser
2. Start asking questions about Apple's 2024 Annual Report
3. For charts, include the word "chart" in your query (e.g., "Show me a chart of revenue trends")

## Usage 🚀

### Web Interface Usage

1. **Text Queries**: Simply type your question and press Enter
   - Example: "What is Apple's revenue for 2024?"
   - Example: "What are the main risks mentioned?"

2. **Chart Queries**: Include "chart" in your question
   - Example: "Show me a chart of capital expenditure evolution"
   - Example: "Create a chart showing revenue trends"
   - The system automatically routes to the chart endpoint

3. **Chat History**: The system maintains conversation context
   - Follow-up questions work naturally
   - Click "Clear" to start a new conversation

### API Usage

#### Text Query Endpoint

```bash
POST http://localhost:5000/api/query
Content-Type: application/json

{
  "question": "What is Apple's revenue for 2024?",
  "chat_history": []
}
```

**Response:**
```json
{
  "answer": "Apple's revenue for 2024 was..."
}
```

#### Chart Endpoint

```bash
POST http://localhost:5000/api/chart
Content-Type: application/json

{
  "question": "Show me a chart of revenue trends",
  "chat_history": []
}
```

**Response:**
```json
{
  "image": "base64_encoded_image_string",
  "answer": "Chart generated successfully"
}
```

### Python API Usage (Direct)

```python
from dotenv import load_dotenv
load_dotenv()

from hybrid_graph_rag import chain

# Query the system
response = chain.invoke({
    "question": "Your question here",
    "chat_history": []
})

print(response)
```

## Example Queries 💭

### Text Queries
- 📈 "What is Apple's revenue for 2024?"
- ⚠️ "What are the main risks mentioned in the annual report?"
- 🌱 "What sustainability initiatives are mentioned?"
- 🌍 "What is the geographical revenue distribution?"
- 💰 "What is Apple's debt profile?"

### Chart Queries
- 📊 "Show me a chart of capital expenditure evolution"
- 📊 "Create a chart showing revenue trends"
- 📊 "Generate a chart of geographical revenue distribution"
- 📊 "Show me a chart of debt over time"

## Project Structure 📁

```
Hybrid-Graph-RAG-Financial-Analyser/
├── backend_api/              # FastAPI backend
│   ├── backend_api.py        # Main API server
│   └── hybrid_graph_rag.py   # RAG chain implementation
├── frontend/                 # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   ├── index.js         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Frontend dependencies
│   └── README.md            # Frontend documentation
├── Annual Report/           # Source documents
│   ├── NASDAQ_AAPL_2024_first_53_pages.pdf
│   └── NASDAQ_AAPL_2024.pdf
├── graph_documents.pkl     # Cached graph documents
├── hybrid_graph_rag.py     # Core RAG implementation
├── hybrid_graph_rag.ipynb  # Jupyter notebook
├── import_data.py          # Neo4j data import script
├── test_chart_generation.py # Chart testing utilities
├── verify_implementation.py # Verification scripts
├── .env_example            # Environment variables template
└── README.md               # This file
```

## API Endpoints 📡

### `GET /`
Health check endpoint.

**Response:**
```json
{"status": "Hybrid Graph RAG backend running successfully!"}
```

### `POST /api/query`
Text-based query endpoint.

**Request:**
```json
{
  "question": "string",
  "chat_history": [["user msg", "ai msg"], ...]
}
```

**Response:**
```json
{
  "answer": "string"
}
```

### `POST /api/chart`
Chart generation endpoint.

**Request:**
```json
{
  "question": "string (should contain 'chart')",
  "chat_history": []
}
```

**Response (Success):**
```json
{
  "image": "base64_encoded_string",
  "answer": "Chart generated successfully"
}
```

**Response (Error):**
```json
{
  "answer": "error message",
  "error": "error message",
  "image": null
}
```

## Best Practices 🌟

1. **Document Processing**: 📝
   - Use appropriate chunk sizes based on document content
   - Maintain overlap between chunks for context preservation

2. **Query Formation**: 🔍
   - Be specific with questions
   - Provide context when needed
   - Utilize chat history for follow-up questions
   - For charts, clearly specify what data to visualize

3. **System Maintenance**: ⚙️
   - Regularly update the knowledge graph
   - Monitor embedding quality
   - Validate response accuracy
   - Keep Neo4j database optimized

4. **Development**: 💻
   - Always start backend before frontend
   - Check backend logs for debugging
   - Use browser console (F12) for frontend debugging
   - Test chart generation with various query types

## Troubleshooting 🔧

### Backend Issues
- **Port 5000 already in use**: Change port in `backend_api.py` or kill the process using port 5000
- **Neo4j connection error**: Verify `.env` credentials and Neo4j instance status
- **Import errors**: Ensure all Python dependencies are installed

### Frontend Issues
- **Port 3000 already in use**: Close other React apps or change port in `package.json`
- **Cannot connect to backend**: Verify backend is running at `http://localhost:5000`
- **Module not found**: Run `npm install` in the frontend directory

### Chart Generation Issues
- **No chart generated**: Ensure query contains "chart" keyword
- **Insufficient data**: Try queries about data that exists in the annual report
- **Chart errors**: Check backend logs for detailed error messages

## Acknowledgments 🙏

- Neo4j team for graph database capabilities
- LangChain community for the framework
- HuggingFace for embeddings model
- FastAPI team for the web framework
- React team for the frontend framework
