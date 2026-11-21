const API_BASE_URL = import.meta.env.VITE_API_URL;

console.log("Backend URL:", API_BASE_URL);

export const getSampleDataset = async () => {
    const response = await fetch(`${API_BASE_URL}/dataset/sample`);

    if (!response.ok) {
        throw new Error(`Dataset Error: ${response.status}`);
    }

    return response.json();
};

export const predictFast = async (data) => {
    const response = await fetch(`${API_BASE_URL}/predict/fast`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(`Prediction Error: ${response.status}`);
    }

    return response.json();
};

export const predictPolicy = async (data) => {
    const response = await fetch(`${API_BASE_URL}/predict/policy`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(`Policy Error: ${response.status}`);
    }

    return response.json();
};

export const checkBackend = async () => {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
        throw new Error("Backend connection failed");
    }

    return response.json();
};
