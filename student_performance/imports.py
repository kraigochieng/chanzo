import datetime
import json
import os
import sqlite3
from enum import Enum
from pprint import pprint
from typing import Annotated, List, TypedDict

import pandas as pd
import scipy
import torch
from dotenv import load_dotenv
from graphviz import Source
from IPython.display import Image, display
from langchain.callbacks.base import BaseCallbackHandler
from langchain.embeddings import init_embeddings
from langchain.prompts import PromptTemplate
from langchain_core.messages import (
    HumanMessage,
    RemoveMessage,
    SystemMessage,
    trim_messages,
)
from langchain_core.runnables import RunnableConfig
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore
from langmem import create_manage_memory_tool, create_search_memory_tool
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown
from sentence_transformers import SentenceTransformer
