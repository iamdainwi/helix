// hooks/use-auth.ts
// Hook for reading / writing auth state from localStorage.
// Returns: { token, isAuthenticated, setToken, clearToken }

"use client"

import { useState, useEffect, useCallback } from "react"

export function useAuth() {
  const [token, setTokenState] = useState<string | null>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setTokenState(localStorage.getItem("access_token"))
    setMounted(true)
  }, [])

  const setToken = useCallback((t: string) => {
    localStorage.setItem("access_token", t)
    setTokenState(t)
  }, [])

  const clearToken = useCallback(() => {
    localStorage.removeItem("access_token")
    setTokenState(null)
  }, [])

  return {
    token,
    isAuthenticated: mounted ? !!token : false,
    mounted,
    setToken,
    clearToken,
  }
}
