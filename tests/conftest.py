"""Instructor-owned fixture. Reload resets module-level in-memory state."""
import importlib
import os
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    module = importlib.reload(importlib.import_module(os.environ.get("APP_MODULE", "app.main")))
    with TestClient(module.app) as test_client:
        yield test_client
