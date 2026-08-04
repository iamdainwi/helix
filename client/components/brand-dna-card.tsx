"use client"
// components/brand-dna-card.tsx
// Renders a structured Brand DNA result using shadcn Card + Badge + Separator.
// Follows BrandDNA aesthetic: mono tags, intentional typography, distinct hierarchy.

import { Globe, Download } from "lucide-react"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import apiClient from "@/lib/axios"
import { toast } from "sonner"

export interface BrandDNA {
  brand_name: string
  tagline: string
  tone_of_voice: string
  brand_personality: string[]
  color_palette: string[]
  primary_color?: string
  typography: string
  audience: string
  values: string[]
  design_style: string
  logo_url?: string
}

interface BrandDNACardProps {
  id: string
  url: string
  dna: BrandDNA
  createdAt: string
  delayMs?: number
}

function Section({ label, children, className = "" }: { label: string; children: React.ReactNode; className?: string }) {
  return (
    <div className={`flex flex-col gap-2 ${className}`}>
      <p className="font-mono text-[11px] font-semibold text-primary uppercase tracking-widest">
        {label}
      </p>
      {children}
    </div>
  )
}

function TagList({ items }: { items: string[] }) {
  if (!items || items.length === 0) return <span className="text-sm text-muted-foreground italic">None</span>
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((item) => (
        <Badge key={item} variant="secondary" className="font-mono text-[11px] font-medium tracking-wide">
          {item}
        </Badge>
      ))}
    </div>
  )
}

function ColorSwatch({ color }: { color: string }) {
  // Only inline style for the color dot — no Tailwind custom color
  return (
    <div className="flex items-center gap-2.5 text-sm">
      <span
        className="size-5 rounded-full border border-border shrink-0 shadow-inner"
        style={{ backgroundColor: color }}
        aria-label={color}
      />
      <span className="font-mono text-xs text-muted-foreground uppercase tracking-widest">{color}</span>
    </div>
  )
}

export function BrandDNACard({ id, url, dna, createdAt, delayMs = 0 }: BrandDNACardProps) {
  const date = new Date(createdAt).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })

  return (
    <Card
      className="w-full transition-all duration-300 hover:border-primary/40 animate-fade-slide-in relative overflow-hidden"
      style={{ animationDelay: `${delayMs}ms` }}
    >
      {/* Subtle top border accent */}
      <div className="absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-primary/50 to-transparent" />

      <CardHeader className="pb-5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex flex-col gap-1.5 min-w-0">
            <CardTitle className="font-heading text-2xl font-bold tracking-tight">{dna.brand_name}</CardTitle>
            <CardDescription className="text-sm italic leading-relaxed text-muted-foreground/80">
              &ldquo;{dna.tagline}&rdquo;
            </CardDescription>
          </div>
          {dna.logo_url && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={dna.logo_url}
              alt={`${dna.brand_name} logo`}
              className="size-14 rounded-lg object-contain border border-border bg-background/50 p-2"
            />
          )}
          <Button 
            variant="outline" 
            size="sm" 
            className="ml-auto shrink-0 h-9 gap-2"
            onClick={async () => {
              const toastId = toast.loading("Generating PDF…")
              try {
                const response = await apiClient.get(`/api/brands/${id}/pdf`, {
                  responseType: 'blob'
                })
                const blobUrl = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')
                link.href = blobUrl
                link.setAttribute('download', `${dna.brand_name.replace(/\s+/g, '_')}_brand_dna.pdf`)
                document.body.appendChild(link)
                link.click()
                link.remove()
                window.URL.revokeObjectURL(blobUrl)
                toast.success("PDF exported successfully!", { id: toastId })
              } catch {
                toast.error("Failed to export PDF. Please try again.", { id: toastId })
              }
            }}
          >
            <Download className="size-4" />
            Export PDF
          </Button>
        </div>

        <div className="flex items-center gap-2 mt-2 font-mono text-[11px] text-muted-foreground uppercase tracking-wider">
          <Globe className="size-3 shrink-0 text-primary" />
          <Link href={url} className="truncate hover:text-primary transition-colors" target="_blank">{url}</Link>
          <span className="shrink-0 opacity-50">·</span>
          <span className="shrink-0">{date}</span>
        </div>
      </CardHeader>

      <Separator />

      <CardContent className="grid gap-x-8 gap-y-7 pt-6 sm:grid-cols-2 lg:grid-cols-3">
        <Section label="Tone of Voice">
          <p className="text-sm leading-relaxed text-foreground/90">{dna.tone_of_voice}</p>
        </Section>

        <Section label="Design Style">
          <p className="text-sm leading-relaxed text-foreground/90">{dna.design_style}</p>
        </Section>

        <Section label="Typography">
          <p className="text-sm leading-relaxed text-foreground/90">{dna.typography}</p>
        </Section>

        <Section label="Target Audience" className="sm:col-span-2 lg:col-span-1">
          <p className="text-sm leading-relaxed text-foreground/90">{dna.audience}</p>
        </Section>

        <Section label="Brand Personality">
          <TagList items={dna.brand_personality ?? []} />
        </Section>

        <Section label="Core Values">
          <TagList items={dna.values ?? []} />
        </Section>

        <Section label="Color Palette" className="sm:col-span-2 lg:col-span-3">
          <div className="flex flex-wrap gap-x-6 gap-y-3">
            {(dna.color_palette ?? []).map((c) => (
              <ColorSwatch key={c} color={c} />
            ))}
          </div>
        </Section>
      </CardContent>
    </Card>
  )
}
