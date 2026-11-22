"use client";

import { useAuth } from "@/components/auth/AuthProvider";

// Chữ thứ hai trên thanh điều hướng của trang chủ: đăng nhập, hoặc trang của người đã đăng nhập.
export function HomeAccountLink() {
  const { user } = useAuth();
  const link =
    user?.role === "consultant"
      ? { href: "/consultant", label: "Tư vấn viên" }
      : user
        ? { href: "/bookings", label: "Lịch của tôi" }
        : { href: "/login", label: "Đăng nhập" };
  return (
    <a className="nav__link" href={link.href}>
      {link.label}
    </a>
  );
}
