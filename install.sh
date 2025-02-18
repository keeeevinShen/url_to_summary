#!/bin/bash
# 1️⃣ Step 1: Set Up Virtual Environment
echo "Creating a virtual environment..."
python3 -m venv env
# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source env/bin/activate

# 2️⃣ Step 2: Install Python Dependencies
echo " Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3️⃣ Step 3: Install Playwright Browsers
echo " Installing Playwright browsers..."
playwright install

# 5️⃣ Step 5: Download LLM Model (llama3)
echo " Downloading the LLM model (llama3)..."
ollama run llama3.1

brew install python-tk


# 7️⃣ Deactivate virtual environment after completion
deactivate
echo " Installation complete!"
