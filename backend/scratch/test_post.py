import requests
import uuid
import json

url = "http://127.0.0.1:8000/api/v1/runs"

def test_run(project_id: str, idea: str):
    payload = {"project_id": project_id, "idea": idea}
    response = requests.post(url, json=payload)
    print("Status:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response text:", response.text)

if __name__ == "__main__":
    # Test with invalid UUID
    print("--- Testing invalid UUID ---")
    test_run("not-a-uuid", "Test idea invalid UUID")
    # Test with valid UUID
    print("--- Testing valid UUID ---")
    test_run(str(uuid.uuid4()), "Test idea valid UUID")
