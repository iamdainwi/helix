// components/navbar.tsx
// Top navigation bar — shows credits balance and logout button.
// Uses only shadcn components + CSS variable classes.

"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { Coins, LogOut } from "lucide-react"
import { toast } from "sonner"
import apiClient from "@/lib/axios"
import { useAuth } from "@/hooks/use-auth"
import { useRefresh } from "@/hooks/use-refresh"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

export function Navbar() {
  const router = useRouter()
  const { isAuthenticated, clearToken } = useAuth()
  const { refreshKey } = useRefresh()
  const [balance, setBalance] = useState<number | null>(null)

  useEffect(() => {
    if (!isAuthenticated) return
    apiClient
      .get("/api/credits/balance")
      .then((res) => setBalance(res.data.balance))
      .catch(() => setBalance(null))
  }, [isAuthenticated, refreshKey])

  function handleLogout() {
    clearToken()
    toast.success("Logged out")
    router.push("/login")
  }

  return (
    <header className="border-b border-border/50 bg-card z-10 sticky top-0">
      <div className="flex h-14 w-full items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <SidebarTrigger />
          <Link href="/dashboard" className="font-heading text-lg font-semibold md:hidden">
            BrandDNA
          </Link>
        </div>

        {isAuthenticated && (
          <div className="flex items-center gap-3">
            <Badge variant="secondary" className="gap-1.5 text-xs">
              <Coins className="size-3" />
              {balance !== null ? `${balance} credits` : "…"}
            </Badge>
            <Separator orientation="vertical" className="h-5" />
            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              className="gap-1.5"
            >
              <LogOut className="size-4" />
              Sign out
            </Button>
          </div>
        )}
      </div>
    </header>
  )
}
