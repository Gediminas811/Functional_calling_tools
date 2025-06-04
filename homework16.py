from openai import OpenAI
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SECRET")  # Replace with your actual token
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

client = OpenAI(
        base_url=endpoint,
        api_key=token,
)

def get_kaunas_wiki():
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": "Kaunas"
        }
    )
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    return [page["extract"]]

tools = [{
    "type": "function",
    "function": {
        "name": "get_kaunas_info",
        "description": "You are a helpful assistant. Get information from Wikipedia about Kaunas, located in Lithuania.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The user question or search query. For example, 'Where is Kaunas situated?'"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        
        "strict": True
    }
}]

question = input("Enter your question about Kaunas: ")

completion = client.chat.completions.create(
    model="openai/gpt-4.1-nano",
    messages=[{"role": "system", "content": "You are a helpful assistant. You will answer questions about Kaunas using Wikipedia."},
        {"role": "user", "content": question}],
    tools=tools #type: ignore
)

tool_calls = completion.choices[0].message.tool_calls
result = None
messages = []

# if tool_calls:
    # Call your function and print the result
result = get_kaunas_wiki()
# print(result) 
messages.append(completion.choices[0].message)  # append model's function call message
messages.append({                               # append result message
    "role": "tool",
    "tool_call_id": tool_calls[0].id if tool_calls else None,
    "content": str(result)
})

completion_2 = client.chat.completions.create(
    model="openai/gpt-4.1-nano",
    messages=messages,
    tools=tools, #type: ignore
)
print(completion_2.choices[0].message.content)
# else:
    # print(completion.choices[0].message.content)