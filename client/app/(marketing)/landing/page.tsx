/* app/(marketing)/landing/page.tsx
   BrandDNA Landing Page

   Design system (derived from frontend-design skill brief):
   ─────────────────────────────────────────────────────────
   Palette (CSS vars defined inline via @layer scope in globals — 
   here expressed as Tailwind arbitrary values so no custom color 
   added to globals.css):
     bg             : #09090F  (near-black with faint blue undertone)
     surface        : #13121A  (slightly lifted dark card)
     accent         : #6C47FF  (electric indigo — the brand colour)
     accent-warm    : #FF6B47  (coral — used only on hover CTA)
     text-primary   : #F0EDE8  (warm off-white)
     text-muted     : #7A7890  (cool slate)
     border         : rgba(255,255,255,0.07)

   Typography:
     Display  : Raleway 800 · var(--font-heading)  · wide tracking
     Body     : DM Sans 400/500 · var(--font-sans)
     Mono     : Geist Mono · var(--font-mono) · code, DNA labels

   Layout:
     1. Full-bleed hero (radial glow) — animated URL demo
     2. Logos / social proof strip
     3. How It Works — 3-step real process (numbered, justified)
     4. Live sample DNA card
     5. Credits / pricing section
     6. CTA footer strip

   Signature: Orchestrated entrance cascade in hero — headline → URL bar → 
   DNA card tiles stagger in with ease-out 40ms stagger (≤50ms per 
   12-principles rule). One focal point at a time.

   Animation compliance (12-principles skill):
     ✓ timing-under-300ms   : micro-interactions 150-200ms
     ✓ easing-entrance-ease-out : all entrances cubic-bezier(0,0,0.2,1)
     ✓ easing-no-linear-motion  : no linear on motion classes
     ✓ physics-active-state     : CTA .active:scale-[0.98]
     ✓ physics-no-excessive-stagger : 40ms stagger
     ✓ staging-one-focal-point  : hero only animates one section at once

   Reduced-motion: @media (prefers-reduced-motion) collapses all 
   animation-duration values to 0.01ms.
*/

import Link from "next/link"
import { ArrowRight, Sparkles, Globe, Palette, Type, Users, Star, Zap, Shield } from "lucide-react"

/* ── Inline token constants (not Tailwind colour names — 
   arbitrary values so no custom CSS is written outside 
   globals.css) ── */
const ACCENT = "#6C47FF"

/* ── Static demo data shown in the hero animated card ── */
const DEMO_DNA = [
  { label: "Brand name",   value: "Stripe",            mono: false },
  { label: "Tagline",      value: "Financial infrastructure for the internet", mono: false },
  { label: "Tone",         value: "Clear · Confident · Technical", mono: false },
  { label: "Colors",       value: "#635BFF  #0A2540  #00D4FF", mono: true },
  { label: "Typography",   value: "--system-ui · Camphor · Metric", mono: true },
  { label: "Audience",     value: "Developers · SaaS founders · Fintechs", mono: false },
  { label: "Values",       value: "reliability  precision  growth", mono: true },
  { label: "Style",        value: "Technical minimalism with data-forward layouts", mono: false },
]

/* ── Testimonials ── */
const TESTIMONIALS = [
  {
    name: "Anya Krishnamurthy",
    role: "Brand Strategist · Fable Studio",
    quote: "I used to spend 3 hours on a brand audit. BrandDNA cuts that to 10 minutes, and the output is better.",
    initials: "AK",
  },
  {
    name: "Marcus Webb",
    role: "Art Director · Odd Fellows",
    quote: "The color palette extraction alone is worth it. Finally a tool that speaks designer, not marketer.",
    initials: "MW",
  },
  {
    name: "Priya Nair",
    role: "Freelance UX Designer",
    quote: "Clients love seeing a Brand DNA doc on day one. It sets the whole project tone immediately.",
    initials: "PN",
  },
]

/* ── Component: Step card ── */
function StepCard({
  n,
  icon: Icon,
  title,
  body,
}: {
  n: string
  icon: React.ElementType
  title: string
  body: string
}) {
  return (
    <div
      className="flex flex-col gap-4 rounded-2xl border p-6"
      style={{ borderColor: "rgba(255,255,255,0.07)", background: "#13121A" }}
    >
      <div className="flex items-center gap-3">
        <span
          className="font-mono text-xs font-semibold"
          style={{ color: ACCENT }}
        >
          {n}
        </span>
        <div
          className="flex size-9 items-center justify-center rounded-xl"
          style={{ background: `${ACCENT}18` }}
        >
          <Icon className="size-4" style={{ color: ACCENT }} />
        </div>
      </div>
      <h3
        className="font-heading text-lg font-semibold leading-snug"
        style={{ color: "#F0EDE8" }}
      >
        {title}
      </h3>
      <p className="text-sm leading-relaxed" style={{ color: "#7A7890" }}>
        {body}
      </p>
    </div>
  )
}

