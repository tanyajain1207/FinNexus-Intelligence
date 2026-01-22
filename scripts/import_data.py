"""
Script to import graph documents into Neo4j database.
Run this script once after setting up Neo4j Desktop to import the graph data.
"""

from dotenv import load_dotenv
import os
import pickle
from langchain_neo4j import Neo4jGraph
# HuggingFaceEmbeddings import moved to where it's used to avoid PyTorch DLL issues
from langchain_neo4j import Neo4jVector

# Load environment variables
load_dotenv()

print("=" * 60)
print("Neo4j Graph Data Import Script")
print("=" * 60)

# Connect to Neo4j
print("\n[1/4] Connecting to Neo4j...")
try:
    kg = Neo4jGraph(
        url=os.environ["NEO4J_URI"],
        username=os.environ["NEO4J_USERNAME"],
        password=os.environ["NEO4J_PASSWORD"],
    )
    print(" Connected to Neo4j successfully!")
except Exception as e:
    print(f" Error connecting to Neo4j: {e}")
    print("\nPlease check:")
    print("  1. Neo4j Desktop is running")
    print("  2. Your database is started (green 'Running' status)")
    print("  3. .env file has correct NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD")
    exit(1)

# Load graph documents from pickle file
print("\n[2/4] Loading graph documents from graph_documents.pkl...")
try:
    with open("graph_documents.pkl", "rb") as f:
        graph_documents = pickle.load(f)
    print(f" Loaded {len(graph_documents)} graph documents.")
except FileNotFoundError:
    print(" Error: graph_documents.pkl file not found!")
    print("\nPlease make sure graph_documents.pkl is in the same folder as this script.")
    exit(1)
except Exception as e:
    print(f" Error loading graph documents: {e}")
    exit(1)

# Import graph documents into Neo4j
print("\n[3/4] Importing graph documents into Neo4j...")
print("   This may take 5-10 minutes. Please wait...")
try:
    kg.add_graph_documents(
        graph_documents,
        include_source=True,
        baseEntityLabel=True,
    )
    print(" Graph documents imported successfully!")
except Exception as e:
    print(f" Error importing graph documents: {e}")
    exit(1)

# Create vector index
print("\n[4/4] Creating vector index...")
print("   This may take a few minutes. Please wait...")
try:
    # Import here to avoid PyTorch DLL issues at startup
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}

    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    vector_index = Neo4jVector.from_existing_graph(
        hf,
        search_type="hybrid",
        node_label="Document",
        text_node_properties=["text"],
        embedding_node_property="embedding",
    )
    print(" Vector index created successfully!")
except OSError as e:
    if "DLL" in str(e) or "WinError 1114" in str(e):
        print(f" Error: PyTorch DLL loading failed!")
        print("\nThis is a known issue with Python 3.13 and PyTorch.")
        print("\nTry these solutions:")
        print("  1. Install Visual C++ Redistributable:")
        print("     https://aka.ms/vs/17/release/vc_    redist.x64.exe")
        print("  2. Restart your computer after installing")
        print("  3. Try PyTorch nightly build:")
        print("     python -m pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu")
        print("\nOr use Python 3.10 or 3.11 instead of 3.13.")
    else:
        print(f" Error creating vector index: {e}")
        print("   You may need to install: python -m pip install sentence-transformers")
    exit(1)
except Exception as e:
    print(f" Error creating vector index: {e}")
    print("   You may need to install: python -m pip install sentence-transformers")
    exit(1)

print("\n" + "=" * 60)
print(" SETUP COMPLETE!")
print("=" * 60)
print("\nYour Neo4j database is ready to use.")
print("You can now start the backend and frontend servers.")
print("\nNext steps:")
print("  1. Open Terminal 1: cd backend_api && python backend_api.py")
print("  2. Open Terminal 2: cd frontend && npm install && npm start")
print("\n" + "=" * 60)

