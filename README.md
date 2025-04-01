# netbox-chatbot
Extract NetBox data, store it in a vector database, and enable interactive chat-based queries.

1) Install the required dependencies
pip3 install fastapi uvicorn qdrant-client sentence-transformers jinja2

2) Run Qdrant via docker
   (Install docker if not already installed)
apt  install docker.io 
docker run -p 6333:6333 qdrant/qdrant

3) Get the data from the netbox 
python embed_data.py

4) Store the data in qdrant
python store_in_qdrant.py

5) Start FastAPI server
python app.py

6) Open in your browser
http://localhost:8000/

And now interact with the data, for example
1) Who owns the system abc
2) Show all the system owned by user user1
3) Show all network 1G switches
4) Show all system from manufacture Hitachi
