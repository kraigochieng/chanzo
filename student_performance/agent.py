import datetime
import os
import sqlite3
import sys

import pandas as pd
import scipy
from dotenv import load_dotenv
from dummy_data_for_agent import (
    strand_grade_prob_df_for_specific_student,
    student_names,
    subject_grade_prob_df_for_specific_student,
    subject_strand_percentile_for_specific_student_df,
)
from graph_state import State
from IPython.display import Image, display
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langmem import create_manage_memory_tool, create_search_memory_tool
from rich.console import Console
from rich.markdown import Markdown

# Environment Variables
load_dotenv()

CHECKPOINTS_DB = os.getenv("CHECKPOINTS_DB")

CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_NAME = os.getenv(
    "CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_NAME"
)
CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_USER = os.getenv(
    "CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_USER"
)
CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_PASSWORD = os.getenv(
    "CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_PASSWORD"
)
CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_HOST = os.getenv(
    "CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_HOST"
)
CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_PORT = os.getenv(
    "CHANZO_STUDENT_PERFORMANCE_LONG_TERM_MEMORY_DB_PORT"
)


deepseek_model = "deepseek-chat"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY

llm = ChatDeepSeek(model=deepseek_model)


# Initialize Graph Builder
graph_builder = StateGraph(State)

# Tools
tools = [
    create_manage_memory_tool(namespace=("memories",)),
    create_search_memory_tool(namespace=("memories",)),
]


# Define Nodes
def chatbot(state: State):
    llm_with_tools = llm.bind_tools(tools)
    messages = [llm_with_tools.invoke(state["messages"])]

    return {"messages": messages}


tool_node = ToolNode(tools=tools)


# Nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

# Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)


# Short-Term Memory


# Memory Place
# It is used with a with block
conn = sqlite3.connect(CHECKPOINTS_DB)

# ## Streaming


def invoke_full_graph(user_input: str, config: dict) -> State:
    # prompt_with_examples = few_shot_prompt.format(input=user_input)

    strand_prob_table = strand_grade_prob_df_for_specific_student.to_markdown(
        index=False
    )
    subject_prob_table = subject_grade_prob_df_for_specific_student.to_markdown(
        index=False
    )
    percentile_table = subject_strand_percentile_for_specific_student_df.to_markdown(
        index=False
    )
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.%f %Z"
    )

    graph_input = {
        "messages": [
            # prompt_with_examples,
            SystemMessage(f"""
            Persona: You are an advisor helping parents with questions about their children
            
            General Tone of Response:
            - Easy to digest for the parents
            - Be informative but concise
            - Very simple english
            - Encourage the parent
            - Do not start the respnse with a title header. Talk like a human. Do not start with 'Here is what I think'
                          
            For any question outside of these areas, respond with: "I cannot answer that question, it is out of my scope."
                          
            You will be responding with specific feedback based on the following information:
            - Grades: Numeric scores ranging from 1 to 5.
            - Percentile of grades: Relative performance in comparison to peers.

            Key Points to Remember:
            - Student-specific responses: Provide feedback based on the individual student’s performance.
            - Response to non-existent students: If a student does not exist in the data, respond with: "name does not exist".

            Question Scope:
            - Strengths and weaknesses of a student in a particular subject and/or subject strand.
                - For a subject, tell them to focus/maintain on a particular subject strand
            - The most probable grade a student will achieve in a subject and/or subject strand based on their data.
                - For this I know there are students who highly excel in a subject, others who perform poorly and others who perform average. Then they are 
            - Career recommendations based on the student's academic strengths and interests.
                - Specify courses and why
                - Specify job options
                - Be modern in your responses with the current state of the job market
                - Talk about salary ranges as per today
                - Show the progression from junior to senior positions in the career
                - Talk about entrepreneurship in the career
                - State the disadvantages of the career

            
            

            
            
            Below is the student(s) academic performance table that includes you will be referencing:

            {percentile_table}

            Below is the student(s) grades per subject together with the probability of getting that grade you will also be referencing:

            {subject_prob_table}
            
            Below is the student(s) grades per subject strand together with the probability of getting that grade you will also be referencing:

            {strand_prob_table}

            Time Reference:
            Please ensure all responses include the current date and time in UTC:
            Current time: {current_time}
        """),
            HumanMessage(user_input),
        ],
    }

    with SqliteSaver.from_conn_string(CHECKPOINTS_DB) as checkpointer:
        graph = graph_builder.compile(checkpointer=checkpointer)

        result = graph.invoke(input=graph_input, config=config)

    return result


# ## Configs


# The thread id will be for a different users
# config_1 = {"configurable": {"thread_id": "1"}}
# config_2 = {"configurable": {"thread_id": "2"}}


# ## Prompts
#
# The prompts are best understood sequentially


# ### Most possible grades in subject
#


# result = invoke_full_graph(
#     user_input=f"Tell me the most possible grades for each subject for {student_names[0]}",
#     config=config_1,
# )

# console = Console()
# md = Markdown(result["messages"][-1].content)
# console.print(md)


# ### Strengths and weaknesses of student
#


# result = invoke_full_graph(
#     user_input=f"Tell me the strengths and weaknesses of my child {student_names[0]}",
#     config=config_1,
# )

# console = Console()
# md = Markdown(result["messages"][-1].content)
# console.print(md)


# ### Career recommendations
#


# result = invoke_full_graph(
#     user_input=f"Recommend a career path for {student_names[0]}", config=config_1
# )

# console = Console()
# md = Markdown(result["messages"][-1].content)
# console.print(md)


# ### Unnecessary question
#


# result = invoke_full_graph(
#     user_input="What is the capital of Nairobi?", config=config_1
# )

# console = Console()
# md = Markdown(result["messages"][-1].content)
# console.print(md)


# ### Child who does not exist
#


# result = invoke_full_graph(user_input="Get output for Ochieng?", config=config_1)

# console = Console()
# md = Markdown(result["messages"][-1].content)
# console.print(md)


# ### Testing the memory
#


# result = invoke_full_graph(
#     user_input="Tell me everything we have talked about before", config=config_1
# )

# console = Console()
# md = Markdown(result["messages"][-1].content)
# console.print(md)


# ### Testing the scope of memory


# result = invoke_full_graph(
#     user_input="Tell me everything we have talked about before", config=config_2
# )

# console = Console()
# md = Markdown(result["messages"][-1].content)
# console.print(md)


# # What was done
#
# 1. Improved prompt engineering
# 2. Added more sample prompts
# 3. Short term memory complete. Each user has their scope


# # Way-forward
#
# 1. Deciding _what_ to store in long-term memory
# 2. Do we actually need the long-term memory?
#     - My reason for thinking this is that the short term memory stores the chats exactly, and this is what we needed
#     - This type of memory is mostly used to store facts, which I see are already part of the existing DB
# 3. How to stream resources
# 4. How to prevent unnecessary questions from reaching the agent
# 5. Start combining agent with frontend
# 6. Filter unnecessary questions beforehand
#     - As suggested by David last week
#     - Based on research, this will use an LLM specified for text classification. I feel this will be double work. We just use the current model
# 7. Make the first SystemMessage to be shown twice
#


# # Ideas
#
# 1. Tell users not to put passwords, credit card information or any other personal information.
# 2. Limit the text characters to 128 for a question...
#
