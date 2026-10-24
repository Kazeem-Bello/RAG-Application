from openai import OpenAI
from core.config import settings
import requests
import json


client = OpenAI(api_key=settings.OPENAI_API_KEY)

previous_conversation = None


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        
        if response.status_code == 200:
            return f"the weather in {city} is {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error getting response: {str(e)}"
    
    
def get_metal_price(metal_symbol: str):
    try:
        response = requests.get(f"https://api.gold-api.com/price/{metal_symbol}")
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            if data is None:
                return f"Could not retrieve the price for {metal_symbol}"
            return data.get("price")
    except requests.exceptions.RequestException as e:
        return f"Error getting response: {str(e)}"
             

tools = [
    {
        "type": "function",
        "name": "get_metal_price",
        "description": "geth the current price of special metals",
        "parameters":{
            "type": "object",
            "properties":{
                "metal_symbol":{
                    "type": "string",
                    "description": "The symbol of the metal whose price is needed e.g Gold is XAU, Silver is XAG"
                }
            },
            "required": ["metal_symbol"],
            "additionalProperties": False
        }
    },
    
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


while True:
    print("="*50)
    input_text = input("User😁 : ").strip()
    if input_text.lower() == "exit":
        break
    messages = [{"role": "user", "content": input_text}]
    response = client.responses.create(
        model="gpt-5.4-mini",
        temperature=0,
        tools=tools,
        instructions="You are an AI assistant that answers users question",
        input=messages,
        previous_response_id=previous_conversation
    )

    # print(f"\nModel🗣️ : {response.output_text}")
    function_output = []
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_weather":
                result = get_weather(**json.loads(item.arguments))
                function_output.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })
            if item.name ==   "get_metal_price":
                result = get_metal_price(**json.loads(item.arguments))     
                function_output.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(result)
                    }
                )
    if function_output:    
        response = client.responses.create(
            model="gpt-5.4-mini",
            tools=tools,
            temperature=0,
            instructions="You are an AI assistant that answers users question",
            input=function_output,
            previous_response_id=response.id
        )
    
    previous_conversation =response.id
    print(f"\nModel🗣️ : {response.output_text}")








# while True:
#     print("="*50)
#     input_text = input("User😁 : ").strip()
#     if input_text.lower() == "exit":
#         break
#     response = client.responses.create(
#         model="gpt-5.4-mini",
#         temperature=0,
#         instructions="You are an AI assistant that answers users question",
#         input=input_text + previous_conversation
#     )
#     previous_conversation += response.output_text
#     print(f"\nModel🗣️ : {response.output_text}")