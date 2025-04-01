#!/usr/bin/env python3

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter, FieldCondition, MatchValue
import uvicorn

# Initialize FastAPI
app = FastAPI()

# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load Qdrant client and embedding model
client = QdrantClient("localhost", port=6333)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
collection_name = "netbox_devices"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the HTML page with a search form.
    """
    return templates.TemplateResponse("index.html", {"request": request, "results": None})


@app.get("/search/")
async def search_devices(query: str, request: Request, top_k: int = 5, manufacturer: str = None):
    """
    API endpoint & UI search handler.

    :param query: Natural language query
    :param request: FastAPI request object
    :param top_k: Number of results to return
    :param manufacturer: Optional filter by manufacturer
    :return: Rendered HTML with search results
    """
    query_vector = model.encode(query).tolist()

    # Apply optional manufacturer filter
    query_filter = None
    if manufacturer:
        query_filter = Filter(
            must=[FieldCondition(key="manufacturer", match=MatchValue(value=manufacturer))]
        )

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        query_filter=query_filter
    )

    return templates.TemplateResponse("index.html", {"request": request, "results": [hit.payload for hit in results], "query": query})

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

