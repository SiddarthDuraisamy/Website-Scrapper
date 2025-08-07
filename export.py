import json
import csv
import os
from datetime import datetime

# Load files
with open("output/scraped_1754552868.json", "r", encoding="utf-8") as f:
    scraped = json.load(f)

with open("summaries/summary_20250807_141404.json", "r", encoding="utf-8") as f:
    summaries = json.load(f)

with open("classified/categories_20250807_141551.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

# Merge data
final_data = []
for url, content in scraped.items():
    summary = summaries.get(url, "N/A")
    category = categories.get(url, "Uncategorized")

    final_data.append({
        "url": url,
        "content": content,
        "summary": summary,
        "category": category
    })

# Save as CSV
csv_file = "final_output.csv"
with open(csv_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["url", "content", "summary", "category"])
    writer.writeheader()
    writer.writerows(final_data)

# Save as JSON
json_file = "final_output.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"Exported {len(final_data)} records to {csv_file} and {json_file}")
