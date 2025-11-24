import axios from "axios";

// In development, always use the proxy. In production, use the env var or fallback to /api.
const baseURL = import.meta.env.DEV ? "/api" : (import.meta.env.VITE_BACKEND_URL || "/api");

export default axios.create({
  baseURL: baseURL,
});
