import google.generativeai as genai
from typing import TypedDict

# Define structure for JSON output
class DialogueLine(TypedDict):
    speaker: str
    text: str

# Configure API and model
genai.configure(api_key="AIzaSyBVHQAc8W6WWJJl_XU-fx6IDAhbruhinWc")  # Replace with your actual API key

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite-preview-06-17"
)

# Generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 400,
    "stop_sequences": ["User:", "Assistant:"],
    "response_mime_type": "application/json",
    "response_schema": list[DialogueLine],
}

# ✅ Supported safety settings only
"""safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": 3},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": 3},
    {"category": "HARM_CATEGORY_SEXUAL", "threshold": 4},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": 3},
]
"""
print("Enter prompt ('exit' to quit):\n")

while True:
    prompt = input("User: ").strip()
    if prompt.lower() in ("exit", "quit"):
        break
    if not prompt:
        print("[Empty prompt. Please type something.]\n")
        continue

    try:
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            #safety_settings=safety_settings
        )
        print("\nJSON Output:", response.text)
    except Exception as e:
        print("Response:", getattr(response, 'text', '[No response]'))
        print("Error:", e)
