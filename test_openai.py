from openai import OpenAI

api_key = "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"

client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)