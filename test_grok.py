from openai import OpenAI

client = OpenAI(api_key="PASTE_YOUR_XAI_KEY_HERE", base_url="https://api.x.ai/v1")

response = client.chat.completions.create(
    model="grok-4", messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)
