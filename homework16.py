from openai import OpenAI
import requests

client = OpenAI()

def get_kaunas_wiki():
    response = requests.get(
        "https://en.wikipedia.org/wiki/Kaunas",
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
    return page["extract"]

tools = [{
    "type": "function",
    "function": {
        "name": "get_kaunas_info",
        "description": "Get information about Kaunas, Lithuania from Wikipedia",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Kaunas, Lithuania"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
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

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "What is the weather like in Paris today?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)