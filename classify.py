import json
import os
from datetime import datetime
import boto3

# --- Setup Bedrock Client ---
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# --- Load scraped data ---
with open("output/scraped_1754552868.json", "r", encoding="utf-8") as f:
    data = json.load(f)

categories = {}
model_id = "amazon.titan-text-express-v1"

# --- Define system prompt for classification ---
def build_prompt(page_text):
    return f"""
Classify the following web page into one of these categories:

- About Us
- Contact
- Team
- Research
- Services
- Tests
- Blog
- Other

Only respond with the category name.

PAGE TEXT:
{page_text[:3500]}
"""

# --- Classify each page ---
for url, text in data.items():
    if not text.strip():
        continue

    prompt = build_prompt(text)

    try:
        print(f"[CLASSIFYING] {url}")
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "temperature": 0.5,
                    "maxTokenCount": 100,
                    "stopSequences": [],
                    "topP": 0.9
                }
            })
        )

        result = json.loads(response["body"].read())
        categories[url] = result["results"][0]["outputText"].strip()

    except Exception as e:
        categories[url] = f"Error classifying: {str(e)}"

# --- Save output ---
os.makedirs("classified", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"classified/categories_{timestamp}.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(categories, f, indent=2, ensure_ascii=False)

print(f"\n Classification results saved to: {output_path}")
