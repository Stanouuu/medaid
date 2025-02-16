from dotenv import load_dotenv
import os

API_KEY = ""
#importation de l'API
def get_api():
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
