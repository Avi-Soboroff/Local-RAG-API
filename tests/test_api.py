from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#  Test for missing fields a.k.a failed POST request
def test_add_profile_missing_fields():
    response = client.post("/profiles", json={})
    assert response.status_code == 422
    assert "detail" in response.json()

# Test for a successful POST request. Can adjust the content field to include any string of any size
def test_add_profile_with_fields():
    payload = {"user_name": "TestUser", "content": "This is valid profile content"}
    # removes whitespaces and splits content string by new paragraph lines if there is content after the newline.
    chunks = len([c.strip() for c in payload["content"].split('\n\n') if c.strip()])
    response = client.post("/profiles", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user_name"] == payload["user_name"]
    assert response_data["chunks_added"] == chunks

# # Test GET endpoint when user parameter is used
# def test_ask_with_user_filter():
#     params = {"question": "What do you want to know?", "user": "TestUser"}
#     response = client.get("/ask", params=params)

#     assert response.status_code == 200
#     response_data = response.json()

# Test GET endpoint without user parameter
def test_ask_without_user_filter():
    params = {"question": "What do you want to know?"}
    response = client.get("/ask", params=params)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["question"] == params["question"]
    assert response_data["filtered_by_user"] is None
