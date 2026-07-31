// lib/axios.ts
// Central axios instance for all server-side and client-side API calls.
// Uses NEXT_PUBLIC_API_URL from env (defaults to http://localhost:8000).
// Reads auth token from localStorage (client-side) or Authorization header.

import axios from "axios"

const apiClient = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
})

// Attach JWT from localStorage on every request (client-side only)
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  }
  return config
})

// On 401, clear token and redirect to login
apiClient.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("access_token")
      window.location.href = "/login"
    }
    return Promise.reject(error)
  }
)

export default apiClient
