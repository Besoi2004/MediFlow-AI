"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useLayoutEffect, useRef, useState } from "react";

import { Field, invalid, useFinishAuth } from "@/components/auth/AuthForm";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api, ApiError, type User } from "@/lib/api";

export function LoginView() {
  const next = useSearchParams().get("next");
  const finish = useFinishAuth(next);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [pending, setPending] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  const done = useRef(false);

  // cacheComponents giữ trang đã rời (Activity): đăng nhập xong mà quay lại /login (401) thì form phải mới, không kẹt
  // "Đang đăng nhập…" với mật khẩu cũ. Cleanup chạy khi trang bị ẩn; chưa gửi xong thì giữ chữ đang gõ dở.
  useLayoutEffect(() => {
    const form = formRef.current;
    return () => {
      if (!done.current) return;
      done.current = false;
      form?.reset();
      setPending(false);
      setError(null);
      setFieldErrors({});
    };
  }, []);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    setPending(true);
    setError(null);
    setFieldErrors({});
    try {
      const user = await api<User>("/auth/login", {
        method: "POST",
        json: { email: form.get("email") || undefined, password: form.get("password") || undefined },
      });
      done.current = true;
      await finish(user);
    } catch (err) {
      const e = err instanceof ApiError ? err : new ApiError(0, "Có lỗi xảy ra");
      setFieldErrors(e.fieldErrors);
      if (Object.keys(e.fieldErrors).length === 0) setError(e.message);
      setPending(false);
    }
  }

  const query = next ? `?next=${encodeURIComponent(next)}` : "";
  return (
    <div className="mx-auto max-w-md py-6">
      <h1 className="font-heading text-3xl font-medium tracking-tight">Đăng nhập</h1>
      <form ref={formRef} onSubmit={onSubmit} noValidate className="mt-6 grid gap-4 rounded-2xl border bg-card p-6">
        <Field id="email" label="Email" error={fieldErrors.email}>
          <Input id="email" name="email" type="email" autoComplete="email" required {...invalid("email", fieldErrors.email)} />
        </Field>
        <Field id="password" label="Mật khẩu" error={fieldErrors.password}>
          <Input id="password" name="password" type="password" autoComplete="current-password" required {...invalid("password", fieldErrors.password)} />
        </Field>
        {error && (
          <p role="alert" className="text-sm text-destructive">
            {error}
          </p>
        )}
        <Button type="submit" disabled={pending}>
          {pending ? "Đang đăng nhập…" : "Đăng nhập"}
        </Button>
      </form>
      <p className="mt-4 text-base">
        Chưa có tài khoản?{" "}
        <Link href={`/register${query}`} className="font-medium underline underline-offset-4">
          Đăng ký
        </Link>
      </p>
    </div>
  );
}
