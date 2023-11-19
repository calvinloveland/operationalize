import subprocess

# Run pytest
result = subprocess.run(["pytest", "-v", "-s", "--cov=src", "--cov-report=term-missing"])

# Check if pytest passed
if result.returncode != 0:
    print("Tests failed!")
    exit(1)