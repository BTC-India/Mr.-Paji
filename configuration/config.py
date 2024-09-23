import os
from dotenv import load_dotenv

# Get the current directory path
current_dir = os.path.abspath(os.path.dirname(__file__))

# Go one folder back
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Load environment variables from .env file in the parent folder
dotenv_path = os.path.join(parent_dir, '.env')
load_dotenv(dotenv_path)

API_TOKEN = os.getenv("TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
