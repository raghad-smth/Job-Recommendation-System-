# ------------------ Loading the pdf into a string text ------------------
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(path): 
    loader = PyMuPDFLoader(path)
    docs = loader.load()
    text = " ".join([d.page_content for d in docs])
    return text

# ------------------ Loading API key for OpenRouter ------------------
from dotenv import load_dotenv
import os 

load_dotenv()
OPEN_ROUTER_API_Key=os.getenv("OPEN_ROUTER_API")
