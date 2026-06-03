import google.generativeai as genai
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.settings import settings

genai.configure(api_key=settings.google_api_key)

print("Available Models:")
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(m.name)
