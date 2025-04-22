from typing import Generator

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph_core.graph import StateGraph  # or wherever your graph builder is
from pydantic import BaseModel

# Your imports
from your_existing_module import CHECKPOINTS_DB, graph_builder  # adjust this

app = FastAPI()


# Input schema
class QueryRequest(BaseModel):
    query: str
    user_id: str


# Streaming callback handler
class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.queue = []

    def on_llm_new_token(self, token: str, **kwargs):
        self.queue.append(token)

    def get_stream(self) -> Generator[str, None, None]:
        while self.queue:
            yield self.queue.pop(0)


@app.post("/ask/stream")
def ask_stream(request: QueryRequest):
    user_input = request.query
    thread_id = request.user_id
    callback_handler = StreamingCallbackHandler()

    def token_stream():
        graph_input = {
            "messages": [
                SystemMessage(
                    content="""
                    You are an AI assistant helping parents assess their child’s academic performance...
                    (Insert your long context here)
                    """
                ),
                HumanMessage(user_input),
            ],
        }

        config = {
            "configurable": {"thread_id": thread_id},
            "callbacks": [callback_handler],
        }

        with SqliteSaver.from_conn_string(CHECKPOINTS_DB) as checkpointer:
            graph = graph_builder.compile(checkpointer=checkpointer)
            graph.invoke(input=graph_input, config=config)

        # Yield the tokens as they come in
        yield from callback_handler.get_stream()

    return StreamingResponse(token_stream(), media_type="text/plain")
