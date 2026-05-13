import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_openai(prompt: str) -> str:
    """
    Runs OpenAI API with the given prompt.
    """
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0
    )
    return chat_completion.choices[0].message.content

def parse_po_text(first_page_text: str, remaining_pages_text: str) -> dict:
    """
    Sends PO text to OpenAI API and returns parsed JSON.
    """
    with open("prompt_template.txt", "r", encoding="utf-8") as f:
        template = f.read()

    # Create separate sections for clarity
    full_prompt = (
        f"{template}\n\n"
        f"---\n"
        f"FIRST PAGE RAW TEXT:\n{first_page_text}\n"
        f"---\n"
        f"REMAINING PAGES RAW TEXT:\n{remaining_pages_text}\n"
    )

    output = run_openai(full_prompt)

    # Extract JSON safely
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        cleaned = output[output.find("{"):output.rfind("}")+1]
        return json.loads(cleaned)
