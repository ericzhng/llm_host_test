import requests

BASE_URL = "http://localhost:8000"


# Create API key
response = requests.post(f"{BASE_URL}/create-api-key", json={"user_id": "user12"})
if response.status_code == 200:
    api_key = response.json()["api_key"]
    print(f"Created API Key: {api_key}")
elif response.status_code == 400 and response.json().get("detail") == "User ID already has an API key":
    print("User ID 'user1' already exists. Attempting to reuse or skipping creation.")
    # Optional: Query existing key or proceed with a different user_id
    # For simplicity, we'll exit here; modify as needed
    exit()
else:
    print(f"Failed to create API key: {response.json()['detail']}")
    exit()


# Predict
headers = {"X-API-Key": api_key}
response = requests.post(f"{BASE_URL}/predict", json={"text": "Hello, world!"}, headers=headers)
if response.status_code == 200:
    print(f"Prediction: {response.json()}")
else:
    print(f"Prediction failed: {response.json()['detail']}")


# Revoke API key
response = requests.post(f"{BASE_URL}/revoke-api-key", json={"api_key": api_key}, headers=headers)
if response.status_code == 200:
    print(f"Revoked API Key: {response.json()}")
else:
    print(f"Revocation failed: {response.json()['detail']}")
