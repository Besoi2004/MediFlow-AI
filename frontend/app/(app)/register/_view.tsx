"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useLayoutEffect, useRef, useState } from "react";

import { Field, invalid, useFinishAuth } from "@/components/auth/AuthForm";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { api, ApiError, type User } from "@/lib/api";
import { GENDER_LABEL } from "@/lib/constants";

const FIELDS = ["full_name", "email", "password", "birth_date", "gender", "phone"] as const;

export function RegisterView() {
  const next = useSearchParams().get("next");
  const finish = useFinishAuth(next);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [pending, setPending] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);

  // cacheComponents giữ trang đã rời (Activity): quay lại form thì form phải mới, không kẹt "Đang đăng ký…"
  useLayoutEffect(() => {
    const form = formRef.current;
    return () => {
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
      // Ô trống gửi đi là thiếu (backend báo "Bắt buộc"), không phải chuỗi rỗng
      const json = Object.fromEntries(FIELDS.map((f) => [f, form.get(f) || undefined]));
      const user = await api<User>("/auth/register", { method: "POST", json });
      await finish(user);
    } catch (err) {
      const e = err instanceof ApiError ? err : new ApiError(0, "Có lỗi xảy ra");
      setFieldErrors(e.fieldErrors);
      if (!FIELDS.some((f) => e.fieldErrors[f])) setError(e.message); // 409 email đã dùng, lỗi mạng
      setPending(false);
    }
  }

  const query = next ? `?next=${encodeURIComponent(next)}` : "";
  return (
    <div className="mx-auto max-w-md py-6">
      <h1 className="font-heading text-3xl font-medium tracking-tight">Đăng ký</h1>
      <form ref={formRef} onSubmit={onSubmit} noValidate className="mt-6 grid gap-4 rounded-2xl border bg-card p-6">
        <Field id="full_name" label="Họ tên" error={fieldErrors.full_name}>
          <Input id="full_name" name="full_name" autoComplete="name" required {...invalid("full_name", fieldErrors.full_name)} />
        </Field>
        <Field id="email" label="Email" error={fieldErrors.email}>
          <Input id="email" name="email" type="email" autoComplete="email" required {...invalid("email", fieldErrors.email)} />
        </Field>
        <Field id="password" label="Mật khẩu (ít nhất 8 ký tự)" error={fieldErrors.password}>
          <Input id="password" name="password" type="password" autoComplete="new-password" required {...invalid("password", fieldErrors.password)} />
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field id="birth_date" label="Ngày sinh" error={fieldErrors.birth_date}>
            <Input id="birth_date" name="birth_date" type="date" required {...invalid("birth_date", fieldErrors.birth_date)} />
          </Field>
          <Field id="gender" label="Giới tính" error={fieldErrors.gender}>
            <Select name="gender" items={GENDER_LABEL}>
              <SelectTrigger id="gender" className="w-full" {...invalid("gender", fieldErrors.gender)}>
                <SelectValue placeholder="Chọn" />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(GENDER_LABEL).map(([value, label]) => (
                  <SelectItem key={value} value={value}>
                    {label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>
        </div>
        <Field id="phone" label="Số điện thoại" error={fieldErrors.phone}>
          <Input id="phone" name="phone" type="tel" autoComplete="tel" required {...invalid("phone", fieldErrors.phone)} />
        </Field>
        {error && (
          <p role="alert" className="text-sm text-destructive">
            {error}
          </p>
        )}
        <Button type="submit" disabled={pending}>
          {pending ? "Đang đăng ký…" : "Đăng ký"}
        </Button>
      </form>
      <p className="mt-4 text-base">
        Đã có tài khoản?{" "}
        <Link href={`/login${query}`} className="font-medium underline underline-offset-4">
          Đăng nhập
        </Link>
      </p>
    </div>
  );
}
