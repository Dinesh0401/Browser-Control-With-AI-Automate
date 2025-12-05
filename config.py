from dataclasses import dataclass
import os


@dataclass
class GoogleSheetConfig:
    """Configuration for reading from Google Sheets via browser automation."""
    chrome_path: str
    headless: bool
    model: str
    base_url: str
    email: str
    password: str


def get_config() -> GoogleSheetConfig:
    """
    Build config from environment variables (with sensible defaults).
    """
    return GoogleSheetConfig(
        chrome_path=os.getenv("CHROME_PATH", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
        headless=os.getenv("HEADLESS", "false").lower() == "true",
        model=os.getenv("GENAI_MODEL", "gemini-2.0-flash-exp"),
        base_url=os.getenv(
            "GOOGLE_SHEET_URL",
            "https://docs.google.com/spreadsheets/d/REPLACE_ME/edit#gid=0",
        ),
        email=os.getenv("MAIL_ID", ""),
        password=os.getenv("MAIL_PASSWORD", ""),
    )