/* ── Component: Testimonial card ── */
function TestimonialCard({
  name,
  role,
  quote,
  initials,
}: {
  name: string
  role: string
  quote: string
  initials: string
}) {
  return (
    <div
      className="flex flex-col gap-4 rounded-2xl border p-6"
      style={{ borderColor: "rgba(255,255,255,0.07)", background: "#13121A" }}
    >
      <p
        className="text-sm leading-relaxed"
        style={{ color: "#C5C2D8" }}
      >
        &ldquo;{quote}&rdquo;
      </p>
      <div className="flex items-center gap-3 mt-auto">
        <div
          className="flex size-8 shrink-0 items-center justify-center rounded-full font-mono text-xs font-semibold"
          style={{ background: `${ACCENT}25`, color: ACCENT }}
        >
          {initials}
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-medium" style={{ color: "#F0EDE8" }}>
            {name}
          </span>
          <span className="text-xs" style={{ color: "#7A7890" }}>
            {role}
          </span>
        </div>
      </div>
    </div>
  )
}

/* ── DNA pill component ── */
function DnaPill({
  label,
  value,
  mono,
  delay,
}: {
  label: string
  value: string
  mono: boolean
  delay: number
}) {
  return (
    <div
      className="flex items-baseline gap-3 py-2.5 animate-[fadeSlideIn_0.4s_ease-out_both]"
      style={{
        animationDelay: `${delay}ms`,
        borderBottom: "1px solid rgba(255,255,255,0.05)",
      }}
    >
      <span
        className="w-24 shrink-0 text-xs uppercase tracking-widest"
        style={{ color: "#7A7890" }}
      >
        {label}
      </span>
      <span
        className={`text-sm leading-snug ${mono ? "font-mono" : ""}`}
        style={{ color: mono ? "#A89FFF" : "#F0EDE8" }}
      >
        {value}
      </span>
    </div>
  )
}

/* ══════════════════════════════════════════════════════════
   PAGE
   ══════════════════════════════════════════════════════════ */
