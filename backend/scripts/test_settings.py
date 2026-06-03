import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.settings import settings

def test_settings():
    try:
        settings.validate_health()
        print("\nPASS: settings.py loaded correctly and all critical configurations are present.")
    except Exception as e:
        print(f"\nFAIL: settings.py failed validation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_settings()
