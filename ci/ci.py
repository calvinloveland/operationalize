import subprocess

# Run pytest
result = subprocess.run(["pytest", "-v"])

# Check if pytest passed
if result.returncode != 0:
    print("Tests failed!")
    exit(1)
    
# Run prospector
result = subprocess.run(["prospector"])
if result.returncode != 0:
    print("Prospector found issues!")
    exit(1)

# Run black
result = subprocess.run(["black", "--check", "."])
if result.returncode != 0:
    print("Black found formatting issues!")
    exit(1)