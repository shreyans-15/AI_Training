from pydantic import BaseModel  #BaseModel is a class

class RequestFromAI(BaseModel):
    requestfromAI:str

class ResponseFromAI(BaseModel):
    responsefromAI:str