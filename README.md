# Google Sheet Expense Agent (browser-use + Gemini)

This project uses the `browser-use` agent and Google's Gemini LLM to:
- Open a Google Sheet in the browser
- Log in to your Google account
- Read the "cost" column
- Calculate the total expense
- Return the total to the user

## 📁 Project Structure

```text
Browser-Ai-Agent/
├── google-login.py       # CLI entry
├── config.py             # Configuration dataclass + loader
├── agent_builder.py      # Creates browser-use Agent
├── run.py                # Shared runner logic
├── streamlit_app.py      # Streamlit UI (for deployment)
├── .env                  # Environment variables (NOT committed)
├── requirements.txt
└── README.md
```

## 🔧 Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root (already provided with Gemini API key):

```env
GEMINI_API_KEY=your_key_here
MAIL_ID=your_email_here
MAIL_PASSWORD=your_password_here
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/...
CHROME_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
HEADLESS=false
```

4. Run from the terminal:

```bash
python google-login.py
```

## 🌐 Streamlit UI

Run locally:

```bash
streamlit run streamlit_app.py
```

For deployment (e.g., Streamlit Cloud):

* Push this repo to GitHub.
* On Streamlit Cloud, create a new app pointing to `streamlit_app.py`.
* Make sure to set the same environment variables in the Streamlit Cloud UI.
* Note: `browser-use` requires a real Chrome/Chromium binary. On fully managed Streamlit hosting this may be limited or require extra configuration. For guaranteed stability, deploy on your own VM/server where you can install Chrome.

## 🚀 About Streamlit Deployment (Important Reality Check)

* **Locally**: this will work as long as:
  * Chrome/Chromium is installed,
  * `CHROME_PATH` is correct,
  * `.env` is set properly.

* **On Streamlit Cloud**:
  * `browser-use` needs a real Chrome/Chromium binary.
  * Streamlit Cloud is a restricted Linux environment; you *might* need an extra `packages.txt` to install `chromium` + `chromium-driver`, and set `CHROME_PATH` accordingly.
  * Even then, full browser automation can be flaky on managed platforms.

**Best architecture (clean way):**

* Use **Streamlit** as UI.
* Run this agent on:
  * your own VM (EC2, Linode, etc.), or
  * your own machine via `ngrok`.
* Streamlit app calls the backend via an API.

For a production-grade setup, consider adding a **FastAPI backend** for the agent with Streamlit calling it via HTTP.
