from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str

class User(BaseModel):
    email: str
