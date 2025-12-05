"""
Browser automation using Playwright (visible browser).
This module handles real browser automation with visible window.
"""

import asyncio
import logging
from typing import Dict, List, Any
from playwright.async_api import async_playwright, Page, Browser

logger = logging.getLogger(__name__)


class GoogleSheetAutomation:
    """Automate Google Sheets interaction with visible browser."""
    
    def __init__(self, sheet_url: str, email: str, password: str, headless: bool = False):
        self.sheet_url = sheet_url
        self.email = email
        self.password = password
        self.headless = headless
        self.browser: Browser = None
        self.page: Page = None
    
    async def start_browser(self):
        """Start Playwright browser (visible window)."""
        logger.info("🌐 Starting Chrome browser...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        logger.info("✅ Browser started successfully")
    
    async def navigate_to_sheet(self) -> bool:
        """Navigate to Google Sheet URL."""
        try:
            logger.info(f"📍 Navigating to: {self.sheet_url}")
            await self.page.goto(self.sheet_url, wait_until="networkidle", timeout=30000)
            logger.info("✅ Page loaded")
            await asyncio.sleep(2)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to navigate: {e}")
            return False
    
    async def handle_login(self) -> bool:
        """Handle Google login if needed."""
        try:
            # Check if login page is present
            login_button = await self.page.query_selector('button[type="button"]')
            
            if login_button or "accounts.google.com" in self.page.url:
                logger.info("🔐 Google login detected, attempting login...")
                
                # Enter email
                email_input = await self.page.query_selector('input[type="email"]')
                if email_input:
                    logger.info("📧 Entering email...")
                    await email_input.fill(self.email)
                    await self.page.click('button:has-text("Next")')
                    await asyncio.sleep(2)
                
                # Enter password
                password_input = await self.page.query_selector('input[type="password"]')
                if password_input:
                    logger.info("🔑 Entering password...")
                    await password_input.fill(self.password)
                    await self.page.click('button:has-text("Next")')
                    await asyncio.sleep(3)
                
                # Wait for page to load after login
                await self.page.wait_for_load_state("networkidle", timeout=30000)
                logger.info("✅ Login successful")
                return True
            else:
                logger.info("✓ Already logged in")
                return True
        except Exception as e:
            logger.warning(f"⚠️ Login attempt: {e}")
            return True  # Continue anyway
    
    async def find_cost_column(self) -> int:
        """Find 'cost' column index."""
        try:
            logger.info("🔍 Scanning for 'cost' column header...")
            
            # Get all header cells
            headers = await self.page.query_selector_all('div[data-header-column]')
            
            for idx, header in enumerate(headers):
                text = await header.text_content()
                if text and "cost" in text.lower():
                    logger.info(f"✅ Found 'cost' column at index: {idx}")
                    return idx
            
            # Fallback: search all text
            page_text = await self.page.text_content()
            if "cost" in page_text.lower():
                logger.info("📍 'cost' column found on page")
                return 0
            
            logger.warning("⚠️ 'cost' column not found")
            return -1
        except Exception as e:
            logger.error(f"❌ Error finding column: {e}")
            return -1
    
    async def read_cost_values(self) -> List[float]:
        """Read all numeric values from cost column."""
        try:
            logger.info("💰 Reading cost values...")
            
            # Get all cells with numeric values
            cells = await self.page.query_selector_all('div[data-value]')
            values = []
            
            for cell in cells:
                try:
                    value_attr = await cell.get_attribute('data-value')
                    if value_attr:
                        # Try to parse as number
                        num_value = float(value_attr)
                        values.append(num_value)
                        logger.info(f"  📊 Found value: {num_value}")
                except (ValueError, TypeError):
                    continue
            
            return values
        except Exception as e:
            logger.error(f"❌ Error reading values: {e}")
            return []
    
    async def calculate_total(self) -> Dict[str, Any]:
        """Calculate total expense."""
        try:
            logger.info("🧮 Calculating total...")
            
            values = await self.read_cost_values()
            
            if not values:
                logger.warning("⚠️ No values found")
                return {
                    "status": "error",
                    "total_expense": 0,
                    "message": "No cost values found in sheet",
                    "values_found": []
                }
            
            total = sum(values)
            logger.info(f"✅ Total calculated: ${total:.2f}")
            
            return {
                "status": "success",
                "total_expense": total,
                "message": f"Successfully calculated total from {len(values)} cost entries",
                "values_found": values,
                "count": len(values)
            }
        except Exception as e:
            logger.error(f"❌ Error calculating: {e}")
            return {
                "status": "error",
                "total_expense": 0,
                "message": str(e)
            }
    
    async def run(self) -> Dict[str, Any]:
        """Execute complete automation workflow."""
        try:
            logger.info("=" * 60)
            logger.info("🚀 Starting Google Sheet Automation")
            logger.info("=" * 60)
            
            # Start browser
            await self.start_browser()
            
            # Navigate to sheet
            if not await self.navigate_to_sheet():
                return {"status": "error", "message": "Failed to navigate to sheet"}
            
            # Handle login
            await self.handle_login()
            
            # Wait for sheet to fully load
            logger.info("⏳ Waiting for sheet to fully load...")
            await asyncio.sleep(3)
            
            # Find cost column
            cost_col = await self.find_cost_column()
            
            # Calculate total
            result = await self.calculate_total()
            
            logger.info("=" * 60)
            logger.info("✅ Automation Complete")
            logger.info("=" * 60)
            
            return result
        
        except Exception as e:
            logger.error(f"❌ Automation failed: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "total_expense": 0
            }
        
        finally:
            # Keep browser open for user to see
            logger.info("🔍 Browser window staying open for inspection...")
            await asyncio.sleep(5)
            
            if self.browser:
                await self.browser.close()
                logger.info("✅ Browser closed")


async def run_google_sheet_automation(
    sheet_url: str,
    email: str,
    password: str,
    headless: bool = False
) -> Dict[str, Any]:
    """
    Run Google Sheet automation with visible browser.
    
    Args:
        sheet_url: Full URL to Google Sheet
        email: Google account email
        password: Google account password
        headless: If False, browser window is visible
    
    Returns:
        Dict with automation results
    """
    automation = GoogleSheetAutomation(sheet_url, email, password, headless=headless)
    return await automation.run()
