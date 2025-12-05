# 🤖 Google Sheet Expense Calculator - AI Browser Agent

An intelligent browser automation agent that uses **Playwright** and **Google's Gemini LLM** to automatically:
- 🌐 Open a Google Sheet in a visible browser
- 🔐 Log in to your Google account
- 📊 Read and analyze expense data from the sheet
- 🧮 Calculate total expenses using AI
- ✅ Return results through a beautiful Streamlit interface

**Key Features:**
- Real browser automation with Playwright (visible mode)
- AI-powered data extraction using Gemini 2.0
- User-friendly Streamlit web interface
- Configurable via environment variables
- Windows-compatible with asyncio fixes

## 📁 Project Structure

```text
Browser-Ai-Agent/
├── streamlit_app.py              # Main Streamlit web UI
├── run.py                        # Orchestrator with Windows asyncio fix
├── google_sheet_automation.py    # Playwright browser automation
├── config.py                     # Configuration management
├── browser_use.py                # Browser-use integration (optional)
├── agent_builder.py              # AI agent builder
├── google-login.py               # CLI entry point
├── .env                          # Environment variables (NOT in git)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Setup & Installation

### Prerequisites
- Python 3.10+
- Google Chrome browser installed
- Google account with access to the target spreadsheet

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/Dinesh0401/Browser-Ai-Agent.git
cd Browser-Ai-Agent
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium
```

4. **Configure environment variables:**

Create a `.env` file in the project root:

```env
# LLM Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GENAI_MODEL=gemini-2.0-flash-exp

# Google Account Credentials
MAIL_ID=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Google Sheet URL
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0

# Chrome Configuration
CHROME_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
HEADLESS=false
```

**Important:** 
- Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- For `MAIL_PASSWORD`, use a [Google App Password](https://support.google.com/accounts/answer/185833), not your regular password
- Replace `YOUR_SHEET_ID` with your actual Google Sheet ID from the URL

## 🚀 Running the Application

### Option 1: Streamlit Web UI (Recommended)

Run the interactive web interface:

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

**Features:**
- 🎨 Clean, intuitive interface
- 📊 Real-time progress tracking
- 🔍 View automation steps in the browser
- 📈 Display results with formatted expense totals

### Option 2: Command Line

Run directly from terminal:

```bash
python google-login.py
```

## 🐛 Troubleshooting

### Windows AsyncIO Issue (Fixed!)
If you see `NotImplementedError` related to asyncio subprocesses, this has been fixed in `run.py` by setting:
```python
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

### Common Issues:
1. **Browser doesn't launch**: Check `CHROME_PATH` in `.env`
2. **Login fails**: Verify credentials and use App Password for Google
3. **Sheet not accessible**: Ensure the Google account has access to the sheet
4. **Playwright errors**: Run `playwright install chromium`

## ☁️ Deployment Considerations

### Local Deployment (Best for Development)
✅ **Works perfectly** when:
- Chrome/Chromium is installed
- `CHROME_PATH` is correctly configured
- `.env` variables are set properly
- Running on Windows/Linux/Mac with display support

### Cloud Deployment Options

#### 1. **Streamlit Cloud** ⚠️
- Requires Chromium installation via `packages.txt`
- May have limitations with browser automation
- Consider using headless mode (`HEADLESS=true`)
- Network access and performance may vary

#### 2. **Self-Hosted VM (Recommended for Production)** ✅
Deploy on AWS EC2, DigitalOcean, Azure, etc.:
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver

# Set environment variables
export CHROME_PATH=/usr/bin/chromium-browser
export HEADLESS=true

# Run the app
streamlit run streamlit_app.py --server.port 8501
```

#### 3. **Docker Deployment** 🐳
Consider containerizing with a Chromium-enabled base image:
```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y chromium chromium-driver
# ... rest of your Dockerfile
```

### Production Architecture Recommendation

For enterprise-grade deployment:
1. **Frontend**: Streamlit UI (lightweight)
2. **Backend**: FastAPI service running the automation
3. **Queue**: Redis/Celery for async job processing
4. **Monitoring**: Logging and error tracking

## 🔐 Security Notes

- **Never commit `.env` file** to git (already in `.gitignore`)
- Use **Google App Passwords**, not your main password
- Rotate API keys regularly
- Use environment variable injection in production
- Limit Google Sheet access permissions

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Dinesh** - [GitHub Profile](https://github.com/Dinesh0401)

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [Google Gemini](https://ai.google.dev/) - LLM integration
- [Streamlit](https://streamlit.io/) - Web UI framework
- [Browser-Use](https://github.com/browser-use/browser-use) - Browser automation framework

---

**⭐ If you find this project helpful, please give it a star!**
