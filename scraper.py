import requests
from bs4 import BeautifulSoup
import json
import sys

def get_cf_problem_data(url):
    print(f"Scraping: {url}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch page: {e}"}

    soup = BeautifulSoup(response.text, 'html.parser')
    problem_statement = soup.find('div', class_='problem-statement')

    if not problem_statement:
        return {"error": "Could not find the problem statement. Check the URL."}

    # Extracting specific blocks
    title = problem_statement.find('div', class_='title').text.strip()
    
    # Getting limits (Crucial for the AI to check O(N) vs O(N^2))
    time_limit = problem_statement.find('div', class_='time-limit').text.replace('time limit per test', '').strip()
    
    # Extracting the actual text sections
    # Codeforces structures these in specific divs
    description_divs = problem_statement.find_all('div', class_=False, recursive=False)
    description = "\n".join([p.text for p in description_divs]).strip()
    
    input_spec = problem_statement.find('div', class_='input-specification')
    input_text = input_spec.text.replace('Input', '').strip() if input_spec else ""
    
    output_spec = problem_statement.find('div', class_='output-specification')
    output_text = output_spec.text.replace('Output', '').strip() if output_spec else ""

    # Package it cleanly for the LLM
    problem_data = {
        "title": title,
        "time_limit": time_limit,
        "description": description,
        "input_specification": input_text,
        "output_specification": output_text
    }
    
    return problem_data

# --- Test the Scraper ---
if __name__ == "__main__":
    # Check if a URL was passed via the command line
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        result = get_cf_problem_data(target_url)
        
        if "error" in result:
            print(result["error"])
            sys.exit(1)
            
        # Overwrite the problem.json file with the new data
        with open("problem.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
            
        print("SUCCESS")
    else:
        print("Error: No URL provided.")
        sys.exit(1)