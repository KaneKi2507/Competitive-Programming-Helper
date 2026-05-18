import subprocess
import time
import os
import sys

def get_execution_commands(lang, filename):
    # Returns (compile_command, run_command)
    if lang == "C++":
        return (["g++", filename, "-o", "solution.exe"], ["solution.exe"])
    elif lang == "C":
        return (["gcc", filename, "-o", "solution.exe"], ["solution.exe"])
    elif lang == "Python":
        return (None, ["python", filename])
    elif lang == "Java":
        return (["javac", filename], ["java", "Main"])
    elif lang == "Go":
        return (["go", "build", "-o", "solution.exe", filename], ["solution.exe"])
    elif lang == "Rust":
        return (["rustc", filename, "-o", "solution.exe"], ["solution.exe"])
    return (None, None)

def run_pipeline():
    print("="*40)
    print("STARTING DYNAMIC STRESS-TEST PIPELINE")
    print("="*40)

    # 1. Read the active language
    if not os.path.exists(".active_lang"):
        print("[ERROR] No committed source file found. Please click 'Commit Source' on the UI.")
        return
        
    with open(".active_lang", "r", encoding="utf-8") as f:
        lang, filename = f.read().strip().split(",")

    print(f"\n[1/4] Preparing execution environment for {lang} ({filename})...")
    compile_cmd, run_cmd = get_execution_commands(lang, filename)

    # 2. Compile if necessary
    if compile_cmd:
        compile_process = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_process.returncode != 0:
            print(f"[ERROR] {lang} Compilation Failed!")
            print(compile_process.stderr)
            return
        print("[SUCCESS] Compiled successfully.")
    else:
        print("[INFO] Interpreted language. Skipping compilation.")

    # 3. Generate Test Case (Uses existing test_gen.py)
    print("\n[2/4] Requesting AI to write new test generator...")
    regen_process = subprocess.run(["python", "test_gen.py"], capture_output=True, text=True)
    if regen_process.returncode != 0 or not os.path.exists("generate_input.py"):
        print("[ERROR] Failed to write new test generator!")
        print(regen_process.stderr)
        return
    print("[SUCCESS] New generator written.")

    print("\n[3/4] Generating random test case...")
    gen_process = subprocess.run(["python", "generate_input.py"], capture_output=True, text=True)
    if gen_process.returncode != 0:
        print("[ERROR] Test Generator Crashed!")
        print(gen_process.stderr)
        return
        
    test_case = gen_process.stdout.strip()
    with open("input.txt", "w") as f:
        f.write(test_case)
    print(f"[SUCCESS] Input generated and saved to input.txt:\n{test_case}")

    # 4. Execute the actual code
    print(f"\n[4/4] Executing {lang} code...")
    start_time = time.time()
    
    try:
        run_process = subprocess.run(run_cmd, input=test_case, capture_output=True, text=True, timeout=5.0) # Added 5-second timeout to prevent infinite loops
        end_time = time.time()
        execution_time = end_time - start_time
        
        if run_process.returncode != 0:
            print("[ERROR] Execution crashed (Runtime Error)!")
            print(run_process.stderr)
        else:
            print("\n" + "-"*20)
            print("PROGRAM OUTPUT:")
            print(run_process.stdout.strip())
            print("-"*20)
            print(f"Execution Time: {execution_time:.5f} seconds")
            
    except subprocess.TimeoutExpired:
        print("\n[ERROR] Output Time Limit Exceeded (TLE)! Code took longer than 5.0 seconds to execute.")

if __name__ == "__main__":
    run_pipeline()