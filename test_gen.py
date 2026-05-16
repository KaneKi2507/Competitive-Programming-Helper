import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GENAI_API_KEY)

def create_test_generator(problem_data):
    system_instruction = """
    You are an expert Python developer writing scripts for competitive programming stress-testing.
    Your job is to read the Input Specification of a problem and write a standalone Python script that prints EXACTLY ONE random, valid test case to standard output.
    
    Rules for the Python script you generate:
    1. It must use the `random` module.
    2. It must strictly follow the constraints (e.g., if N is up to 10^5, generate N in that range).
    3. DO NOT output any markdown blocks (like ```python). 
    4. Output ONLY the raw Python code so it can be executed immediately.
    """

    user_prompt = f"""
    ### PROBLEM DATA ###
    Title: {problem_data.get('title', 'N/A')}
    Input Specs: {problem_data.get('input_specification', 'N/A')}
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(system_instruction=system_instruction)
            )
            code = response.text.replace("```python", "").replace("```", "").strip()
            return code
        except Exception as e:
            if attempt == max_retries - 1:
                return f"print('Error: AI generation failed. {str(e)}')"
            time.sleep(2)

if __name__ == "__main__":
    try:
        with open("problem.json", "r", encoding="utf-8") as f:
            scraped_data = json.load(f)

        generator_code = create_test_generator(scraped_data)
        
        with open("generate_input.py", "w", encoding="utf-8") as f:
            f.write(generator_code)
            
        print("SUCCESS")
    except Exception as e:
        print(f"Error: {e}")