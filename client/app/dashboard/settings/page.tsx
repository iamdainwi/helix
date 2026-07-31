"use client"

import { useEffect, useState } from "react"
import { toast } from "sonner"
import { Loader2, Settings2, UserCircle, KeyRound, CalendarDays, Coins } from "lucide-react"
import apiClient from "@/lib/axios"
import { useAuth } from "@/hooks/use-auth"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from "@/components/ui/card"

interface UserProfile {
  id: number
  email: string
  is_active: boolean
  created_at: string
}

export default function SettingsPage() {
  const { isAuthenticated } = useAuth()
  
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [balance, setBalance] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [updating, setUpdating] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) return

    Promise.all([
      apiClient.get<UserProfile>("/api/users/me"),
      apiClient.get<{ balance: number }>("/api/credits/balance")
    ])
      .then(([profileRes, creditRes]) => {
        setProfile(profileRes.data)
        setEmail(profileRes.data.email)
        setBalance(creditRes.data.balance)
      })
      .catch(() => {
        toast.error("Failed to load profile data")
      })
      .finally(() => setLoading(false))
  }, [isAuthenticated])

  async function handleUpdateProfile(e: React.FormEvent) {
    e.preventDefault()
    if (!email.trim()) {
      toast.error("Email cannot be empty")
      return
    }

    setUpdating(true)
    try {
      const payload: any = { email: email.trim() }
      if (password) {
        payload.password = password
      }

      const res = await apiClient.put<UserProfile>("/api/users/me", payload)
      setProfile(res.data)
      setPassword("") // Clear password field on success
      toast.success("Profile updated successfully")
    } catch (err: unknown) {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Failed to update profile"
      toast.error(detail)
    } finally {
      setUpdating(false)
    }
  }

  if (loading) {
    return (
      <div className="mx-auto w-full max-w-3xl px-4 py-8 flex flex-col gap-8">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-[300px] w-full rounded-xl" />
      </div>
    )
  }

  if (!profile) return null

  const joinDate = new Date(profile.created_at).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8 flex flex-col gap-8 animate-fade-in">
      <div className="flex flex-col gap-1">
        <h1 className="font-heading text-3xl font-bold flex items-center gap-2">
          <Settings2 className="size-6 text-primary" />
          Settings
        </h1>
        <p className="text-muted-foreground">
          Manage your account details and view your credit balance.
        </p>
      </div>

      <div className="grid gap-6">
        
        {/* Account Details Card */}
        <Card className="bg-card">
          <CardHeader>
            <CardTitle className="text-xl">Account Overview</CardTitle>
            <CardDescription>A quick glance at your account status.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-6">
            <div className="flex items-center gap-4 p-4 rounded-xl border border-border/50 bg-muted/20">
              <div className="flex size-10 items-center justify-center rounded-full bg-primary/20 text-primary">
                <Coins className="size-5" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-medium text-muted-foreground">Credit Balance</span>
                <span className="text-2xl font-bold font-heading">{balance ?? 0}</span>
              </div>
            </div>
            
            <div className="flex items-center gap-4 p-4 rounded-xl border border-border/50 bg-muted/20">
              <div className="flex size-10 items-center justify-center rounded-full bg-primary/20 text-primary">
                <CalendarDays className="size-5" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-medium text-muted-foreground">Member Since</span>
                <span className="text-base font-semibold">{joinDate}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Profile Edit Card */}
        <Card className="bg-card">
          <CardHeader>
            <CardTitle className="text-xl">Edit Profile</CardTitle>
            <CardDescription>Update your email address or change your password.</CardDescription>
          </CardHeader>
          <form onSubmit={handleUpdateProfile}>
            <CardContent className="flex flex-col gap-6">
              <div className="flex flex-col gap-3">
                <Label htmlFor="email" className="flex items-center gap-2">
                  <UserCircle className="size-4 text-muted-foreground" />
                  Email Address
                </Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={updating}
                  required
                />
              </div>

              <div className="flex flex-col gap-3">
                <Label htmlFor="password" className="flex items-center gap-2">
                  <KeyRound className="size-4 text-muted-foreground" />
                  New Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Leave blank to keep current password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={updating}
                  minLength={8}
                />
              </div>
            </CardContent>
            <CardFooter className="border-t border-border/50 px-6 py-4">
              <Button type="submit" disabled={updating} className="w-full sm:w-auto active:scale-[0.98]">
                {updating ? (
                  <>
                    <Loader2 className="mr-2 size-4 animate-spin" />
                    Saving Changes...
                  </>
                ) : (
                  "Save Changes"
                )}
              </Button>
            </CardFooter>
          </form>
        </Card>

      </div>
    </main>
  )
}
