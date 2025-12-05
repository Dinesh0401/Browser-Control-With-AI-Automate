import os
import streamlit as st
from dotenv import load_dotenv
import time
import json
import pandas as pd

from run import run_agent_sync

load_dotenv()

st.set_page_config(
    page_title="🤖 Google Sheet Expense Agent", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 Google Sheet Expense Calculator (AI Agent)")
st.markdown("""
This app uses **real browser automation** to:
- 🌐 **Open Chrome browser** (visible window)
- 📊 **Navigate to your Google Sheet** (live URL from .env)
- 🔐 **Log in automatically** (uses credentials from .env)
- 🔍 **Scan for 'cost' column** (shows process)
- 💰 **Calculate total expense** (sums all values)
- 📈 **Display results** (shows each value found)
""")

# Status indicator
st.markdown("---")
st.subheader("📋 Current Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    sheet_url = os.getenv("GOOGLE_SHEET_URL", "Not set")
    if sheet_url and sheet_url != "https://docs.google.com/spreadsheets/d/your_sheet_id_here/edit#gid=0":
        st.success("✅ Sheet URL: Configured")
        with st.expander("View Sheet URL"):
            st.code(sheet_url)
    else:
        st.warning("⚠️ Sheet URL: Not set")
        st.info("Please update `.env` with your Google Sheet URL")

with col2:
    email = os.getenv("MAIL_ID", "Not set")
    if email and email != "your_google_email@gmail.com":
        st.success("✅ Email: Configured")
    else:
        st.warning("⚠️ Email: Not set")

with col3:
    password = os.getenv("MAIL_PASSWORD", "Not set")
    if password and password != "your_google_password_or_app_password":
        st.success("✅ Password: Configured")
    else:
        st.warning("⚠️ Password: Not set")

st.markdown("---")

# Configuration details
with st.expander("⚙️ Advanced Configuration", expanded=False):
    config_cols = st.columns(2)
    
    with config_cols[0]:
        st.write("**Email (for Google login):**")
        st.code(os.getenv("MAIL_ID", "Not set"))
        
        st.write("**Headless Mode:**")
        st.code(os.getenv("HEADLESS", "false"))
    
    with config_cols[1]:
        st.write("**Chrome Path:**")
        st.code(os.getenv("CHROME_PATH", "Not set"))
        
        st.write("**Model:**")
        st.code(os.getenv("GENAI_MODEL", "gemini-2.0-flash-exp"))

st.markdown("---")

# Quick link opener
st.subheader("🔗 Open Google Sheet in Browser")
st.write("Paste your Google Sheet URL below and click to open it in a new browser tab.")

sheet_link_input = st.text_input(
    "Google Sheet URL",
    value=os.getenv("GOOGLE_SHEET_URL", ""),
    placeholder="https://docs.google.com/spreadsheets/d/your_sheet_id/edit",
    help="Paste your Google Sheet link here"
)

col_open, col_save = st.columns([1, 1])

with col_open:
    if st.button("🌐 Open in Browser", use_container_width=True):
        if sheet_link_input and sheet_link_input.startswith("http"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url={sheet_link_input}" target="_blank">', unsafe_allow_html=True)
            st.success(f"✅ Opening: {sheet_link_input}")
            st.markdown(f"[Click here if it doesn't open automatically]({sheet_link_input})")
            # JavaScript to open in new window
            st.markdown(f"""
            <script>
                window.open('{sheet_link_input}', '_blank');
            </script>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Please enter a valid Google Sheet URL starting with 'http'")

with col_save:
    if st.button("💾 Save to .env", use_container_width=True):
        if sheet_link_input and sheet_link_input.startswith("http"):
            try:
                # Read current .env
                env_path = os.path.join(os.path.dirname(__file__), ".env")
                with open(env_path, "r") as f:
                    lines = f.readlines()
                
                # Update GOOGLE_SHEET_URL
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith("GOOGLE_SHEET_URL="):
                        lines[i] = f'GOOGLE_SHEET_URL="{sheet_link_input}"\n'
                        updated = True
                        break
                
                if not updated:
                    lines.append(f'\nGOOGLE_SHEET_URL="{sheet_link_input}"\n')
                
                # Write back
                with open(env_path, "w") as f:
                    f.writelines(lines)
                
                st.success("✅ URL saved to .env file!")
            except Exception as e:
                st.error(f"❌ Failed to save: {e}")
        else:
            st.error("❌ Please enter a valid URL")

st.markdown("---")

# Upload-based calculation (no browser)
st.subheader("📤 Upload a Sheet (CSV or Excel)")
st.write("Upload a local file and we will calculate the total from your 'cost' column—no browser automation required.")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"], accept_multiple_files=False)

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File loaded successfully. Preview below.")
        st.dataframe(df.head())

        # Detect cost column automatically
        cost_candidates = [c for c in df.columns if str(c).strip().lower() == "cost"]
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        default_cost_col = cost_candidates[0] if cost_candidates else (numeric_cols[0] if numeric_cols else None)

        cost_col = st.selectbox(
            "Select the cost column",
            options=df.columns,
            index=df.columns.get_loc(default_cost_col) if default_cost_col in df.columns else 0,
        ) if len(df.columns) else None

        if cost_col:
            # Coerce to numeric and drop NaNs
            cost_series = pd.to_numeric(df[cost_col], errors="coerce").dropna()
            values = cost_series.tolist()

            if not values:
                st.error("No numeric values found in the selected column.")
            else:
                total = sum(values)
                avg = total / len(values)
                max_val = max(values)

                st.markdown("---")
                st.subheader("📊 Upload Results")

                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Total", f"${total:,.2f}")
                with m2:
                    st.metric("Entries", len(values))
                with m3:
                    st.metric("Average", f"${avg:,.2f}")
                with m4:
                    st.metric("Max", f"${max_val:,.2f}")

                st.markdown("---")
                st.write("**All values found:**")
                st.dataframe(pd.DataFrame({"cost": values}))

    except Exception as e:
        st.error(f"Failed to process file: {e}")

# Divider before browser automation
st.markdown("---")

# Main action button
st.subheader("🚀 Launch Browser Automation")

col_button, col_info = st.columns([2, 3])

with col_button:
    run_button = st.button(
        "🚀 START AUTOMATION",
        key="run_button",
        help="Click to start - Chrome will open and navigate to your sheet",
        use_container_width=True
    )

with col_info:
    st.info("""
    **What happens:**
    1. Chrome opens (visible window)
    2. Navigates to your Sheet URL
    3. Logs in if needed
    4. Scans for 'cost' column
    5. Results display here
    """)

if run_button:
    st.markdown("---")
    
    # Create containers for different sections
    progress_container = st.container()
    status_container = st.container()
    result_container = st.container()
    debug_container = st.container()
    
    with progress_container:
        st.info("⏳ **Browser Automation Started...**")
        st.markdown("""
        **Process:**
        1. Opening Chrome browser (watch for window popup) 🌐
        2. Navigating to Google Sheet 📍
        3. Handling login (if needed) 🔐
        4. Waiting for page to load ⏱️
        5. Finding 'cost' column 🔍
        6. Reading all cost values 💰
        7. Calculating total 🧮
        """)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Update status
        status_text.write("**Status:** Starting automation...")
        progress_bar.progress(10)
        
        # Run the agent
        status_text.write("**Status:** Running browser automation (this may take 30-60 seconds)...")
        progress_bar.progress(50)
        
        result = run_agent_sync()
        
        # Update progress
        progress_bar.progress(100)
        status_text.write("**Status:** ✅ Automation completed successfully!")
        
        # Clear progress container and show results
        progress_container.empty()
        
        with status_container:
            st.success("✅ **Browser Automation Completed Successfully!**")
        
        # Display results
        with result_container:
            st.markdown("---")
            st.subheader("📊 Results")
            
            if isinstance(result, dict):
                # Status
                status = result.get("status", "unknown")
                if status == "success":
                    st.success(f"✅ Status: {status.upper()}")
                else:
                    st.error(f"❌ Status: {status.upper()}")
                
                # Main metric - Total Expense
                col_metric, col_details = st.columns([2, 2])
                
                with col_metric:
                    if "total_expense" in result:
                        total = result['total_expense']
                        st.metric(
                            "💰 Total Expense",
                            f"${total:,.2f}" if isinstance(total, (int, float)) else total
                        )
                
                with col_details:
                    if "message" in result:
                        st.write(f"**Message:** {result['message']}")
                    
                    if "count" in result:
                        st.write(f"**Entries Found:** {result['count']}")
                
                # Show all values found
                if "values_found" in result and result["values_found"]:
                    st.markdown("---")
                    st.subheader("💾 Individual Cost Values Found:")
                    
                    values_col1, values_col2, values_col3 = st.columns(3)
                    
                    for idx, value in enumerate(result["values_found"]):
                        with [values_col1, values_col2, values_col3][idx % 3]:
                            st.metric(f"Entry {idx + 1}", f"${value:.2f}")
                    
                    # Summary
                    st.markdown("---")
                    summary_col1, summary_col2, summary_col3 = st.columns(3)
                    with summary_col1:
                        st.metric("📈 Number of Entries", len(result["values_found"]))
                    with summary_col2:
                        if len(result["values_found"]) > 0:
                            avg = sum(result["values_found"]) / len(result["values_found"])
                            st.metric("📊 Average Cost", f"${avg:.2f}")
                    with summary_col3:
                        if len(result["values_found"]) > 0:
                            max_val = max(result["values_found"])
                            st.metric("⬆️ Highest Cost", f"${max_val:.2f}")
                
                # Debug info
                with debug_container:
                    with st.expander("🔧 Debug Info (Raw Result)"):
                        st.json(result)
            else:
                st.write(result)
    
    except Exception as e:
        status_container.empty()
        
        with status_container:
            st.error(f"❌ **Automation Failed**")
            st.error(f"Error: {str(e)}")
        
        with debug_container:
            st.error("**Please check:**")
            st.markdown("""
            - ✅ Chrome is installed on your system
            - ✅ `.env` file has correct credentials
            - ✅ Google Sheet URL is valid
            - ✅ Email and password are correct
            - ✅ Check terminal for detailed error logs
            """)

st.markdown("---")

# Help section
st.subheader("❓ Help & Setup")

help_col1, help_col2 = st.columns(2)

with help_col1:
    st.write("""
    **Before Running:**
    1. Edit `.env` file in project folder
    2. Add your Google Sheet URL
    3. Add your Google email (MAIL_ID)
    4. Add your password (MAIL_PASSWORD)
    5. Make sure Chrome is installed
    """)

with help_col2:
    st.write("""
    **What You'll See:**
    - Chrome browser opens automatically
    - Navigates to your Sheet URL
    - Shows login process (if needed)
    - Waits for page to load
    - Scans for 'cost' column
    - Shows all values found
    - Returns total calculation
    """)

st.markdown("---")
st.caption(
    "🔐 **Security:** Credentials stored locally in `.env`. Never uploaded. "
    "Browser automation runs on your machine. Read-only access to sheets."
)
