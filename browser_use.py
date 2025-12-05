"""
Mock browser-use module for testing Streamlit UI.
Replace this with real browser-use once available.
"""

class BrowserProfile:
    def __init__(self, browser_session=None, user_data_dir=None, headless=False, 
                 executable_path=None, allowed_domains=None):
        self.browser_session = browser_session
        self.user_data_dir = user_data_dir
        self.headless = headless
        self.executable_path = executable_path
        self.allowed_domains = allowed_domains


class BrowserSession:
    def __init__(self, browser_profile=None):
        self.browser_profile = browser_profile


class Agent:
    def __init__(self, task=None, llm=None, sensitive_data=None, 
                 enable_memory=False, browser_session=None):
        self.task = task
        self.llm = llm
        self.sensitive_data = sensitive_data
        self.enable_memory = enable_memory
        self.browser_session = browser_session
    
    async def run(self, max_steps=100):
        """Mock agent run - returns sample expense total"""
        return {
            "status": "success",
            "total_expense": 1250.50,
            "message": "Successfully calculated total expense from Google Sheet",
            "steps_taken": 5
        }
    
    def create_history_gif(self):
        """Mock GIF creation"""
        pass
