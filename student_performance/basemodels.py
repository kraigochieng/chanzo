from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_text_input: str
    user_id: str


class ChatResponse(BaseModel):
    response: str
