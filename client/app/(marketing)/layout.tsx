/* app/(marketing)/layout.tsx
   Marketing layout — no navbar, just full-bleed dark pages.
*/
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <>{children}</>
}
