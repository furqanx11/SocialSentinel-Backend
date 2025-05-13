# import pytest
# from script import detect_abuse
# from asgi_lifespan import LifespanManager
# from httpx import AsyncClient
# from main import app


# @pytest.mark.asyncio
# async def test_detect_abuse_exact_match(mocker):
#     mock_update_fairness_score = mocker.patch("app.auth.db.update_fairness_score", return_value=None)
#     mock_add_detected_words = mocker.patch("app.auth.db.add_detected_words", return_value=None)

#     result, reason, score = await detect_abuse("idiot", "67ebcfa1c1213cb848227125")
#     assert result is True
#     assert reason == "Exact match (idiot)"
#     assert score == 0.25
#     mock_update_fairness_score.assert_called_once_with("67ebcfa1c1213cb848227125", 0.25)
#     mock_add_detected_words.assert_called_once_with("67ebcfa1c1213cb848227125", "idiot")

# @pytest.mark.asyncio
# async def test_detect_abuse_clean_text():
#     result, reason, score = await detect_abuse("hello world", "67ebcfa1c1213cb848227125")
#     assert result is False
#     assert reason == "Clean"
#     assert score == 0.0

# from app.auth.views import create_user
# from app.auth.model import UserSignUp


# from starlette.testclient import TestClient

# client = TestClient(app)

# @pytest.mark.asyncio
# async def test_detect_abuse_endpoint(mocker):
#     mock_detect_abuse = mocker.patch("script.detect_abuse", return_value=(True, "Exact match (idiot)", 0.25))
#     mocker.patch("app.middleware.dependecy.get_current_user", return_value="67ebcfa1c1213cb848227125")

#     response = client.post("/detect", json={"text": "idiot"})
#     assert response.status_code == 200
#     assert response.json() == {"flagged": True, "reason": "Exact match (idiot)", "score": 0.25}
#     mock_detect_abuse.assert_called_once_with("idiot", "67ebcfa1c1213cb848227125")

# def test_user_signup_and_login():
#     # Step 1: Sign up a new user
#     signup_response = client.post("/auth/", json={
#         "name": "John Doe",
#         "username": "johndoe",
#         "email": "john@example.com",
#         "password": "password123"
#     })
#     assert signup_response.status_code == 200
#     assert "data" in signup_response.json()

#     # Step 2: Log in with the same user
#     login_response = client.post("/auth/login", json={
#         "username": "johndoe",
#         "password": "password123"
#     })
#     assert login_response.status_code == 200
#     assert "data" in login_response.json()


# def test_detect_abuse_integration_with_extension():
#     # Simulate a message sent from the browser extension
#     response = client.post("/detect", json={"text": "idiot"})
#     assert response.status_code == 200
#     assert response.json()["flagged"] is True
#     assert response.json()["reason"] == "Exact match (idiot)"

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from main import app
from script import detect_abuse
from app.auth.views import create_user
from app.auth.model import UserSignUp

# -------------------- Unit Tests for detect_abuse() --------------------
@pytest.mark.asyncio
async def test_detect_abuse_exact_match(mocker):
    mock_update = mocker.patch("app.auth.db.update_fairness_score", return_value=None)
    mock_add_words = mocker.patch("app.auth.db.add_detected_words", return_value=None)
    
    mock_update.return_value = None
    mock_add_words.return_value = None
    
    result, reason, score = await detect_abuse("idiot", "67ebcfa1c1213cb848227125")
    
    assert result is True
    assert reason == "Exact match (idiot)"
    assert score == 0.25
    mock_update.assert_called_once_with("67ebcfa1c1213cb848227125", 0.25)
    mock_add_words.assert_called_once_with("67ebcfa1c1213cb848227125", "idiot")

@pytest.mark.asyncio
async def test_detect_abuse_clean_text(mocker):
    mocker.patch("app.auth.db.update_fairness_score", return_value=None)
    mocker.patch("app.auth.db.add_detected_words", return_value=None)
    
    result, reason, score = await detect_abuse("hello world", "67ebcfa1c1213cb848227125")
    
    # Assert the results
    assert result is False
    assert reason == "Clean"
    assert score == 0.0

# -------------------- Endpoint Test for /detect (async) --------------------
@pytest.mark.asyncio
async def test_detect_abuse_endpoint(mocker):
    mock_detect_abuse = mocker.patch("script.detect_abuse", return_value=(True, "Exact match (idiot)", 0.25))
    
    mocker.patch("app.middleware.dependecy.get_current_user", return_value="67ebcfa1c1213cb848227125")
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/detect", 
            json={"text": "idiot"},
            headers={"Authorization": "Bearer token"}  
        )
        
        assert response.status_code == 200
        assert response.json() == {
            "flagged": True,
            "reason": "Exact match (idiot)",
            "score": 0.25
        }
        
        mock_detect_abuse.assert_called_once_with("idiot", "67ebcfa1c1213cb848227125")

# -------------------- Signup/Login (sync) --------------------
@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

def test_user_signup_and_login(test_client, mocker):
    mocker.patch("app.auth.db.create_user", return_value={"_id": "123", "name": "Furqan Ahmed", "username": "furqan_ahmed", "email": "furqan@bahria.com"})
    mocker.patch("app.auth.db.get_user_by_username", return_value={"_id": "123", "name": "Furqan Ahmed", "username": "furqan_ahmed", "email": "furqan@bahria.com"})
    
    signup_response = test_client.post("/auth/", json={
        "name": "Furqan Ahmed",
        "username": "furqan_ahmed",
        "email": "furqan@bahria.com",
        "password": "password123"
    })
    assert signup_response.status_code == 200
    assert "data" in signup_response.json()
    
    login_response = test_client.post("/auth/login", json={
        "username": "furqan",
        "password": "password123"
    })
    assert login_response.status_code == 200
    assert "data" in login_response.json()

# -------------------- Integration Test (sync) --------------------
def test_detect_abuse_integration_with_extension(test_client, mocker):
    mocker.patch("script.detect_abuse", return_value=(True, "Exact match (idiot)", 0.25))
    mocker.patch("app.middleware.dependecy.get_current_user", return_value="67ebcfa1c1213cb848227125")
    
    response = test_client.post(
        "/detect", 
        json={"text": "idiot"},
        headers={"Authorization": "Bearer token"} 
    )
    
    assert response.status_code == 200
    assert response.json()["flagged"] is True
    assert response.json()["reason"] == "Exact match (idiot)"