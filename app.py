import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os

os.environ["PYTHONIOENCODING"] = "utf-8"
# --- Page Configuration ---
st.set_page_config(
    page_title="CP Analysis Suite", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Top Anchor for Back-to-Top Navigation ---
st.markdown("<div id='top-anchor' style='scroll-margin-top: 100px;'></div>", unsafe_allow_html=True)

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* --- Stop UI Dimming During Backend Processing --- */
    [data-testid="stApp"] div {
        opacity: 1 !important;
        transition: none !important;
    }
    
    /* Base Theme */
    .stApp {
        background-color: #0D1117;
        color: #C9D1D9;
    }
    
    /* Panel Headers with Red Left-Accent */
    h3 {
        border-left: 5px solid #D32F2F;
        padding-left: 12px !important;
        color: #FFFFFF !important;
        background-color: #161B22;
        padding-top: 8px !important;
        padding-bottom: 8px !important;
        border-radius: 0px 6px 6px 0px;
        font-size: 1.3rem !important;
        margin-bottom: 20px !important;
    }
    
    /* --- Fix for Invisible "Apply" Text --- */
    [data-testid="stCustomComponentV1"] div, iframe + div {
        color: #8B949E !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* --- Hide 'Press Enter to apply' in text inputs --- */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    
    /* --- Button & Link Styling --- */
    .nav-btn, .back-to-top, .stButton>button {
        display: inline-block;
        text-align: center;
        text-decoration: none;
        border-radius: 6px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #8B0000 0%, #D32F2F 50%, #E57373 100%);
        border: 1px solid #5C0000 !important;
        transition: all 0.3s ease;
    }
    
    .nav-btn:hover, .back-to-top:hover, .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4);
        background: linear-gradient(135deg, #990000 0%, #E53935 50%, #EF9A9A 100%);
        color: #FFFFFF !important;
    }
    
    /* Specific overrides for layout positioning */
    .nav-btn {
        position: absolute;
        top: 15px;
        right: 15px;
        padding: 8px 16px;
        font-size: 14px;
        z-index: 9999;
    }
    
    .back-to-top {
        width: 180px;
        margin: 40px auto 10px auto;
        padding: 10px;
    }
    
    .stButton>button {
        width: 100%;
        margin-top: 10px;
    }
    
    /* Table Styling for Documentation */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    th, td {
        border: 1px solid #30363D;
        padding: 12px;
        text-align: left;
    }
    th {
        background-color: #161B22;
        color: #58A6FF;
    }
    </style>
    
    <a href="#documentation" target="_self" class="nav-btn">Documentation ↓</a>
""", unsafe_allow_html=True)

# --- Header (Bulletproof SVG Image Render) ---
st.markdown("""
    <img data-darkreader-ignore="true" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='800' height='75'><defs><linearGradient id='g' x1='0%25' y1='0%25' x2='50%25' y2='0%25'><stop offset='0%25' stop-color='%23FFFFFF'/><stop offset='100%25' stop-color='%23FF4B4B'/></linearGradient></defs><text x='0' y='60' font-family='sans-serif' font-size='52' font-weight='900' fill='url(%23g)'>Neural Analysis Suite</text></svg>" style="filter: drop-shadow(0px 4px 10px rgba(255, 75, 75, 0.4)); margin-top: 10px; margin-bottom: -15px;" alt="Neural Analysis Suite">
    
    <div data-darkreader-ignore="true" style="color: #8B949E; font-size: 1.1rem; font-weight: 500; margin-bottom: 30px; letter-spacing: 0.5px;">
        Automated Static Analysis & Dynamic Edge-Case Verification
    </div>
""", unsafe_allow_html=True)
st.divider()

# --- Main Layout ---
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.subheader("Source Configuration")
    
    # --- Language Configuration Routing ---
    LANG_CONFIG = {
        "C++": {"file": "solution.cpp", "mode": "c_cpp", "default": "#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your C++ code here\n    return 0;\n}"},
        "Python": {"file": "solution.py", "mode": "python", "default": "def solve():\n    # Write your Python code here\n    pass\n\nif __name__ == '__main__':\n    solve()"},
        "Java": {"file": "Main.java", "mode": "java", "default": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        // Write your Java code here\n    }\n}"},
        "C": {"file": "solution.c", "mode": "c_cpp", "default": "#include <stdio.h>\n\nint main() {\n    // Write your C code here\n    return 0;\n}"},
        "Go": {"file": "solution.go", "mode": "golang", "default": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    // Write your Go code here\n}"},
        "Rust": {"file": "solution.rs", "mode": "rust", "default": "fn main() {\n    // Write your Rust code here\n}"}
    }
    
    selected_lang = st.selectbox("Select Language", list(LANG_CONFIG.keys()), label_visibility="collapsed")
    lang_data = LANG_CONFIG[selected_lang]
    target_file = lang_data["file"]
    
    # Load existing code or default boilerplate
    current_code = lang_data["default"]
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            current_code = f.read()

    source_code = st_ace(
        value=current_code,
        language=lang_data["mode"],
        theme="tomorrow_night",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        height=450,
        show_gutter=True,
        show_print_margin=False,
    )
    
    if st.button("Commit Source"):
        # Write the actual code file
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(source_code)
        
        # Write a hidden pointer file so the backend knows what to execute
        with open(".active_lang", "w", encoding="utf-8") as f:
            f.write(f"{selected_lang},{target_file}")
            
        st.toast(f"Source committed as {target_file}", icon="✅")

with col2:
    st.subheader("Execution Parameters")
    
    # --- Dynamic Scraper Integration ---
    st.markdown("<div style='color: #58A6FF; font-size: 1.1em; margin-top: 0px; margin-bottom: 5px;'>1. Target Problem</div>", unsafe_allow_html=True)
    
    current_problem = "No problem loaded."
    if os.path.exists("problem.json"):
        import json
        try:
            with open("problem.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                current_problem = f"Currently loaded: **{data.get('title', 'Unknown')}**"
        except:
            pass

    st.markdown(current_problem)
    
    url_col, btn_col = st.columns([3, 1])
    with url_col:
        cf_url = st.text_input("Codeforces URL", placeholder="https://codeforces.com/problemset/problem/...", label_visibility="collapsed")
    with btn_col:
        if st.button("Fetch"):
            if cf_url.strip() == "":
                st.error("Enter a URL")
            else:
                with st.spinner("Scraping..."):
                    result = subprocess.run(["python", "scraper.py", cf_url], capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        st.toast("Problem constraints updated!", icon="✅")
                        st.rerun() 
                    else:
                        st.error("Failed to scrape URL.")
                        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Execution Tabs ---
    tab1, tab2 = st.tabs(["AI Code Review", "Automated Stress Test"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True) 
        if st.button("Run AI Review"):
            with st.spinner("Analyzing logic and constraints..."):
                result = subprocess.run(["python", "explainer.py"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    out = result.stdout
                    if "AI COACH FEEDBACK:" in out:
                        clean_out = out.split("AI COACH FEEDBACK:")[1].replace("=", "").strip()
                        with st.container(border=True):
                            st.markdown(clean_out)
                    else:
                        st.text(out)
                else:
                    st.error("Analysis execution failed.")
                    st.code(result.stderr, language="bash")

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True) 
        if st.button("Run Stress Test"):
            with st.spinner("Compiling and generating boundary inputs..."):
                result = subprocess.run(["python", "runner.py"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    test_case = "N/A"
                    if os.path.exists("input.txt"):
                        with open("input.txt", "r") as f:
                            test_case = f.read()
                    
                    st.markdown("**Generated Edge Case**")
                    st.code(test_case, language="text")
                    
                    st.markdown("**Program Output**")
                    raw_out = result.stdout
                    if "PROGRAM OUTPUT:" in raw_out:
                        final_out = raw_out.split("PROGRAM OUTPUT:")[1].split("--------------------")[0].strip()
                        st.code(final_out, language="text")
                        
                        for line in raw_out.split('\n'):
                            if "Execution Time" in line:
                                st.caption(line.strip())
                    else:
                        st.text(raw_out)
                else:
                    st.error("System Crash Detected.")
                    with st.expander("View Stack Trace"):
                        st.code(result.stderr, language="bash")

st.divider()

# --- Documentation Section ---
st.markdown("<div id='documentation' style='scroll-margin-top: 50px;'></div>", unsafe_allow_html=True)
st.subheader("System Documentation")

with st.container(border=True):
    st.markdown("""
    ### 📖 What is this tool?
    Think of this app as your personal coding tutor and proofreader. 

    When solving competitive programming puzzles, it is incredibly easy to miss a tricky "edge case" (like what happens if an input is zero, negative, or a massive number). This app helps you find those blind spots before you submit your code.

    ---

    ### 💻 Step 1: Write Your Code (The Editor)
    This is where you write your solution. 
    1. **Pick your language** from the dropdown (Python, C++, Java, Go, C, or Rust).
    2. **Write or paste your code** into the dark editor box.
    3. **Save it:** Press `Ctrl + Enter` to apply your typing, and then click the red **Commit Source** button. *(You MUST click Commit Source before running any tests!)*

    ---

    ### 🧠 Step 2: AI Code Review
    * **What it does:** It acts like a senior programmer looking over your shoulder.
    * **How it works:** It reads the problem rules and looks at your code. It will gently point out logical mistakes or warn you if your code is too slow, but it **will not** just give you the exact answer. You still have to do the thinking!

    ---

    ### ⚡ Step 3: Automated Stress Test
    * **What it does:** It actively tries to break your code.
    * **How it works:** Instead of you manually typing in test numbers, the app's AI writes a custom script to generate random, super-hard trick questions based on the problem's rules. It feeds those numbers into your code to see if it crashes or takes too long to answer.

    ---

    ### 🛑 Troubleshooting Crashes
    If the Stress Test throws a red "System Crash" error, open the Stack Trace to see why. It usually happens for two reasons:
    1. **Typo:** You have a syntax error in your code (like a missing semicolon) so it couldn't run.
    2. **Infinite Loop:** Your code got stuck and took longer than 5 seconds to answer (Time Limit Exceeded).
    """)

# --- Back to Top Anchor ---
st.markdown("<a href='#top-anchor' target='_self' class='back-to-top'>↑ Return to Top</a>", unsafe_allow_html=True)