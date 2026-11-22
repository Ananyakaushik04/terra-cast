
const API_URL = import.meta.env.VITE_API_URL;

// Check backend connection
export const checkBackend = async () => {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend connection failed");
  }

  return response.json();
};

// Get sample dataset
export const getSampleDataset = async () => {
  const response = await fetch(`${API_URL}/dataset/sample`);

  if (!response.ok) {
    throw new Error("Unable to fetch dataset");
  }

  return response.json();
};

// Fast prediction
export const predictFast = async (data) => {
  const response = await fetch(`${API_URL}/predict/fast`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Fast prediction failed");
  }

  return response.json();
};

// Policy prediction
export const predictPolicy = async (data) => {
  const response = await fetch(`${API_URL}/predict/policy`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Policy prediction failed");
  }

  return response.json();
};
