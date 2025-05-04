from typing import Union

from langchain.schema import AIMessage, HumanMessage, SystemMessage


def message_to_dict(msg: Union[AIMessage, HumanMessage, SystemMessage]):
    # Convert the message object into a dictionary
    msg_dict = {
        "id": msg.id,
        "name": msg.name,
        "type": msg.type,
        "content": msg.content,
        "additional_kwargs": msg.additional_kwargs,
        "response_metadata": msg.response_metadata,
    }

    return msg_dict


def dict_to_message(d):
    id = d["id"]
    d_type = d["type"]
    content = d["content"]
    name = d["name"]
    response_metadata = d["response_metadata"]
    additional_kwargs = d["additional_kwargs"]

    if d["type"] == "system":
        message = SystemMessage(
            id=id,
            type=d_type,
            name=name,
            content=content,
            response_metadata=response_metadata,
            additional_kwargs=additional_kwargs,
        )
    elif d["type"] == "user":
        message = HumanMessage(
            id=id,
            type=d_type,
            name=name,
            content=content,
            response_metadata=response_metadata,
            additional_kwargs=additional_kwargs,
        )
    elif d["type"] == "assistant":
        message = AIMessage(
            id=id,
            type=d_type,
            name=name,
            content=content,
            response_metadata=response_metadata,
            additional_kwargs=additional_kwargs,
        )
    else:
        raise ValueError(f"Unknown role: {d['type']}")

    return message
