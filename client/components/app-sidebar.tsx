"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { Sparkles, Plus, LayoutDashboard, Loader2, Settings, Trash2 } from "lucide-react"
import apiClient from "@/lib/axios"
import { useAuth } from "@/hooks/use-auth"
import { BrandDNA } from "@/components/brand-dna-card"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuAction,
} from "@/components/ui/sidebar"

interface BrandRecord {
  id: number
  user_id: number
  url: string
  dna: BrandDNA
  created_at: string
}

export function AppSidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { isAuthenticated } = useAuth()
  const [brands, setBrands] = useState<BrandRecord[]>([])
  const [loading, setLoading] = useState(true)

  const fetchBrands = () => {
    apiClient
      .get<BrandRecord[]>("/api/brands")
      .then((res) => setBrands(res.data))
      .catch(() => { })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    if (!isAuthenticated) return
    fetchBrands()
  }, [isAuthenticated])

  const handleDelete = async (e: React.MouseEvent, brandId: number) => {
    e.preventDefault()
    e.stopPropagation()

    const confirmDelete = window.confirm("Are you sure you want to delete this brand kit?")
    if (!confirmDelete) return

    try {
      await apiClient.delete(`/api/brands/${brandId}`)
      setBrands((prev) => prev.filter((b) => b.id !== brandId))

      if (pathname === `/dashboard/brand/${brandId}`) {
        router.push("/dashboard")
      }
    } catch (error) {
      console.error("Failed to delete brand", error)
      alert("Failed to delete brand. Please try again.")
    }
  }

  return (
    <Sidebar className="border-r border-border/50 bg-card">
      <SidebarHeader className="border-b border-border/50 px-4 py-4">
        <Link href="/dashboard" className="flex items-center gap-2 font-heading text-lg font-bold">
          <div className="flex size-6 items-center justify-center rounded bg-primary/20 text-primary">
            <Sparkles className="size-3.5" />
          </div>
          BrandDNA
        </Link>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Main</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  render={<Link href="/dashboard" />}
                  isActive={pathname === "/dashboard"}
                >
                  <Plus className="size-4" />
                  <span>New Brand DNA</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton
                  render={<Link href="/dashboard/settings" />}
                  isActive={pathname.startsWith("/dashboard/settings")}
                >
                  <Settings className="size-4" />
                  <span>Settings</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Your Brands</SidebarGroupLabel>
          <SidebarGroupContent>
            {loading ? (
              <div className="flex items-center gap-2 px-4 py-2 text-sm text-muted-foreground">
                <Loader2 className="size-3 animate-spin" />
                Loading...
              </div>
            ) : brands.length === 0 ? (
              <div className="px-4 py-2 text-xs text-muted-foreground">
                No brands generated yet.
              </div>
            ) : (
              <SidebarMenu>
                {brands.map((brand) => (
                  <SidebarMenuItem key={brand.id}>
                    <SidebarMenuButton
                      render={<Link href={`/dashboard/brand/${brand.id}`} />}
                      isActive={pathname.startsWith(`/dashboard/brand/${brand.id}`)}
                    >
                      <LayoutDashboard className="size-4" />
                      <span className="truncate">{brand.dna.brand_name}</span>
                    </SidebarMenuButton>
                    <SidebarMenuAction
                      onClick={(e) => handleDelete(e, brand.id)}
                      title="Delete brand"
                    >
                      <Trash2 className="size-3.5 text-muted-foreground hover:text-destructive" />
                    </SidebarMenuAction>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            )}
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
