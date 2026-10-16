from openai import OpenAI
from core.config import settings
import requests
import json


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        
        if response.status_code == 200:
            return f"the weather in {city} is {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error getting response: {str(e)}"


tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "geth the weather condition of a location in realtime",
        "parameters":{
            "type": "object",
            "properties":{
                "city":{
                    "type": "string",
                    "description": "The city whose realtime weather condition is needed e.g Paris, London"
                }
            },
            "required": ["city"],
            "additionalProperties": False
        }
    }
]


print("="*50)
input_text = input("User😁 : ").strip()
input_list = [{"role": "user", "content": input_text}]
response = client.responses.create(
    model="gpt-5.4-mini",
    temperature=0,
    tools=tools,
    instructions="You are an AI assistant that answers users question",
    input=input_list,
    # include=["web_search_call.action.sources"]
)

input_list += response.output

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_weather":
            result = get_weather(**json.loads(item.arguments))
            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                }
            )
            

response = client.responses.create(
    model="gpt-5.4-mini",
    temperature=0,
    tools=tools,
    instructions="You are an AI assistant that answers users question",
    input=input_list,
    
)

print(f"\nModel🗣️ : {response.output}\n")



# for item in response.output:
#     print (f"\n{item}")