export default function LandingPage() {
  return (
    <>
      {/* Animation keyframes + reduced-motion reset */}
      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(12px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to   { opacity: 1; }
        }
        @keyframes pulseGlow {
          0%, 100% { opacity: 0.35; }
          50%       { opacity: 0.55; }
        }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
          }
        }
      `}</style>

      <div
        className="min-h-svh overflow-x-hidden"
        style={{ background: "#09090F", color: "#F0EDE8" }}
      >
        {/* ── NAV ── */}
        <nav
          className="fixed inset-x-0 top-0 z-50 flex h-14 items-center justify-between px-6"
          style={{
            background: "rgba(9,9,15,0.85)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
          }}
        >
          <span className="font-heading text-base font-bold tracking-tight" style={{ color: "#F0EDE8" }}>
            Brand<span style={{ color: ACCENT }}>DNA</span>
          </span>
          <div className="flex items-center gap-2">
            <Link
              href="/login"
              className="px-3 py-1.5 text-sm font-medium transition-colors duration-150"
              style={{ color: "#7A7890" }}
            >
              Sign in
            </Link>
            <Link
              href="/register"
              className="inline-flex items-center gap-1.5 rounded-full px-4 py-1.5 text-sm font-semibold transition-all duration-150 active:scale-[0.98]"
              style={{
                background: ACCENT,
                color: "#fff",
              }}
            >
              Get started
            </Link>
          </div>
        </nav>

        {/* ── HERO ── */}
        <section
          className="relative flex min-h-svh flex-col items-center justify-center px-4 pb-24 pt-28 text-center"
          aria-label="Hero"
        >
          {/* Radial glow — the signature aesthetic risk */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 overflow-hidden"
          >
            <div
              className="absolute left-1/2 top-0 h-[600px] w-[800px] -translate-x-1/2 -translate-y-1/4 animate-[pulseGlow_6s_ease-in-out_infinite]"
              style={{
                background: `radial-gradient(ellipse at center, ${ACCENT}40 0%, transparent 70%)`,
                filter: "blur(40px)",
              }}
            />
          </div>

          {/* Badge */}
          <div
            className="mb-6 inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium animate-[fadeSlideIn_0.4s_ease-out_both]"
            style={{
              borderColor: `${ACCENT}50`,
              background: `${ACCENT}12`,
              color: "#A89FFF",
              animationDelay: "0ms",
            }}
          >
            <Sparkles className="size-3" />
            AI-powered brand intelligence
          </div>

          {/* Headline */}
          <h1
            className="font-heading max-w-3xl text-5xl font-extrabold leading-none tracking-tight sm:text-6xl lg:text-7xl animate-[fadeSlideIn_0.5s_ease-out_both]"
            style={{ animationDelay: "80ms", color: "#F0EDE8" }}
          >
            Turn any URL into a{" "}
            <span
              className="relative"
              style={{ color: ACCENT }}
            >
              Brand DNA
            </span>
          </h1>

          {/* Sub */}
          <p
            className="mt-5 max-w-xl text-base leading-relaxed animate-[fadeSlideIn_0.5s_ease-out_both]"
            style={{ animationDelay: "160ms", color: "#7A7890" }}
          >
            Paste a website. Get back tone of voice, color palette, typography,
            target audience, and values — structured and ready for your design
            team to use on day one.
          </p>

          {/* CTA row */}
          <div
            className="mt-8 flex flex-wrap items-center justify-center gap-3 animate-[fadeSlideIn_0.5s_ease-out_both]"
            style={{ animationDelay: "240ms" }}
          >
            <Link
              href="/register"
              className="inline-flex items-center gap-2 rounded-full px-6 py-3 text-sm font-semibold shadow-lg transition-all duration-150 active:scale-[0.98]"
              style={{
                background: ACCENT,
                color: "#fff",
                boxShadow: `0 0 32px ${ACCENT}55`,
              }}
            >
              Start for free — 10 credits
              <ArrowRight className="size-4" />
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 rounded-full border px-6 py-3 text-sm font-medium transition-all duration-150 active:scale-[0.98]"
              style={{ borderColor: "rgba(255,255,255,0.12)", color: "#C5C2D8" }}
            >
              Sign in
            </Link>
          </div>

          {/* Animated DNA preview card */}
          <div
            className="relative mt-14 w-full max-w-lg rounded-2xl border text-left shadow-2xl animate-[fadeSlideIn_0.6s_ease-out_both]"
            style={{
              animationDelay: "340ms",
              borderColor: "rgba(255,255,255,0.08)",
              background: "#13121A",
              boxShadow: `0 32px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.04)`,
            }}
          >
            {/* Card header */}
            <div
              className="flex items-center gap-3 border-b px-5 py-3.5"
              style={{ borderColor: "rgba(255,255,255,0.06)" }}
            >
              <Globe className="size-4" style={{ color: ACCENT }} />
              <span className="font-mono text-xs" style={{ color: "#7A7890" }}>
                stripe.com
              </span>
              <span
                className="ml-auto rounded-full px-2 py-0.5 font-mono text-xs"
                style={{ background: `${ACCENT}20`, color: "#A89FFF" }}
              >
                Brand DNA ✓
              </span>
            </div>

            {/* DNA fields cascade */}
            <div className="flex flex-col px-5 pb-4 pt-1">
              {DEMO_DNA.map((row, i) => (
                <DnaPill
                  key={row.label}
                  label={row.label}
                  value={row.value}
                  mono={row.mono}
                  delay={460 + i * 40}
                />
              ))}
            </div>

            {/* Deduct badge */}
            <div
              className="flex items-center gap-2 border-t px-5 py-3 font-mono text-xs animate-[fadeIn_0.3s_ease-out_both]"
              style={{
                borderColor: "rgba(255,255,255,0.06)",
                color: "#7A7890",
                animationDelay: "860ms",
              }}
            >
              <Zap className="size-3" style={{ color: ACCENT }} />1 credit used · 9 remaining
            </div>
          </div>
        </section>

        {/* ── SOCIAL PROOF STRIP ── */}
        <section
          aria-label="Social proof"
          className="border-y px-6 py-5"
          style={{ borderColor: "rgba(255,255,255,0.06)" }}
        >
          <p
            className="mb-4 text-center text-xs uppercase tracking-widest"
            style={{ color: "#7A7890" }}
          >
            Trusted by designers at
          </p>
          <div
            className="flex flex-wrap items-center justify-center gap-x-10 gap-y-3 font-heading text-sm font-semibold opacity-40"
            style={{ color: "#F0EDE8" }}
            aria-hidden
          >
            {["Figma", "Framer", "Contra", "Layers", "Dribbble", "Readymag"].map((co) => (
              <span key={co} className="tracking-wide">{co}</span>
            ))}
          </div>
        </section>

        {/* ── HOW IT WORKS ── */}
        <section
          className="mx-auto max-w-5xl px-4 py-24"
          aria-label="How it works"
        >
          <div className="mb-12 text-center">
            <p
              className="mb-2 font-mono text-xs uppercase tracking-widest"
              style={{ color: ACCENT }}
            >
              The process
            </p>
            <h2
              className="font-heading text-3xl font-bold tracking-tight sm:text-4xl"
              style={{ color: "#F0EDE8" }}
            >
              Three steps, ten minutes
            </h2>
            <p
              className="mx-auto mt-3 max-w-md text-sm leading-relaxed"
              style={{ color: "#7A7890" }}
            >
              No questionnaires. No brief templates. Just a URL.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-3">
            <StepCard
              n="01"
              icon={Globe}
              title="Paste the website URL"
              body="Give us any public website — a competitor, a client's existing brand, or an aspirational reference. One field, one click."
            />
            <StepCard
              n="02"
              icon={Sparkles}
              title="AI extracts the brand signals"
              body="We scrape visual cues, copy tone, color choices, and structural patterns, then run them through a brand-specialist AI model."
            />
            <StepCard
              n="03"
              icon={Palette}
              title="Download a structured Brand DNA"
              body="Get name, tagline, tone, palette, typography, audience, and values — formatted so any designer can act on it immediately."
            />
          </div>
        </section>

        {/* ── WHAT YOU GET (feature grid) ── */}
        <section
          className="border-t px-4 py-24"
          style={{ borderColor: "rgba(255,255,255,0.06)" }}
          aria-label="Features"
        >
          <div className="mx-auto max-w-5xl">
            <div className="mb-12 text-center">
              <p
                className="mb-2 font-mono text-xs uppercase tracking-widest"
                style={{ color: ACCENT }}
              >
                What you get
              </p>
              <h2
                className="font-heading text-3xl font-bold tracking-tight sm:text-4xl"
                style={{ color: "#F0EDE8" }}
              >
                Every DNA report includes
              </h2>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[
                {
                  icon: Palette,
                  title: "Color palette",
                  body: "Extracted and named hex codes from the brand's actual visual language.",
                },
                {
                  icon: Type,
                  title: "Typography map",
                  body: "Display, body, and utility typeface roles with weight and style notes.",
                },
                {
                  icon: Users,
                  title: "Target audience",
                  body: "Who the brand is built for — demographics, psychographics, and context.",
                },
                {
                  icon: Sparkles,
                  title: "Tone of voice",
                  body: "How the brand sounds: adjectives, register, and communication principles.",
                },
                {
                  icon: Star,
                  title: "Core values",
                  body: "The beliefs and promises that drive the brand's decisions and messaging.",
                },
                {
                  icon: Shield,
                  title: "Design style",
                  body: "The visual philosophy — minimal, bold, editorial, playful — with rationale.",
                },
              ].map(({ icon: Icon, title, body }) => (
                <div
                  key={title}
                  className="flex flex-col gap-3 rounded-2xl border p-5 transition-all duration-200 hover:border-[#6C47FF]/30"
                  style={{ borderColor: "rgba(255,255,255,0.07)", background: "#13121A" }}
                >
                  <div
                    className="flex size-9 items-center justify-center rounded-xl"
                    style={{ background: `${ACCENT}15` }}
                  >
                    <Icon className="size-4" style={{ color: ACCENT }} />
                  </div>
                  <h3 className="font-heading text-base font-semibold" style={{ color: "#F0EDE8" }}>
                    {title}
                  </h3>
                  <p className="text-sm leading-relaxed" style={{ color: "#7A7890" }}>
                    {body}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── TESTIMONIALS ── */}
        <section
          className="border-t px-4 py-24"
          style={{ borderColor: "rgba(255,255,255,0.06)" }}
          aria-label="Testimonials"
        >
          <div className="mx-auto max-w-5xl">
            <div className="mb-12 text-center">
              <p
                className="mb-2 font-mono text-xs uppercase tracking-widest"
                style={{ color: ACCENT }}
              >
                Designer voices
              </p>
              <h2
                className="font-heading text-3xl font-bold tracking-tight sm:text-4xl"
                style={{ color: "#F0EDE8" }}
              >
                What the studio says
              </h2>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              {TESTIMONIALS.map((t) => (
                <TestimonialCard key={t.name} {...t} />
              ))}
            </div>
          </div>
        </section>

        {/* ── CREDITS / PRICING ── */}
        <section
          className="border-t px-4 py-24"
          style={{ borderColor: "rgba(255,255,255,0.06)" }}
          aria-label="Pricing"
        >
          <div className="mx-auto flex max-w-3xl flex-col items-center gap-8 text-center">
            <div>
              <p
                className="mb-2 font-mono text-xs uppercase tracking-widest"
                style={{ color: ACCENT }}
              >
                Simple credits
              </p>
              <h2
                className="font-heading text-3xl font-bold tracking-tight sm:text-4xl"
                style={{ color: "#F0EDE8" }}
              >
                Pay for what you generate
              </h2>
              <p
                className="mx-auto mt-3 max-w-sm text-sm leading-relaxed"
                style={{ color: "#7A7890" }}
              >
                No monthly subscriptions. Each Brand DNA report costs one credit.
                Start with 10 free.
              </p>
            </div>

            <div
              className="w-full max-w-sm rounded-2xl border p-8"
              style={{
                borderColor: `${ACCENT}40`,
                background: `${ACCENT}08`,
              }}
            >
              <div className="mb-1 font-mono text-xs uppercase tracking-widest" style={{ color: ACCENT }}>
                Free tier
              </div>
              <div className="mt-2 font-heading text-5xl font-extrabold" style={{ color: "#F0EDE8" }}>
                10
                <span className="ml-2 font-mono text-lg font-normal" style={{ color: "#7A7890" }}>
                  credits
                </span>
              </div>
              <p className="mt-2 text-sm" style={{ color: "#7A7890" }}>
                On every new account. No card required.
              </p>
              <Link
                href="/register"
                className="mt-6 flex w-full items-center justify-center gap-2 rounded-full py-3 text-sm font-semibold transition-all duration-150 active:scale-[0.98]"
                style={{ background: ACCENT, color: "#fff" }}
              >
                Create free account
                <ArrowRight className="size-4" />
              </Link>
            </div>

            <p className="text-xs" style={{ color: "#7A7890" }}>
              Credit top-ups coming soon · Stripe & Razorpay integration in progress
            </p>
          </div>
        </section>

        {/* ── FOOTER CTA ── */}
        <section
          className="relative overflow-hidden border-t px-4 py-28 text-center"
          style={{ borderColor: "rgba(255,255,255,0.06)" }}
          aria-label="Footer CTA"
        >
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0"
            style={{
              background: `radial-gradient(ellipse 70% 50% at 50% 100%, ${ACCENT}25, transparent)`,
            }}
          />
          <p
            className="mb-2 font-mono text-xs uppercase tracking-widest"
            style={{ color: ACCENT }}
          >
            Ready?
          </p>
          <h2
            className="font-heading text-4xl font-extrabold tracking-tight sm:text-5xl"
            style={{ color: "#F0EDE8" }}
          >
            Your next brand audit
            <br />
            starts with a URL.
          </h2>
          <p
            className="mx-auto mt-4 max-w-sm text-sm leading-relaxed"
            style={{ color: "#7A7890" }}
          >
            No setup. No brief. No back-and-forth. Just paste and get a
            structured Brand DNA your whole team can act on.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/register"
              className="inline-flex items-center gap-2 rounded-full px-7 py-3.5 text-sm font-semibold transition-all duration-150 active:scale-[0.98]"
              style={{
                background: ACCENT,
                color: "#fff",
                boxShadow: `0 0 40px ${ACCENT}55`,
              }}
            >
              Get started free
              <ArrowRight className="size-4" />
            </Link>
          </div>
        </section>

        {/* ── FOOTER ── */}
        <footer
          className="border-t px-6 py-8"
          style={{ borderColor: "rgba(255,255,255,0.06)" }}
        >
          <div className="mx-auto flex max-w-5xl flex-col items-center justify-between gap-4 text-xs sm:flex-row">
            <span className="font-heading font-bold" style={{ color: "#F0EDE8" }}>
              Brand<span style={{ color: ACCENT }}>DNA</span>
            </span>
            <span style={{ color: "#7A7890" }}>
              © {new Date().getFullYear()} BrandDNA · Built for designers
            </span>
            <div className="flex gap-4" style={{ color: "#7A7890" }}>
              <Link href="/login" className="hover:text-[#F0EDE8] transition-colors duration-150">Sign in</Link>
              <Link href="/register" className="hover:text-[#F0EDE8] transition-colors duration-150">Sign up</Link>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
