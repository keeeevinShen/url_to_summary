#!/bin/bash

echo "🚀 Starting Full Installation..."

# 1️⃣ Step 1: Create Virtual Environment
if [ ! -d "env" ]; then
    echo "🐍 Creating a virtual environment..."
    python3 -m venv env
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

# 5️⃣ Step 5: Download the LLM Model (llama3)
echo "🧠 Downloading the LLM model (llama3)..."
ollama pull llama3

# 6️⃣ Step 6: Install macOS Command-Line Tools (if needed)
if ! xcode-select -p &> /dev/null; then
    echo "🛠️ Installing macOS Command-Line Tools..."
    xcode-select --install
else
    echo "✅ Command-line tools already installed."
fi

# 7️⃣ Step 7: Run the Application
echo "🚀 Installation Complete! Launching the app..."
open dist/app.app

echo "🎉 Done! You can now run the app directly from your Applications folder."

# Deactivate virtual environment (optional)
deactivate
