"use client";

import { MenuIcon } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { useAuth } from "@/components/auth/AuthProvider";
import { Button, buttonVariants } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from "@/components/ui/sheet";

export function SiteHeader() {
  const { user, loading, logout } = useAuth();
  const [open, setOpen] = useState(false);

  const links = [
    { href: "/hospitals", label: "Bệnh viện" },
    { href: "/packages", label: "Gói khám" },
    ...(user?.role === "customer" ? [{ href: "/bookings", label: "Lịch của tôi" }] : []),
    ...(user?.role === "consultant" ? [{ href: "/consultant", label: "Tư vấn viên" }] : []),
  ];

  async function onLogout() {
    setOpen(false);
    await logout();
    window.location.reload(); // trang cần đăng nhập sẽ được proxy chuyển về /login
  }

  const account = loading ? null : user ? (
    <>
      <span className="truncate text-base">{user.full_name}</span>
      <Button variant="outline" onClick={onLogout}>
        Đăng xuất
      </Button>
    </>
  ) : (
    <Link className={buttonVariants()} href="/login" onClick={() => setOpen(false)}>
      Đăng nhập
    </Link>
  );

  return (
    <header className="sticky top-0 z-40 border-b bg-background">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center gap-6 px-4">
        {/* Trang chủ dùng bộ giao diện riêng của taste-skill: cần tải lại cả trang, nên không dùng <Link> */}
        {/* eslint-disable-next-line @next/next/no-html-link-for-pages */}
        <a href="/" className="font-heading text-xl font-medium tracking-tight">
          MediFlow
        </a>
        <nav aria-label="Chính" className="hidden flex-1 items-center gap-1 md:flex">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className={buttonVariants({ variant: "ghost" })}>
              {l.label}
            </Link>
          ))}
        </nav>
        <div className="hidden min-w-0 items-center gap-3 md:flex">{account}</div>
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger render={<Button variant="ghost" size="icon" className="ml-auto md:hidden" aria-label="Mở menu" />}>
            <MenuIcon />
          </SheetTrigger>
          <SheetContent side="right" className="gap-2 p-6 pt-14">
            <SheetTitle className="sr-only">Menu</SheetTitle>
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                onClick={() => setOpen(false)}
                className="flex h-14 items-center border-b text-lg"
              >
                {l.label}
              </Link>
            ))}
            <div className="mt-4 flex flex-col items-start gap-3">{account}</div>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
