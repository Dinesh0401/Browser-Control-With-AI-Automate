import asyncio
import logging
from typing import Any
import sys

from config import get_config
from google_sheet_automation import run_google_sheet_automation

# Fix for Windows asyncio subprocess issue
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def _run_visible_automation() -> Any:
    """
    Run real browser automation with visible Chrome window.
    Shows all steps: navigation, login, scanning, calculating.
    """
    logger.info("🚀 Starting Visible Browser Automation...")
    
    try:
        config = get_config()
        logger.info(f"📝 Configuration loaded")
        logger.info(f"   Sheet URL: {config.base_url}")
        logger.info(f"   Email: {config.email if hasattr(config, 'email') else 'Not set'}")
        
        # Run visible browser automation
        result = await run_google_sheet_automation(
            sheet_url=config.base_url,
            email=config.email,
            password=config.password,
            headless=config.headless
        )
        
        logger.info(f"✅ Automation complete: {result}")
        return result
    
    except Exception as e:
        logger.error(f"❌ Automation failed: {e}", exc_info=True)
        raise


def run_agent_sync() -> Any:
    """
    Synchronous wrapper for Streamlit.
    Runs the async browser automation.
    """
    try:
        return asyncio.run(_run_visible_automation())
    except RuntimeError as e:
        # Handle case where event loop already exists
        logger.warning(f"Event loop issue: {e}, creating new loop...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(_run_visible_automation())
        finally:
            loop.close()
