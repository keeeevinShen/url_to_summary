#!/bin/bash

echo "🚀 Starting Installation for Canvas Lecture Summarizer..."

# 1️⃣ Step 1: Set Up Virtual Environment
if [ ! -d "env" ]; then
    echo "🐍 Creating a virtual environment..."
    python3 -m venv env
else
    echo "🔁 Virtual environment already exists."
fi

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source env/bin/activate

# 2️⃣ Step 2: Install Python Dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3️⃣ Step 3: Install Playwright Browsers
echo "🌐 Installing Playwright browsers..."
playwright install

# 4️⃣ Step 4: Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "🤖 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama is already installed."
fi

# 5️⃣ Step 5: Download LLM Model (llama3)
echo "🧠 Downloading the LLM model (llama3)..."
ollama pull llama3

# 6️⃣ Step 6: Run the Python Script
echo "🚀 Launching the Lecture Summarizer..."
python3 app.py

# 7️⃣ Deactivate virtual environment after completion
deactivate

echo "🎉 Installation complete!"
