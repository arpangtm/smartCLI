from openai import OpenAI
import time
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal
import json
from urllib3 import response
from nexcli.src.RAG import RAG_Search

load_dotenv()

import os

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

class question_answer_response(BaseModel):
    question_type: Literal["command", "general", "correction"] = Field(description="The type of question. 1. The command is a question about a terminal command or a command the user needs help with (command). 2. The command is a general question (general). 3. The command is a terminal command but the user is using it correctly (correction)")


def autocomplete_suggestion(prompt):

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout:free",
        messages=[
            {"role": "system", "content": "You are a terminal helper assistant. You help users complete terminal commands based on the characters they enter. Only provide the most likely command. Nothing else. Just the command and nothing else. No more than one line"},
            {
                "role": "user",
                "content": prompt
            }
        ],
        reasoning_effort="low"
    )

    return response.choices[0].message.content

def question_answer(prompt):
    fomatted_prompt = f"""{{error:"{prompt["error"]}", command:"{prompt["command"]}"}}"""
    response = client.beta.chat.completions.parse(
        model="meta-llama/llama-4-scout:free",
        messages=[
            {"role": "system", "content": f"""You are a terminal helper assistant. You help users with terminal questions. The user faced an error in terminal. You need to help them with the error. The prompt is in the format {{error:"Error given by the terminal", command:"Command by the user"}} Look at the command and categorize if:
            1. The command is a question about a terminal command or a command the user needs help with (command)
            2. The command is a general question (general)
            3. The command is a terminal command but the user is using it correctly (correction)
            """},
            {
                "role": "user",
                "content": fomatted_prompt
            }
        ],
        reasoning_effort="low",
        response_format= question_answer_response
    )
    if response.choices[0].message.parsed.question_type == "general":
        print("general question detected!")
        general_question_response =general_question(prompt["command"])
        return general_question_response
    elif response.choices[0].message.parsed.question_type == "command":
        print("command question detected!")
        command_question_response = command_question(prompt["command"])
        return command_question_response

    elif response.choices[0].message.parsed.question_type == "correction":
        print("command question detected!")
        correction_question_response = command_question(prompt["command"])
        return correction_question_response



def general_question(prompt):
    with open("config.json", "r") as f:
        config = json.load(f)
        if config["RAG"]["enabled"]:
            response = RAG_Search(prompt)
        else:
            prompt = f"""{{question:"{prompt}"}}"""
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout:free",
                messages=[
                    {"role": "system", "content": f"""
                    Answer in very short. Possibly 1-2 lines.
                    """},
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                reasoning_effort="low")
            response = response.choices[0].message.content
    return {"question_type":"general","answer":response}


def command_question(prompt):
    prompt = f"""{{question:"{prompt}"}}"""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout:free",
        messages=[
            {"role": "system", "content": f"""
            You are a terminal helper assistant. Help the user with a command. The command is either a typo or the user is asking for a command to do a specific thing. The answer should be only the command. Don't give any suggestions, just the command.
            """},
            {
                "role": "user",
                "content": prompt
            }
        ],
        reasoning_effort="low")
    command = response.choices[0].message.content.strip("`")
    return {"question_type":"command","answer":command}


