import sqlite3
from fastapi import FastAPI, Request, Response
from dataSetLocator.IDataSetLocator import DataLocator

app = FastAPI()


@app.get("/")
async def root(request: Request, response: Response):        
    return {"message": "API Docs can be accessed at " + request.base_url.__str__() + "docs"}

@app.get("/Domains")
async def domains():
    datafile = DataLocator.get_db_connection(None);
    conn = sqlite3.connect(datafile);
    c = conn.cursor()
    c.execute(" SELECT * FROM Domain ")
    results = c.fetchall();    
    c.close();
    return {"Domains": results}


@app.get("/Subjects")
async def subjects():
    datafile = DataLocator.get_db_connection(None);
    conn = sqlite3.connect(datafile);
    c = conn.cursor()
    c.execute(" SELECT * FROM Subject ")
    results = c.fetchall();    
    c.close();
    return {"Subjects": results}


@app.get("/Timeline")
async def timeline():
    datafile = DataLocator.get_db_connection(None);
    conn = sqlite3.connect(datafile);
    c = conn.cursor()
    c.execute(" SELECT * FROM Occurance ")
    results = c.fetchall();    
    c.close();
    return {"Occurances": results}
