from agent import invoke_full_graph
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You should restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    user_input: str
    thread_id: str


@app.post("/chat")
async def ask_agent(request: ChatRequest):
    try:
        config = {
            "configurable": {"thread_id": request.thread_id},
        }

        result = invoke_full_graph(user_input=request.user_input, config=config)
        return JSONResponse(content={"response": result["messages"][-1].content})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while processing the request: {str(e)}"
            },
        )
