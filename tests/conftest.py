"""
Pytest configuration and fixtures for FastAPI tests.

This module provides shared fixtures for all tests:
- test_client: FastAPI TestClient instance for making test requests
- sample_activities: Fresh copy of activities database for test isolation
"""

import sys
from pathlib import Path
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def test_client():
    """
    Fixture that provides a FastAPI TestClient instance.
    
    This client allows making HTTP requests to the FastAPI app
    in a synchronous manner during tests.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture that provides a fresh copy of the activities database.
    
    Uses deepcopy to ensure test isolation - modifications to activities
    in one test won't affect other tests (since we're using shared database approach).
    
    Returns a dictionary with all activities and their details.
    """
    return deepcopy(activities)
