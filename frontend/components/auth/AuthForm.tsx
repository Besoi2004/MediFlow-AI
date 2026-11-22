"use client";

import { useRouter } from "next/navigation";

import { useAuth } from "@/components/auth/AuthProvider";
import type { User } from "@/lib/api";
import { safeNext } from "@/lib/nav";

// Ô nhập có nhãn và lỗi ngay dưới ô (Review Focus 5).
export function Field({ id, label, error, children }: { id: string; label: string; error?: string; children: React.ReactNode }) {
  return (
    <div className="grid gap-1.5">
      <label htmlFor={id} className="text-sm font-medium">
        {label}
      </label>
      {children}
      {error && (
        <p id={`${id}-error`} className="text-sm text-destructive">
          {error}
        </p>
      )}
    </div>
  );
}

export const invalid = (id: string, error?: string) =>
  error ? { "aria-invalid": true, "aria-describedby": `${id}-error` } : {};

// Đăng nhập/đăng ký xong: tải lại người dùng rồi về trang đang dở (tư vấn viên mặc định về /consultant).
export function useFinishAuth(next: string | null) {
  const router = useRouter();
  const { refresh } = useAuth();
  return async (user: User) => {
    const target = safeNext(next, user.role === "consultant" ? "/consultant" : "/");
    await refresh();
    if (target === "/") window.location.assign(target); // trang chủ nạp bộ giao diện riêng: tải lại cả trang
    else router.push(target);
  };
}
