"use client"

import { useState } from "react"
import { toast } from "sonner"
import { Globe, Loader2, Sparkles, Plus } from "lucide-react"
import apiClient from "@/lib/axios"
import { useRouter } from "next/navigation"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { BrandDNA } from "@/components/brand-dna-card"

interface BrandRecord {
  id: number
  user_id: number
  url: string
  dna: BrandDNA
  created_at: string
}

export default function DashboardPage() {
  const router = useRouter()
  const [url, setUrl] = useState("")
  const [generating, setGenerating] = useState(false)
  const [insufficientCredits, setInsufficientCredits] = useState(false)

  async function handleGenerate(e: React.FormEvent) {
    e.preventDefault()
    if (!url.trim()) return
    setGenerating(true)
    setInsufficientCredits(false)
    try {
      const res = await apiClient.post<BrandRecord>("/api/brands/generate", {
        url: url.trim(),
      })
      setUrl("")
      toast.success("Brand DNA generated! 1 credit deducted.")
      // Redirect to the new workspace for this brand
      router.push(`/dashboard/brand/${res.data.id}`)
    } catch (err: unknown) {
      const status = (err as { response?: { status?: number } })?.response?.status
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Generation failed"
      if (status === 402) {
        setInsufficientCredits(true)
        toast.error("Insufficient credits")
      } else {
        toast.error(detail)
      }
    } finally {
      setGenerating(false)
    }
  }

  return (
    <main className="mx-auto w-full max-w-5xl px-4 py-20 flex flex-col items-center justify-center min-h-[calc(100svh-3.5rem)] gap-16 relative">
      <section className="relative flex flex-col gap-8 items-center text-center animate-fade-slide-in w-full">
        
        {/* Radial glow background effect matching landing page */}
        <div aria-hidden className="pointer-events-none absolute inset-0 flex items-center justify-center overflow-hidden">
          <div className="h-[400px] w-[600px] rounded-full bg-primary/20 opacity-30 blur-[100px] animate-pulse-glow" />
        </div>

        <div className="flex flex-col gap-3 relative z-10">
          <div className="mx-auto flex items-center justify-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3 py-1.5 text-xs font-medium text-primary">
            <Sparkles className="size-3.5" />
            Analyze any website
          </div>
          <h1 className="font-heading text-4xl font-bold tracking-tight sm:text-5xl text-foreground">
            Brand DNA Generator
          </h1>
          <p className="mx-auto mt-2 text-base text-muted-foreground max-w-xl leading-relaxed">
            Paste a website URL and our AI will extract tone, palette, typography, and personality. 
            One click, complete design foundation.
          </p>
        </div>

        <form
          onSubmit={handleGenerate}
          className="flex w-full max-w-xl items-center gap-2 relative z-10"
        >
          <div className="relative flex-1 group">
            <Globe className="absolute left-3.5 top-1/2 -translate-y-1/2 size-4 text-muted-foreground transition-colors group-focus-within:text-primary pointer-events-none" />
            <Input
              id="url-input"
              type="url"
              placeholder="https://yourcompany.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="pl-10 h-12 rounded-xl border-border bg-card shadow-sm transition-all focus-visible:ring-1 focus-visible:ring-primary focus-visible:border-primary/50 text-base"
              required
              disabled={generating}
            />
          </div>
          <Button 
            type="submit" 
            disabled={generating} 
            className="h-12 rounded-xl gap-2 shrink-0 px-6 font-semibold shadow-md transition-all active:scale-[0.98]"
          >
            {generating ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                Analyzing…
              </>
            ) : (
              <>
                <Plus className="size-4" />
                Generate
              </>
            )}
          </Button>
        </form>

        {insufficientCredits && (
          <Alert variant="destructive" className="max-w-xl text-left relative z-10 animate-fade-in border-destructive/50 bg-destructive/10 text-destructive-foreground">
            <AlertTitle className="font-semibold tracking-wide uppercase font-mono text-[11px]">No credits remaining</AlertTitle>
            <AlertDescription className="text-sm">
              You&apos;ve used all your credits. Top up to continue generating
              Brand DNA reports.
            </AlertDescription>
          </Alert>
        )}
      </section>
    </main>
  )
}
