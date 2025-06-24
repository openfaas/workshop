import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables."""
    env_vars = {}
    
    def set_env(key, value):
        env_vars[key] = value
        monkeypatch.setenv(key, value)
    
    def get_env(key, default=None):
        return env_vars.get(key, default)
    
    mock = Mock()
    mock.set = set_env
    mock.get = get_env
    mock.vars = env_vars
    
    return mock


@pytest.fixture
def mock_requests(mocker):
    """Mock requests library."""
    mock = mocker.patch('requests.get')
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {}
    mock.return_value.text = ""
    return mock


@pytest.fixture
def mock_github_client(mocker):
    """Mock PyGithub client."""
    mock_github = mocker.patch('github.Github')
    mock_instance = Mock()
    mock_github.return_value = mock_instance
    return mock_instance


@pytest.fixture
def sample_handler_event():
    """Sample OpenFaaS handler event."""
    return {
        "body": "test body",
        "headers": {
            "Content-Type": "application/json",
            "X-GitHub-Event": "issues",
            "X-Hub-Signature": "sha1=test_signature"
        },
        "method": "POST",
        "query": {},
        "path": "/"
    }


@pytest.fixture
def sample_github_payload():
    """Sample GitHub webhook payload."""
    return {
        "action": "opened",
        "issue": {
            "id": 1,
            "number": 42,
            "title": "Test Issue",
            "body": "This is a test issue",
            "user": {
                "login": "testuser"
            },
            "labels": []
        },
        "repository": {
            "name": "test-repo",
            "owner": {
                "login": "test-owner"
            }
        }
    }


@pytest.fixture
def mock_config_file(temp_dir):
    """Create a mock configuration file."""
    config_path = temp_dir / "config.json"
    config_data = {
        "github_token": "test_token",
        "webhook_secret": "test_secret",
        "labels": ["bug", "enhancement", "question"]
    }
    
    import json
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
    
    return config_path


@pytest.fixture(autouse=True)
def reset_modules():
    """Reset imported modules between tests."""
    import sys
    modules_to_reset = [
        module for module in sys.modules.keys() 
        if module.startswith(('astronaut-finder', 'hello-openfaas', 
                            'hmac-protected', 'issue-bot'))
    ]
    for module in modules_to_reset:
        sys.modules.pop(module, None)


@pytest.fixture
def capture_logs(caplog):
    """Capture and return logs."""
    import logging
    caplog.set_level(logging.DEBUG)
    return caplog