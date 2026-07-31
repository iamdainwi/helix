// app/page.tsx
// Root: unauthenticated users see the landing page.
// Authenticated users are redirected to /dashboard by the dashboard's own client guard.
// We don't do a server-side redirect here so the landing is public and crawlable.

export { default } from "./(marketing)/landing/page"
