import subprocess

# Run pytest
result = subprocess.run(["pytest", "-v"])

# Check if pytest passed
if result.returncode != 0:
    print("Tests failed!")
    exit(1)
