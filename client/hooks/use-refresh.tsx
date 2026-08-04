// hooks/use-refresh.tsx
// A lightweight shared refresh context.
// Any component can call triggerRefresh() to notify all subscribers
// (Sidebar, Navbar) to re-fetch their data.
"use client"

import { createContext, useContext, useState, useCallback, ReactNode } from "react"

interface RefreshContextValue {
  refreshKey: number
  triggerRefresh: () => void
}

const RefreshContext = createContext<RefreshContextValue>({
  refreshKey: 0,
  triggerRefresh: () => {},
})

export function RefreshProvider({ children }: { children: ReactNode }) {
  const [refreshKey, setRefreshKey] = useState(0)

  const triggerRefresh = useCallback(() => {
    setRefreshKey((k) => k + 1)
  }, [])

  return (
    <RefreshContext.Provider value={{ refreshKey, triggerRefresh }}>
      {children}
    </RefreshContext.Provider>
  )
}

export function useRefresh() {
  return useContext(RefreshContext)
}
