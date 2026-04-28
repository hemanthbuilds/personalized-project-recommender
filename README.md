# 🎯 Personalized Project Recommender

Research any company and get **3 tailored project ideas** that make you stand out in interviews.

The app searches company news, reads their engineering blog, and scans job postings — then uses GPT-4o to synthesize project ideas matched to what that company actually cares about.

## How it works

1. Searches latest company news & announcements via Apify
2. Reads their engineering blog
3. Scans job postings for tech stack signals
4. GPT-4o synthesizes 3 tailored project ideas

## Setup (local)

### 1. Clone the repo
```bash
git clone https://github.com/hemanthbuilds/personalized-project-recommender.git
cd personalized-project-recommender
```

### 2. Create your `.env` file
```bash
cp .env.example .env
```
Then open `.env` and fill in your keys:
```
OPENAI_API_KEY=sk-...
APIFY_API_TOKEN=apify_api_...
```

Get your keys here:
- OpenAI: https://platform.openai.com/api-keys
- Apify: https://console.apify.com/account/integrations

### 3. Install dependencies
```bash
pip install uv       # if you don't have uv
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.
