# 🕸️ MCP Scraper

An end-to-end **Model-Callable Program (MCP)** server that recursively scrapes complete content from both static HTML and JavaScript-rendered websites using Selenium, then **summarizes**, **classifies**, and **exports** structured insights.

> Built for integration with AI Agents like Amazon Bedrock for deep website analysis.

---

## 🚀 Features

- ✅ **Recursive Web Crawler** with Selenium (supports JavaScript-rendered pages)
- 🧠 **Text Summarization** using Amazon Bedrock Titan model
- 🏷️ **Topic Classification** of pages (e.g., Home, About Us, Services)
- 📦 **Exports structured JSON & CSV** for downstream processing
- 🌐 **FastAPI Server** to make it callable from any LLM or agent

---

## 📂 Folder Structure

```
mcp_scraper/
│
├── main.py              # FastAPI MCP server with /scrape endpoint
├── post_main.py         # Utility if you extend to POST-based pipelines
├── classify.py          # Classifies pages into categories
├── summarize.py         # Summarizes page content using Bedrock
├── export.py            # Combines scraped + classified + summary into final output
│
├── chromedriver.exe     # Headless Chrome for Selenium
├── output/              # Raw scraped page content (JSON)
├── summaries/           # Summarized pages
├── classified/          # Topic-classified pages
│
├── final_output.json    # (generated) Full JSON mapping
├── final_output.csv     # (generated) Full CSV mapping
│
└── venv/                # Python virtual environment
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/mcp_scraper.git
cd mcp_scraper
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Create `requirements.txt` by running:

```bash
pip freeze > requirements.txt
```

---

## 🧪 Usage

### 🚦 Run the FastAPI Server

```bash
uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 📥 Scrape a Website

**GET** `/scrape?url=https://example.com`

Optional: Add `&limit=30` to limit the number of recursive links.

---

## 🧠 Pipeline Details

### 1. Scraping

- Headless Chrome via Selenium
- Extracts all links recursively from a homepage
- Supports dynamic JS websites

### 2. Summarization

- Uses Amazon Bedrock’s `titan-text-express-v1`
- Stored in `/summaries/`

### 3. Classification

- Rule-based classification (e.g., Home, About Us, Contact)
- Stored in `/classified/`

### 4. Export

- Merges all into:
  - `final_output.json`
  - `final_output.csv`

---

## 📌 Dependencies

- `selenium`
- `fastapi`
- `uvicorn`
- `openpyxl`
- `boto3` *(for Amazon Bedrock)*
- `pydantic`
- `jinja2` *(if used in future templates)*

---

## ☁️ AWS Usage

If you're using **Amazon Bedrock**:
- Make sure your environment has proper AWS credentials.
- The summarizer uses `boto3` to invoke Titan model via Bedrock.

---

## 🛠️ Next Steps (Optional)

- [ ] Add `/process` endpoint to auto-run full pipeline
- [ ] Deploy to AWS EC2, Fargate, or Lambda
- [ ] Connect to Bedrock Agent as a Tool
- [ ] Add UI dashboard with React or Streamlit

---

## 📄 License

MIT © [Your Name or Org]

---

## 🙋‍♂️ Contact

For issues, feature requests, or support, open an [issue](https://github.com/your-username/mcp_scraper/issues).
