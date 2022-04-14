#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


#Email-validator 
#from email_validator import validate_email


#FastAPI

from fastapi import FastAPI
from fastapi import Body , Query , Path ,Form , Header , Cookie , UploadFile , File 
from fastapi import status 
from fastapi import HTTPException

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str


class PersonBase(BaseModel):
    
    first_name:str = Field(
        ...,
        min_Length = 1,
        max_Length = 50,
        example = "Miguel"
    )
    last_name:str = Field (
        ...,
        min_Length =0,
        max_Length = 115,
        example = "Reyes Novoa"


    )
    age:int = Field (
        ...,
        gt = 0,
        le = 115,
        example = 25

    ) 

    hair_color:Optional[HairColor] = Field (default = None,example ="black")
    is_married:Optional[bool] = Field(default =None, example=False)

class Person(PersonBase):
    
    password: str = Field(..., min_length = 8)

class personOut(PersonBase):
    pass

class loginOut(BaseModel):
    username: str = Field(..., max_length = 20, example = "santiago2123" )

#    class Config:
#       schema_extra = {
#            "example":{
#                "first_name": "Santiago",
#                "last_name": "",
#                "age": 21,
#                "hair_color": "brown",
#                "is_married": False

 #           }
                




  #      }



@app.get(
    path = "/" ,
    status_code = status.HTTP_200_OK,
    tags = ["Home"] 
    )
def home():
    return {"Hello" : "World"}

# Request and response body

@app.post(
    path = "/person/new",
    response_model = personOut,
    status_code = status.HTTP_201_CREATED,
    tags = ["Persons"],
    summary =  "Create Person in the app"
    )


def create_person(person:Person = Body(...)):
    """
    Create Person 

    This path operation creates a person in the app and save the information in the database

    parameters:
    - request body parameter:
    
        -**person: Person -> A person model with first name, age , hair color and marital status**

    Returns a person model with first name, last name, age, hair color and marital status

    """
    return person 

#Validations :Query Parameters


@app.get(
    path = "/person/detail",
    status_code = status.HTTP_200_OK,
    tags = ["Persons"] 
    
    )

def show_person(
    name: Optional[str] =   Query(
        None,
        min_Length = 1,
        max_length=50,
        title = "Person Name",
        description = "This is the person name. It's between 1 and 50 characters",
        example = "Rocio"

        ),
    age: str = Query(
        ...,
        title="Person Age",
        description = "This is the person age.It's required",
        example="25"
        )
):

    return {name: age}


# Validations : Path Parameters 

persons = [1, 2, 3, 4, 5]



@app.get(
    path = "/person/detail/{person_id}",
    status_code = status.HTTP_200_OK,
    tags = ["Persons"]
    
    
    
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example = 123
    )
        
):
    if person_id not in persons :
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "¡This person doesn't exist!"

        )
    return {person_id: "It exists!"}

# Validations : Request Body


@app.put(
    path = "/person/{person_id}",
    status_code = status.HTTP_200_OK,
    tags = ["Persons"] 
    )
def update_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        description = "This is the person ID",
        gt = 0,
        example = 123

    ),
    person: Person = Body (...),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict())
    #return results 
    return person

    #forms 

@app.post(
    path = "/login",
    response_model = loginOut,
    status_code = status.HTTP_200_OK,
    tags = ["Persons"] 
)

def login(username: str = Form(...), password: str = Form(...)):
    return loginOut(username = username ) 

    #cookies and headers parammeters

@app.post(
    path= "/contact",
    status_code = status.HTTP_200_OK,
    tags = ["Cookies and Files"] 
)
def contact(
    first_name:str = Form(
        ...,
        max_length = 20,
        min_length = 1 
    
    ),
    last_name:str = Form(
        ...,
        max_length = 20,
        min_length = 1 
    
    ),
    email:  EmailStr = Form(...),
    message: str = Form (
        ...,
        min_length = 20

    ),
    user_agent: Optional [str] = Header(default= None ),
    ads : Optional[str] = Cookie(default=None) 
):
    return user_agent

#files 

@app.post (
    path = "/post-image",
    tags = ["Cookies and Files"]     
)
def post_image(
    image: UploadFile = File(...) 
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024,ndigits = 3 )

        }



