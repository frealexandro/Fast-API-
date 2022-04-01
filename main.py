#Python 
from typing import Optional
from unittest.util import _MAX_LENGTH

#Pydantic
from pydantic import BaseModel



#FastAPI

from fastapi import FastAPI
from fastapi import Body , Query
app = FastAPI()

#Models

class Person(BaseModel):
    first_name:str
    last_name:str
    age:int
    hair_color:Optional[str] = None
    is_married:Optional[bool] = None


@app.get("/")
def home():
    return {"Hello" : "World"}

# Request and response body

@app.post("/person/new")
def create_person(person:Person = Body(...)):
    return person 

#Validations :Query Parameters

@app.get("/person/detail")

def show_person(
    name: Optional[str] =   Query(None, min_Length = 1, max_length=50),
    age: str = Query(...)
):

    return {name: age}


