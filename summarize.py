import boto3
import json
import os
from datetime import datetime

# --- Config ---
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "amazon.titan-text-express-v1"
INPUT_FILE = "output/scraped_1754552868.json"
OUTPUT_DIR = "summaries"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Helper Function ---
def summarize_text(text: str) -> str:
    prompt = f"Summarize the following webpage content:\n\n{text[:4000]}"
    body = json.dumps({
        "inputText": prompt
    })

    response = bedrock.invoke_model(
        body=body,
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body.get("results", [{}])[0].get("outputText", "").strip()

# --- Load scraped content ---
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    scraped_data = json.load(f)

summaries = {}

# --- Summarize each page ---
for url, page_text in scraped_data.items():
    if not page_text.strip():
        summaries[url] = "Skipped (Empty content)"
        continue

    print(f"[SUMMARIZING] {url}")
    try:
        summary = summarize_text(page_text)
        summaries[url] = summary
    except Exception as e:
        summaries[url] = f"Error summarizing: {str(e)}"

# --- Save summaries ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(OUTPUT_DIR, f"summary_{timestamp}.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(summaries, f, indent=2, ensure_ascii=False)

print(f"\nSummaries saved to: {output_path}")
