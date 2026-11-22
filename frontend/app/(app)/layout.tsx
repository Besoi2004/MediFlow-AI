import "../globals.css";

import { SiteHeader } from "@/components/SiteHeader";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-svh bg-background font-sans text-foreground antialiased">
      <SiteHeader />
      <main className="mx-auto max-w-6xl px-4 py-6">{children}</main>
    </div>
  );
}
