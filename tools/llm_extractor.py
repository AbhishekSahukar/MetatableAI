import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-chat-v3"
LLM_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://metatable.ai",
    "X-Title": "MetaTableAI"
}

def extract_parameters_from_text(text: str):
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in environment.")

    # Clean the input text
    cleaned_text = re.sub(r"\s{2,}", " ", text.strip())

    # Improved and focused prompt
    prompt = f"""
You are a precise table extraction assistant.

Extract structured parameter-value-context objects from the given technical document text.

Each object should contain:
- "parameter": a clear and concise label (prefer row label or nearby identifier)
- "value": the associated value (numeric or text)
- "context": the column name, section, or merged label it belongs to

Avoid repeating all column headers in parameters.
Avoid redundant or long phrases.

Example:
[
  {{
    "parameter": "Operating Voltage",
    "value": "230V",
    "context": "Electrical"
  }},
  {{
    "parameter": "Efficiency",
    "value": "92%",
    "context": "Performance"
  }}
]

Text:
\"""{cleaned_text[:3000]}\"""

JSON:
"""

    try:
        response = requests.post(
            LLM_URL,
            headers=HEADERS,
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        raw = response.json()
        content = raw["choices"][0]["message"]["content"]

        match = re.search(r"\[.*\]", content, re.DOTALL)
        if not match:
            raise ValueError("Could not find valid JSON block in output.")

        parsed = json.loads(match.group(0))

        # Save output
        with open("extracted_data.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)

        print(f"✅ Extracted {len(parsed)} parameter-value pairs. Saved to extracted_data.json")
        return parsed

    except Exception as e:
        print("⚠️ LLM Output parsing failed:", e)
        print("🔎 Raw response:", raw if 'content' not in locals() else content)
        return []
