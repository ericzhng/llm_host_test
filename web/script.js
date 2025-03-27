const BASE_URL = "http://localhost:8000";

async function apiRequest(endpoint, method, data, apiKey = null) {
    const headers = {
        "Content-Type": "application/json",
    };
    if (apiKey) headers["X-API-Key"] = apiKey;

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method,
        headers,
        body: JSON.stringify(data),
    });
    const result = await response.json();
    return { status: response.status, data: result };
}

function displayOutput(message, isError = false) {
    const outputDiv = document.getElementById("output");
    outputDiv.textContent = message;  // Use textContent to ensure full text
    outputDiv.className = isError ? "error" : "success";
}

function formatOutput(data, type) {
    switch (type) {
        case "create":
            return `API Key: ${data.api_key}\nUser ID: ${data.user_id}`;
        case "predict":
            return `Response: ${data.response}\nUser ID: ${data.user_id}`;  // No truncation here
        case "revoke":
            return `Message: ${data.message}`;
        default:
            return JSON.stringify(data, null, 2); // Fallback
    }
}

async function createApiKey() {
    const userId = document.getElementById("userId").value;
    if (!userId) return displayOutput("Please enter a User ID", true);

    try {
        const { status, data } = await apiRequest("/create-api-key", "POST", { user_id: userId });
        if (status === 200) {
            displayOutput(formatOutput(data, "create"));
            document.getElementById("apiKey").value = data.api_key;
            document.getElementById("revokeKey").value = data.api_key;
        } else {
            displayOutput(`Error: ${data.detail}`, true);
        }
    } catch (error) {
        displayOutput(`Request failed: ${error.message}`, true);
    }
}

async function predict() {
    const apiKey = document.getElementById("apiKey").value;
    const text = document.getElementById("textInput").value;
    if (!apiKey || !text) return displayOutput("Please enter API Key and Text", true);

    try {
        const { status, data } = await apiRequest("/predict", "POST", { text }, apiKey);
        if (status === 200) {
            displayOutput(formatOutput(data, "predict"));
        } else {
            displayOutput(`Error: ${data.detail}`, true);
        }
    } catch (error) {
        displayOutput(`Request failed: ${error.message}`, true);
    }
}

async function revokeApiKey() {
    const apiKey = document.getElementById("revokeKey").value;
    if (!apiKey) return displayOutput("Please enter an API Key to revoke", true);

    try {
        const { status, data } = await apiRequest("/revoke-api-key", "POST", { api_key: apiKey }, apiKey);
        if (status === 200) {
            displayOutput(formatOutput(data, "revoke"));
            document.getElementById("apiKey").value = "";
            document.getElementById("revokeKey").value = "";
        } else {
            displayOutput(`Error: ${data.detail}`, true);
        }
    } catch (error) {
        displayOutput(`Request failed: ${error.message}`, true);
    }
}