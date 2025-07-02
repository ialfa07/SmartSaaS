from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from openai_client import generate_text
from auth import fake_auth, users_db
from models import PromptRequest, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(prompt: PromptRequest, user: User = Depends(fake_auth)):
    if users_db[user.email]["credits"] <= 0:
        raise HTTPException(status_code=403, detail="Not enough credits")
    response = generate_text(prompt.prompt)
    users_db[user.email]["credits"] -= 1
    return {"result": response, "credits_left": users_db[user.email]["credits"]}
