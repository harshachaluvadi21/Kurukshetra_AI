import urllib.request
import json

def run_tests():
    project_id = "e0ff2a1b-7b1b-4dd6-b774-40ab357af937"
    base_url = "http://127.0.0.1:8000/api/v1/runs"
    
    # 1. POST /api/v1/runs/
    print("Testing POST /api/v1/runs/")
    payload = json.dumps({"project_id": project_id, "idea": "Test idea for graph execution"}).encode("utf-8")
    req = urllib.request.Request(base_url + "/", data=payload, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("Run created successfully:", data)
        run_id = data["run_id"]
        
    # 2. GET /api/v1/runs/{run_id}
    print(f"\nTesting GET /api/v1/runs/{run_id}")
    req = urllib.request.Request(f"{base_url}/{run_id}")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("Run retrieved successfully:", data)

    # 3. POST /api/v1/runs/{run_id}/execute
    print(f"\nTesting POST /api/v1/runs/{run_id}/execute")
    req = urllib.request.Request(f"{base_url}/{run_id}/execute", data=b"{}", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("Run executed successfully:", data)

if __name__ == "__main__":
    run_tests()
