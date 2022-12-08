# wtl-graph
Persistence Micro-service to store and query events - geo-locations and relations

## prerequisites 
- Python 3+
- sqllite3
- FastAPI 
pip install fastapi
- optionally install uvicorn for local development
pip install "uvicorn[standard]"

## run
$ python create-db
$ uvicorn api:app
http://localhost:8000/docs
