# netbox-chatbot
Extract NetBox data, store it in a vector database, and enable interactive chat-based queries.

### Install the required dependencies
```pip3 install fastapi uvicorn qdrant-client sentence-transformers jinja2```

### Run Qdrant via docker
Install docker if not already installed
```bash
apt  install docker.io 
docker run -p 6333:6333 qdrant/qdrant
``` 
### Get the data from the netbox 
```python3 embed_data.py```

### Store the data in qdrant
```python3 store_in_qdrant.py```

### Start FastAPI server
```python3 app.py```

### Open in your browser
http://localhost:8000/

#### And now interact with the data, for example
* Who owns the system abc 
* Show all the system owned by user user1
* Show all network 1G switches
* Show all system from manufacture Hitachi
