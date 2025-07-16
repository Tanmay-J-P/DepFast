import google.generativeai as genai


# Step 1: Configure Gemini API
genai.configure(api_key="AIzaSyBVHQAc8W6WWJJl_XU-fx6IDAhbruhinWc")  # Replace with your API key

# Step 2: Define a simulated tool function
def get_weather(city: str) -> str:
    return f"The weather in {city} is 31°C and partly cloudy."

# Step 3: Declare the tool (function)
tools = [
    {
        "function_declarations": [
            {
                "name": "get_weather",
                "description": "Returns current weather by city name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    },
                    "required": ["city"]
                }
            }
        ]
    }
]

# Step 4: Create the model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite-preview-06-17"
)

# Step 5: Setup generation config
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 300,
}

# Step 6: Interactive loop
print("🔧 Gemini Function Calling Test (type 'exit' to quit)\n")

while True:
    user_input = input("User: ").strip()
    if user_input.lower() in ("exit", "quit"):
        break
    if not user_input:
        continue

    try:
        # First call: prompt Gemini to invoke a function if needed
        response = model.generate_content(
            user_input,
            tools=tools,
            generation_config=generation_config
        )

        for part in response.parts:
            # If a function call is triggered
            if hasattr(part, "function_call"):
                fn_call = part.function_call
                args = dict(fn_call.args)
                print(f"\n🔧 Function called: {fn_call.name}({args})")

                if fn_call.name == "get_weather":
                    tool_output = get_weather(args.get("city", "Unknown"))

                    # Second call: pass function result back to Gemini
                    final_response = model.generate_content(
                        contents=[
                            genai.Content(role="user", parts=[user_input]),
                            genai.Content(role="function", name=fn_call.name, parts=[tool_output])
                        ],
                        tools=tools
                    )

                    print("\n🤖 Gemini (after using tool):", final_response.text)
                break

            # Otherwise just regular reply
            elif hasattr(part, "text"):
                print("\n🤖 Gemini:", part.text)

    except Exception as e:
        print("[Error]:", e)
