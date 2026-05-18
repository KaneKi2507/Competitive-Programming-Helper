import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GENAI_API_KEY)

def analyze_cp_code(problem_data, cpp_code):
    system_instruction = """
    You are an elite Competitive Programming coach. Your goal is to help the user debug their code without just giving them the exact copied-and-pasted solution.
    
    You will be provided with:
    1. Problem Statement
    2. Input/Output Specifications8
    3. The User's Code
    
    Your Output MUST follow this exact structure:
    - **Bug Analysis**: Identify logical flaws or edge cases they missed.
    - **Complexity Analysis**: State the Big-O Time and Space complexity of their current code. Compare it against the problem's time limit and constraints to predict if it will get TLE.
    - **A Nudge**: Give a hint on how to fix it, but DO NOT write the complete corrected code.
    """

    user_prompt = f"""
    ### PROBLEM DATA ###
    Title: {problem_data.get('title', 'N/A')}
    Time Limit: {problem_data.get('time_limit', 'N/A')}
    Description: {problem_data.get('description', 'N/A')}
    Input Specs: {problem_data.get('input_specification', 'N/A')}
    Output Specs: {problem_data.get('output_specification', 'N/A')}

    ### MY CODE ###
    ```cpp\n{cpp_code}\n```
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(system_instruction=system_instruction)
            )
            return response.text
        except Exception as e:
            if attempt == max_retries - 1:
                return f"**API Error:** Failed after {max_retries} attempts. \n\nDetails: {str(e)}"
            time.sleep(2)

if __name__ == "__main__":
    try:
        # Load the problem data
        with open("problem.json", "r", encoding="utf-8") as f:
            scraped_data = json.load(f)
            
        # Check which language is active
        if not os.path.exists(".active_lang"):
            print("AI COACH FEEDBACK:\n❌ **Error:** No source code committed. Please click 'Commit Source' first.")
            exit(1)
            
        with open(".active_lang", "r", encoding="utf-8") as f:
            active_lang, target_file = f.read().strip().split(",")
            
        # Read the active code file
        with open(target_file, "r", encoding="utf-8") as f:
            my_code = f.read()
            
        # Prepend the language metadata to the prompt so the AI knows the context
        language_context = f"// Language: {active_lang}\n" + my_code
            
        feedback = analyze_cp_code(scraped_data, language_context)
        print("\nAI COACH FEEDBACK:")
        print(feedback)
        
    except Exception as e:
        print(f"File Error: {e}")