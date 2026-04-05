import yaml

def test_compose_has_three_services():
    with open("docker-compose.yml") as f:
        compose = yaml.safe_load(f)
    assert len(compose.get("services", {})) >= 3

def test_frontend_dockerfile_exists():
    from pathlib import Path
    assert Path("frontend/Dockerfile").exists()
