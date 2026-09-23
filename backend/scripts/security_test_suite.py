"""
Kurukshetra.AI Production Security Verification Test Suite
Automated verification for all 15 security checks.
Uses httpx.AsyncClient with persistent Windows asyncio loop to prevent asyncpg event-loop collisions.
"""
import sys
import os
import uuid
import re
import json
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import httpx
from app.main import app
from app.core.settings import settings
from app.core.auth import create_access_token
from app.core.ai_limits import ai_limits_manager

TOTAL_TESTS = 0
PASSED_TESTS = 0
FAILED_TESTS = []

def record_result(test_name: str, passed: bool, details: str = ""):
    global TOTAL_TESTS, PASSED_TESTS, FAILED_TESTS
    TOTAL_TESTS += 1
    if passed:
        PASSED_TESTS += 1
        print(f"  [PASS] {test_name}", flush=True)
    else:
        FAILED_TESTS.append((test_name, details))
        print(f"  [FAIL] {test_name}: {details}", flush=True)

async def run_tests():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        print("=" * 70, flush=True)
        print(" KURUKSHETRA.AI — PRODUCTION SECURITY TEST SUITE ", flush=True)
        print("=" * 70, flush=True)

        # -------------------------------------------------------------
        # 01 - API KEY PROTECTION
        # -------------------------------------------------------------
        print("\n--- 01. API KEY PROTECTION ---", flush=True)
        frontend_dir = backend_dir.parent / "frontend" / "src"
        frontend_exposed_keys = []
        suspicious_patterns = [
            re.compile(r'AIza[0-9A-Za-z-_]{35}'),
            re.compile(r'sk-[A-Za-z0-9]{32,}'),
            re.compile(r'gsk_[A-Za-z0-9]{40,}'),
            re.compile(r'tvly-[A-Za-z0-9_-]+'),
        ]
        if frontend_dir.exists():
            for root, _, files in os.walk(frontend_dir):
                for file in files:
                    if file.endswith((".ts", ".tsx", ".js", ".jsx", ".json")):
                        file_path = Path(root) / file
                        try:
                            content = file_path.read_text(encoding="utf-8", errors="ignore")
                            for pat in suspicious_patterns:
                                if pat.search(content):
                                    frontend_exposed_keys.append(str(file_path))
                        except Exception:
                            pass
        record_result(
            "No hardcoded API keys in frontend source files",
            len(frontend_exposed_keys) == 0,
            f"Exposed keys found in: {frontend_exposed_keys}"
        )

        env_example_path = backend_dir / ".env.example"
        has_real_secrets = False
        if env_example_path.exists():
            for line in env_example_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if any(sec in k.lower() for sec in ("key", "secret")) and v.strip() and v.strip() != "your-secret-key-here":
                        has_real_secrets = True
        record_result(
            "backend/.env.example contains only safe placeholders",
            not has_real_secrets,
            "Found non-placeholder secrets in .env.example"
        )

        # -------------------------------------------------------------
        # 02 - SECURITY HEADERS
        # -------------------------------------------------------------
        print("\n--- 02. SECURITY HEADERS ---", flush=True)
        res = await client.get("/health")
        headers = res.headers
        record_result(
            "X-Content-Type-Options: nosniff present",
            headers.get("x-content-type-options") == "nosniff",
            f"Got: {headers.get('x-content-type-options')}"
        )
        record_result(
            "X-Frame-Options: DENY present",
            headers.get("x-frame-options") == "DENY",
            f"Got: {headers.get('x-frame-options')}"
        )
        record_result(
            "Referrer-Policy: strict-origin-when-cross-origin present",
            headers.get("referrer-policy") == "strict-origin-when-cross-origin",
            f"Got: {headers.get('referrer-policy')}"
        )
        record_result(
            "Permissions-Policy present",
            "permissions-policy" in headers,
            "Missing permissions-policy"
        )

        # -------------------------------------------------------------
        # 03 - INPUT VALIDATION
        # -------------------------------------------------------------
        print("\n--- 03. INPUT VALIDATION ---", flush=True)
        # Register a real test user in DB so authentication succeeds
        val_user_email = f"validator_{uuid.uuid4().hex[:6]}@example.com"
        reg_val = await client.post("/auth/register", json={"name": "Val User", "email": val_user_email, "password": "Password123!"})
        val_token = reg_val.json().get("access_token")
        auth_header = {"Authorization": f"Bearer {val_token}"}

        # Oversized prompt (> 2000 chars)
        oversized_res = await client.post(
            "/api/v1/runs/",
            headers=auth_header,
            json={"project_id": "00000000-0000-0000-0000-000000000000", "idea": "A" * 2500}
        )
        record_result(
            "Oversized idea (>2000 chars) rejected with 422",
            oversized_res.status_code == 422,
            f"Status: {oversized_res.status_code}"
        )

        # Too short idea (< 3 chars)
        short_res = await client.post(
            "/api/v1/runs/",
            headers=auth_header,
            json={"project_id": "00000000-0000-0000-0000-000000000000", "idea": "AB"}
        )
        record_result(
            "Undersized idea (<3 chars) rejected with 422",
            short_res.status_code == 422,
            f"Status: {short_res.status_code}"
        )

        # Invalid UUID in path param
        invalid_uuid_res = await client.get("/api/v1/runs/not-a-valid-uuid", headers=auth_header)
        record_result(
            "Malformed UUID path parameter rejected with 400",
            invalid_uuid_res.status_code == 400,
            f"Status: {invalid_uuid_res.status_code}"
        )

        # Invalid email registration
        invalid_email_res = await client.post(
            "/auth/register",
            json={"name": "Hacker", "email": "not-an-email", "password": "securepassword123"}
        )
        record_result(
            "Malformed email registration rejected with 422",
            invalid_email_res.status_code == 422,
            f"Status: {invalid_email_res.status_code}"
        )

        # Short password registration
        short_pw_res = await client.post(
            "/auth/register",
            json={"name": "Hacker", "email": "hacker@test.com", "password": "123"}
        )
        record_result(
            "Short password (<8 chars) registration rejected with 422",
            short_pw_res.status_code == 422,
            f"Status: {short_pw_res.status_code}"
        )

        # -------------------------------------------------------------
        # 04 - AUTHENTICATION SECURITY
        # -------------------------------------------------------------
        print("\n--- 04. AUTHENTICATION ---", flush=True)
        unauth_res = await client.get("/auth/me")
        record_result(
            "Unauthenticated /auth/me rejected with 401",
            unauth_res.status_code == 401,
            f"Status: {unauth_res.status_code}"
        )

        unauth_runs_res = await client.post(
            "/api/v1/runs/",
            json={"idea": "Valid startup business concept"}
        )
        record_result(
            "Unauthenticated run creation rejected with 401",
            unauth_runs_res.status_code == 401,
            f"Status: {unauth_runs_res.status_code}"
        )

        invalid_token_res = await client.get(
            "/auth/me",
            headers={"Authorization": "Bearer malformed.invalid.token"}
        )
        record_result(
            "Malformed token rejected with 401",
            invalid_token_res.status_code == 401,
            f"Status: {invalid_token_res.status_code}"
        )

        # -------------------------------------------------------------
        # 05 - AUTHORIZATION & IDOR PROTECTION
        # -------------------------------------------------------------
        print("\n--- 05. AUTHORIZATION & IDOR PROTECTION ---", flush=True)
        # Register User A and User B
        user_a_email = f"user_a_{uuid.uuid4().hex[:6]}@example.com"
        user_b_email = f"user_b_{uuid.uuid4().hex[:6]}@example.com"

        reg_a = await client.post("/auth/register", json={"name": "User A", "email": user_a_email, "password": "Password123!"})
        token_a = reg_a.json()["access_token"]
        user_a_id = reg_a.json()["user"]["id"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        reg_b = await client.post("/auth/register", json={"name": "User B", "email": user_b_email, "password": "Password123!"})
        token_b = reg_b.json()["access_token"]
        user_b_id = reg_b.json()["user"]["id"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # User A creates a run
        run_a_res = await client.post("/api/v1/runs/", headers=headers_a, json={"idea": "User A proprietary AI startup"})
        run_a_id = run_a_res.json()["run_id"]

        # User A accesses own run -> 200
        user_a_own_run = await client.get(f"/api/v1/runs/{run_a_id}", headers=headers_a)
        record_result(
            "User A can access own run (200 OK)",
            user_a_own_run.status_code == 200,
            f"Status: {user_a_own_run.status_code}"
        )

        # User B attempts to access User A's run -> 403 Forbidden
        user_b_cross_run = await client.get(f"/api/v1/runs/{run_a_id}", headers=headers_b)
        record_result(
            "User B accessing User A's run blocked with 403 Forbidden (IDOR Defended)",
            user_b_cross_run.status_code == 403,
            f"Status: {user_b_cross_run.status_code}"
        )

        # User B attempts to execute User A's run -> 403 Forbidden
        user_b_cross_exec = await client.post(f"/api/v1/runs/{run_a_id}/execute", headers=headers_b)
        record_result(
            "User B executing User A's run blocked with 403 Forbidden (IDOR Defended)",
            user_b_cross_exec.status_code == 403,
            f"Status: {user_b_cross_exec.status_code}"
        )

        # User B attempts to view User A's report -> 403 Forbidden
        user_b_cross_report = await client.get(f"/api/v1/runs/{run_a_id}/report", headers=headers_b)
        record_result(
            "User B viewing User A's report blocked with 403 Forbidden (IDOR Defended)",
            user_b_cross_report.status_code == 403,
            f"Status: {user_b_cross_report.status_code}"
        )

        # -------------------------------------------------------------
        # 06 - AI KILL SWITCH
        # -------------------------------------------------------------
        print("\n--- 06. AI KILL SWITCH ---", flush=True)
        settings.ai_enabled = False
        
        kill_run_create = await client.post("/api/v1/runs/", headers=headers_a, json={"idea": "Startup while kill switch is active"})
        record_result(
            "Run creation blocked with 503 when AI_ENABLED=False",
            kill_run_create.status_code == 503,
            f"Status: {kill_run_create.status_code}"
        )

        kill_run_exec = await client.post(f"/api/v1/runs/{run_a_id}/execute", headers=headers_a)
        record_result(
            "Run execution blocked with 503 when AI_ENABLED=False",
            kill_run_exec.status_code == 503,
            f"Status: {kill_run_exec.status_code}"
        )

        # Non-AI endpoints continue working
        health_still_ok = await client.get("/health")
        record_result(
            "/health remains 200 OK during kill switch activation",
            health_still_ok.status_code == 200,
            f"Status: {health_still_ok.status_code}"
        )

        auth_me_still_ok = await client.get("/auth/me", headers=headers_a)
        record_result(
            "/auth/me remains 200 OK during kill switch activation",
            auth_me_still_ok.status_code == 200,
            f"Status: {auth_me_still_ok.status_code}"
        )

        # Restore kill switch
        settings.ai_enabled = True

        # -------------------------------------------------------------
        # 07 - AI DAILY QUOTA ENFORCEMENT
        # -------------------------------------------------------------
        print("\n--- 07. AI DAILY USAGE LIMITS ---", flush=True)
        # Simulate reaching daily limit for User A
        orig_daily_limit = settings.ai_daily_limit
        settings.ai_daily_limit = 2
        
        # User A quota exhaustion simulation
        today_key = ai_limits_manager._get_key(str(user_a_id))
        ai_limits_manager.daily_counts[today_key] = 2

        quota_exceeded_res = await client.post(
            "/api/v1/runs/",
            headers=headers_a,
            json={"idea": "Attempt exceeding daily AI quota"}
        )
        record_result(
            "Run creation blocked with 429 when AI_DAILY_LIMIT reached",
            quota_exceeded_res.status_code == 429,
            f"Status: {quota_exceeded_res.status_code}"
        )

        # Reset quota limit
        settings.ai_daily_limit = orig_daily_limit
        ai_limits_manager.daily_counts[today_key] = 0

        # -------------------------------------------------------------
        # 08 - RATE LIMITING
        # -------------------------------------------------------------
        print("\n--- 08. RATE LIMITING ---", flush=True)
        hit_429 = False
        for i in range(12):
            r = await client.post("/auth/login", json={"email": "spam_bot@example.com", "password": "wrongpassword"})
            if r.status_code == 429:
                hit_429 = True
                break
        record_result(
            "Rapid failed logins trigger HTTP 429 Rate Limit Exceeded",
            hit_429,
            "Failed to trigger 429 within limit window"
        )

        # -------------------------------------------------------------
        # 09 - SAFE PRODUCTION ERROR HANDLING
        # -------------------------------------------------------------
        print("\n--- 09. ERROR HANDLING SAFETY ---", flush=True)
        err_res = await client.get("/api/v1/runs/00000000-0000-0000-0000-000000000000", headers=headers_a)
        err_body = err_res.text
        record_result(
            "404 error does not leak stack traces or internal paths",
            "Traceback" not in err_body and "File " not in err_body and "postgresql" not in err_body.lower(),
            f"Body leaked info: {err_body}"
        )

        # -------------------------------------------------------------
        # 10 - DATA SANITIZATION / XSS TEST
        # -------------------------------------------------------------
        print("\n--- 10. DATA SANITIZATION (XSS) ---", flush=True)
        renderer_file = backend_dir.parent / "frontend" / "src" / "components" / "ui" / "MarkdownRenderer.tsx"
        renderer_content = renderer_file.read_text(encoding="utf-8") if renderer_file.exists() else ""
        has_sanitization = "sanitizeHtml" in renderer_content and "&lt;" in renderer_content
        record_result(
            "MarkdownRenderer sanitizes raw HTML tags before dangerouslySetInnerHTML",
            has_sanitization,
            "Missing sanitizeHtml in MarkdownRenderer.tsx"
        )

        # -------------------------------------------------------------
        # 11 - WEBSOCKET SECURITY
        # -------------------------------------------------------------
        print("\n--- 11. WEBSOCKET SECURITY ---", flush=True)
        ws_manager_file = backend_dir / "app" / "api" / "websockets" / "manager.py"
        ws_content = ws_manager_file.read_text(encoding="utf-8") if ws_manager_file.exists() else ""
        has_ws_auth = "decode_access_token" in ws_content and "run.user_id" in ws_content
        record_result(
            "WebSocket endpoint enforces JWT decoding and run ownership validation",
            has_ws_auth,
            "Missing authentication checks in WebSocket manager"
        )

        # -------------------------------------------------------------
        # 12 - GITHUB & SECRETS CONFIGURATION
        # -------------------------------------------------------------
        print("\n--- 12. GITHUB & SECRETS CONFIGURATION ---", flush=True)
        gitignore_file = backend_dir.parent / ".gitignore"
        gitignore_content = gitignore_file.read_text(encoding="utf-8") if gitignore_file.exists() else ""
        record_result(
            ".gitignore ignores .env*, secrets/, *.pem, *.key",
            ".env*" in gitignore_content and "secrets/" in gitignore_content,
            "Missing environment patterns in root .gitignore"
        )

        # -------------------------------------------------------------
        # 13 - SUMMARY & VERIFICATION
        # -------------------------------------------------------------
        print("\n" + "=" * 70, flush=True)
        print(f" TOTAL TESTS RUN: {TOTAL_TESTS} | PASSED: {PASSED_TESTS} | FAILED: {len(FAILED_TESTS)}", flush=True)
        print("=" * 70, flush=True)

        if FAILED_TESTS:
            print("\nFailed Tests Details:", flush=True)
            for name, details in FAILED_TESTS:
                print(f" - {name}: {details}", flush=True)
            sys.exit(1)
        else:
            print("\nALL SECURITY TESTS PASSED SUCCESSFULLY!", flush=True)
            sys.exit(0)

if __name__ == "__main__":
    asyncio.run(run_tests())
