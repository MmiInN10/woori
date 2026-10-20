import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"],
)

#추가
q=input("질문을 입력해주세요 : ")

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1:novita",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message)