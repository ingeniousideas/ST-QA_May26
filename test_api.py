# test_api.py
import pytest
from fastapi.testclient import TestClient

# Import your FastAPI app. Change 'main' to your filename (without .py) if needed.
from app import app

client = TestClient(app)


def test_health_ok():
    """Health endpoint should return a basic OK status."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_search_staff_filter_sort_paginate():
    """
    Should:
    - filter by department=Engineering
    - sort by name desc
    - paginate with page_size=2 (take first page)
    Validate total count, page metadata, and the order of returned names.
    """
    params = {
        "department": "Engineering",
        "sort_by": "name",
        "order": "desc",
        "page": 1,
        "page_size": 2,
    }
    resp = client.get("/staff", params=params)
    assert resp.status_code == 200
    data = resp.json()

    # total should reflect ALL engineering matches in the mock DB (Alice, Bob, Eva, Isabella, ... etc)
    assert data["total"] >= 1
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert isinstance(data["items"], list)
    assert len(data["items"]) <= 2

    # Check all returned items are in the department and order is descending by name
    names = []
    for item in data["items"]:
        assert item["department"].lower() == "engineering"
        names.append(item["name"])

    # Ensure the names are in descending order (case-insensitive)
    assert names == sorted(names, key=lambda s: s.lower(), reverse=True)


def test_get_staff_by_id_and_not_found():
    """Valid id returns a staff record; invalid id returns 404."""
    # Known IDs in your seed data go from 1..10
    ok_resp = client.get("/staff/1")
    assert ok_resp.status_code == 200
    staff = ok_resp.json()
    assert staff["id"] == 1
    assert "name" in staff
    assert "email" in staff

    # Invalid ID
    not_found_resp = client.get("/staff/9999")
    assert not_found_resp.status_code == 404
    detail = not_found_resp.json().get("detail", "")
    assert "not found" in detail.lower()
