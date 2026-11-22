const API_BASE_URL = import.meta.env.VITE_API_URL?.replace(/\/+$/, "");

console.log("TerraCast Backend URL:", API_BASE_URL);

// Check backend URL configuration
if (!API_BASE_URL) {
    console.error("VITE_API_URL is missing. Check Vercel Environment Variables.");
}

// Common API request handler
const apiRequest = async (endpoint, options = {}) => {
    if (!API_BASE_URL) {
        throw new Error("Backend URL is not configured.");
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
            `API Error ${response.status}: ${errorText}`
        );
    }

    return response.json();
};

// Get sample dataset
export const getSampleDataset = async (station = null) => {
    const query = station
        ? `?station=${encodeURIComponent(station)}`
        : "";

    return apiRequest(`/dataset/sample${query}`);
};

// Fast AQI prediction
export const predictFast = async (data) => {
    return apiRequest("/predict/fast", {
        method: "POST",
        body: JSON.stringify(data)
    });
};

// Policy prediction
export const predictPolicy = async (data) => {
    return apiRequest("/predict/policy", {
        method: "POST",
        body: JSON.stringify(data)
    });
};

// Check backend health
export const checkBackend = async () => {
    return apiRequest("/health");
};

