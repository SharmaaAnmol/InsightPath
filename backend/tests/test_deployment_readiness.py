"""
backend/tests/test_deployment_readiness.py
-------------------------------------------
Production deployment readiness verification test suite for InsightPath:
1. Verifies render.yaml specification and Render start command ($PORT, 0.0.0.0)
2. Verifies frontend/vercel.json configuration and security headers
3. Verifies .env.example templates (zero secret commitment, expected keys)
4. Verifies project root resolution and environment overrides
5. Verifies CORS parsing across formats (comma-delimited, wildcard, JSON array)
6. Verifies production health check payload details
"""

import json
from pathlib import Path
import os
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import find_project_root, parse_cors_origins, Settings

client = TestClient(app)


def test_render_yaml_specification():
    """Verify render.yaml exists and follows production standards."""
    root = find_project_root()
    render_file = root / "render.yaml"
    assert render_file.exists(), "render.yaml must be present in project root"

    content = render_file.read_text(encoding="utf-8")
    assert "type: web" in content
    assert "name: insightpath-backend" in content
    assert "buildCommand: pip install -r requirements.txt" in content
    assert "startCommand: uvicorn backend.main:app" in content
    assert "--host 0.0.0.0" in content, "Must bind to 0.0.0.0 for container networking"
    assert "--port $PORT" in content, "Must use dynamic $PORT assigned by Render"
    assert "healthCheckPath: /health" in content


def test_vercel_json_specification():
    """Verify frontend/vercel.json exists, parses valid JSON, and specifies security headers."""
    root = find_project_root()
    vercel_file = root / "frontend" / "vercel.json"
    assert vercel_file.exists(), "frontend/vercel.json must be present"

    with open(vercel_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    assert config.get("framework") == "nextjs"
    assert "headers" in config
    header_rules = config["headers"]
    assert len(header_rules) > 0
    header_keys = [h["key"] for h in header_rules[0]["headers"]]
    assert "X-Content-Type-Options" in header_keys
    assert "X-Frame-Options" in header_keys


def test_env_example_templates_and_no_secrets():
    """Verify .env.example files exist and contain no sensitive secrets."""
    root = find_project_root()
    backend_env = root / ".env.example"
    frontend_env = root / "frontend" / ".env.example"

    assert backend_env.exists(), ".env.example must exist in root"
    assert frontend_env.exists(), "frontend/.env.example must exist"

    b_content = backend_env.read_text(encoding="utf-8")
    assert "HOST=0.0.0.0" in b_content
    assert "PORT=8000" in b_content
    assert "CORS_ALLOWED_ORIGINS" in b_content

    f_content = frontend_env.read_text(encoding="utf-8")
    assert "NEXT_PUBLIC_API_URL" in f_content
    assert "NEXT_PUBLIC_SUPABASE_URL" in f_content
    assert "NEXT_PUBLIC_SUPABASE_ANON_KEY" in f_content

    # Ensure no committed active secret keys
    forbidden_tokens = ["sbp_", "eyJh", "ghp_", "sk_live"]
    for token in forbidden_tokens:
        assert token not in b_content, f"Forbidden secret token found in backend .env.example: {token}"
        assert token not in f_content, f"Forbidden secret token found in frontend .env.example: {token}"


def test_cors_origin_parsing_variations(monkeypatch):
    """Test CORS parser handles wildcard, comma-delimited strings, and JSON arrays."""
    # Wildcard
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "*")
    assert parse_cors_origins() == ["*"]

    # Comma-separated
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        "https://insightpath.vercel.app, https://preview.vercel.app",
    )
    assert parse_cors_origins() == [
        "https://insightpath.vercel.app",
        "https://preview.vercel.app",
    ]

    # JSON array format
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        '["https://domain1.com", "https://domain2.com"]',
    )
    assert parse_cors_origins() == [
        "https://domain1.com",
        "https://domain2.com",
    ]


def test_project_root_env_override(monkeypatch, tmp_path):
    """Test that setting PROJECT_ROOT environment variable overrides auto-detection."""
    # Create mock directory structure in tmp_path
    (tmp_path / "data" / "processed").mkdir(parents=True)
    (tmp_path / "outputs" / "tables").mkdir(parents=True)

    monkeypatch.setenv("PROJECT_ROOT", str(tmp_path))
    resolved = find_project_root()
    assert resolved == tmp_path.resolve()


def test_health_check_payload_contract():
    """Verify /health contract fulfills production monitoring expectations."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] in ["ok", "degraded"]
    assert data["version"] == "1.0.0"
    assert data["service"] == "InsightPath API"
    assert data["artifacts_verified"] is True

    details = data["details"]
    assert "models" in details
    assert details["models"]["jds_model_loaded"] is True
    assert details["models"]["sds_model_loaded"] is True
    assert details["models"]["jds_champion_roc_auc"] >= 0.90
    assert details["models"]["sds_champion_roc_auc"] >= 0.95
    assert details["tables_dir_exists"] is True
    assert details["tables_count"] > 0
    assert details["host"] == "0.0.0.0"
    assert "port" in details
