import os
import logging

from config import GoogleSheetConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try importing real browser-use, fallback to mock
try:
    from browser_use import Agent
    from browser_use.browser import BrowserProfile, BrowserSession
    BROWSER_USE_AVAILABLE = True
    logger.info("✅ Real browser-use package detected")
except ImportError:
    BROWSER_USE_AVAILABLE = False
    logger.warning("⚠️ browser-use not available, using mock")
    
    class BrowserProfile:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class BrowserSession:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class Agent:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
        
        async def run(self, max_steps=100):
            return {
                "status": "success (mock)",
                "total_expense": 1250.50,
                "message": "Mock: Successfully calculated total expense",
            }
        
        def create_history_gif(self):
            pass

# Try importing Gemini LLM, fallback to mock
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    class ChatGoogleGenerativeAI:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)


def create_google_sheet_agent(config: GoogleSheetConfig) -> Agent:
    """
    Create and return a browser-use Agent configured
    to log into Google Sheets and calculate total cost.
    
    This agent will:
    - Open your default Chrome browser
    - Navigate to the Google Sheet URL
    - Log in to your Google account
    - Find the "cost" column
    - Sum all expense values
    - Return the total
    """

    llm = ChatGoogleGenerativeAI(
        model=config.model,
        temperature=0.7,
        max_completion_tokens=1000,
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    browser_profile = BrowserProfile(
        browser_session="~/.config/google-chrome/Default",
        user_data_dir="~/.config/google-chrome/Default",
        headless=config.headless,
        executable_path=config.chrome_path,
        allowed_domains=["docs.google.com", "sheets.google.com"],
    )

    browser_session = BrowserSession(browser_profile=browser_profile)

    task = f"""
Navigate to the Google Sheet and calculate the total expense from the "cost" column.

Sheet URL: {config.base_url}

DETAILED STEPS:
1. Open the provided Google Sheet URL in the browser
2. If prompted to sign in, use the provided Google credentials
3. If 2-step verification is required, wait for manual verification
4. Wait for the spreadsheet to fully load (see all data rows)
5. Locate the column with the header "cost"
6. Read all numerical values in the "cost" column
7. Calculate the sum of all cost values
8. Return the result as: "Total expense: $XXX.XX" plus the numeric value

INTERACTION RULES:
- Always wait 2+ seconds for pages to load after navigation
- Do NOT click any buttons that could modify the sheet
- Do NOT add rows or change any data
- If a cell appears empty, skip it and continue reading
- Scroll down if needed to see all data rows

EXAMPLE OUTPUT:
"Total expense: $450.00"
"""

    agent = Agent(
        task=task,
        llm=llm,
        sensitive_data={
            "google_email": os.environ.get("MAIL_ID"),
            "google_password": os.environ.get("MAIL_PASSWORD"),
        },
        enable_memory=False,
        browser_session=browser_session,
    )

    return agent
