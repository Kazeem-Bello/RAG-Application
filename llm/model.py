from ollama import Client


client = Client(
    host="http://localhost:11434"
)





while True:
    input_text = input("Paste your prompt here:")
    print("="*30)
    
    response = client.chat(
        model="qwen2.5:3b",
        messages=[
            {"role": "user", "content": input_text}
        ]
    )

    print(response.message.content)
    print("="*30)
    
