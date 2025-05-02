import datetime
import logging
import os
import uuid
from contextlib import asynccontextmanager

from basemodels import ChatRequest, ChatResponse
from dependencies import get_chanzo_agent_db_session, get_chanzo_app_db_session
from dotenv import load_dotenv
from engines import chanzo_agent_db_engine
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from helper_functions import dict_to_message, message_to_dict
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from llm import llm
from models import Base, ChatMessage, ChatSession
from sessions import ChanzoAgentDbSession, ChanzoAppDbSession
from sqlalchemy import text
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables once before the app starts
    try:
        Base.metadata.create_all(chanzo_agent_db_engine)
    except Exception as e:
        logging.error(f"Error creating tables for Chanzo Agent: {e}")
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# history = [
#     SystemMessage(content="You are a helpful assistant."),
#     HumanMessage(content="How can I save money?"),
# ]

load_dotenv()


# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg.content)

# for chunk in llm.stream("Write me a 1 verse song about goldfish on the moon"):
#     print(chunk.content, end="", flush=True)


@app.get("/", status_code=status.HTTP_200_OK)
def root(chanzo_agent_db_session: Session = Depends(get_chanzo_agent_db_session)):
    return "agent api"


@app.post("/chat", status_code=status.HTTP_200_OK)
def chat(
    chat_request: ChatRequest,
    chanzo_agent_db_session_dependency: Session = Depends(get_chanzo_agent_db_session),
):
    messages_from_db = (
        chanzo_agent_db_session_dependency.query(ChatMessage)
        .filter(ChatMessage.user_id == chat_request.user_id)
        .all()
    )

    for message in messages_from_db:
        pass


# # Fetch latest chat history
# def get_user_chat_history(user_id: str, session: Session, limit=10):
#     return (
#         session.query(ChatMessage)
#         .join(ChatSession)
#         .filter(ChatSession.user_id == user_id)
#         .order_by(ChatMessage.timestamp.desc())
#         .limit(limit)
#         .all()
#     )


# async def stream_llm_response(prompt):
#     async def generator():
#         for chunk in llm.stream(prompt):
#             yield chunk["text"]

#     return StreamingResponse(generator(), media_type="text/plain")


# # messages = [
# #     {
# #         "role": "system",
# #         "content": "You are a helpful assistant for financial insights.",
# #     },
# #     *chat_history,
# #     {"role": "user", "content": current_prompt},
# # ]


# @app.post("/chat")
# async def chat(
#     user_id: str, prompt: str, db_session: Session = Depends(get_db_session)
# ):
#     chat_history = get_user_chat_history(user_id, db_session)
#     system_msg = {"role": "system", "content": "You're a financial advisor AI."}
#     messages = [system_msg] + chat_history + [{"role": "user", "content": prompt}]

#     # def token_stream():
#     #     for chunk in openai.ChatCompletion.create(
#     #         model="gpt-4", messages=messages, stream=True
#     #     ):
#     #         yield chunk["choices"][0].get("delta", {}).get("content", "")

#     # # Log user + assistant messages in DB
#     # save_user_message(user_id, prompt)
#     # return StreamingResponse(token_stream(), media_type="text/plain")
