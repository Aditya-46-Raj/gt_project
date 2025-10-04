import axios from "axios";

// --- CORRECTED: Use a base URL for API requests. The "proxy" in package.json handles this in development.
const API_URL = "/api/analyze";

export const uploadBlueprint = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(API_URL, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};