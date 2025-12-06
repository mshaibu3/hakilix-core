import os

# 1. Create the hidden GitHub directory structure
workflow_dir = os.path.join(".github", "workflows")
os.makedirs(workflow_dir, exist_ok=True)

# 2. Create the CI Workflow File
yaml_content = """
name: Hakilix Core CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        
    - name: Run Unit Tests
      run: |
        python -m unittest discover tests
"""

# 3. Write the file
file_path = os.path.join(workflow_dir, "test.yml")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(yaml_content)

print(f"✅ CI Workflow created at: {file_path}")
print("👉 Next Step: Run 'git add .', 'git commit', and 'git push'.")
print("👉 GitHub will now automatically test your code in the cloud.")