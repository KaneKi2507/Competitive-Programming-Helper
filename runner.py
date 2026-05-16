import subprocess
import time
import os

def run_pipeline():
    print("="*40)
    print("STARTING STRESS-TEST PIPELINE")
    print("="*40)

    print("\n[1/4] Compiling solution.cpp...")
    compile_process = subprocess.run(
        ["g++", "solution.cpp", "-o", "solution.exe"], 
        capture_output=True, text=True
    )
    
    if compile_process.returncode != 0:
        print("[ERROR] Compilation Failed!")
        print(compile_process.stderr)
        return
    print("[SUCCESS] Compiled successfully.")

    # --- THE FIX: Tell the AI to write a NEW generator for the new problem ---
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

    print("\n[4/4] Executing solution.exe...")
    start_time = time.time()
    
    run_process = subprocess.run(
        ["solution.exe"], 
        input=test_case, 
        capture_output=True, text=True
    )
    
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

if __name__ == "__main__":
    run_pipeline()