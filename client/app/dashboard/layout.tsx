"use client"

import { useEffect } from "react"
import { usePathname, useRouter } from "next/navigation"
import { useAuth } from "@/hooks/use-auth"
import { AppSidebar } from "@/components/app-sidebar"
import { Navbar } from "@/components/navbar"
import { SidebarProvider } from "@/components/ui/sidebar"
import { RefreshProvider } from "@/hooks/use-refresh"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { isAuthenticated, mounted } = useAuth()
  const pathname = usePathname()

  // Auth guard
  useEffect(() => {
    if (mounted && !isAuthenticated) {
      router.push("/login")
    }
  }, [mounted, isAuthenticated, router])

  if (!mounted || !isAuthenticated) return null

  return (
    <RefreshProvider>
      <SidebarProvider>
        <AppSidebar />
        <div className="flex flex-1 flex-col overflow-hidden bg-background">
          <Navbar />
          <div className="flex-1 overflow-y-auto">
            {children}
          </div>
        </div>
      </SidebarProvider>
    </RefreshProvider>
  )
}
