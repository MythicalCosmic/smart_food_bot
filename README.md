# 1. Create a virtual environment named .venv
python3 -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Install project dependencies
pip install -r requirements.txt

# 4. Copy the example environment variables file to .env
cp .env-example .env

# 5. Run the application
python3 main.py
