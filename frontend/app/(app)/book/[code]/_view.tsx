"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { BookingSummary } from "@/components/booking/BookingSummary";
import { SlotPicker } from "@/components/booking/SlotPicker";
import { Disclaimer } from "@/components/Disclaimer";
import { ErrorState, PageSkeleton } from "@/components/PageState";
import { Button } from "@/components/ui/button";
import { api, ApiError, type Booking, type PackageDetail, type Slot } from "@/lib/api";
import { loginHref } from "@/lib/nav";
import { useApi } from "@/lib/useApi";

export function BookView() {
  const { code } = useParams<{ code: string }>();
  const router = useRouter();
  const pkg = useApi<PackageDetail>(`/packages/${encodeURIComponent(code)}`);
  const slots = useApi<Slot[]>(`/packages/${encodeURIComponent(code)}/slots`);
  const [selected, setSelected] = useState<Slot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  // Danh sách giờ tải lại (sau 409) mà giờ đang chọn đã hết chỗ thì bỏ chọn
  const chosen = selected && slots.data?.some((s) => s.id === selected.id) ? selected : null;

  useEffect(() => {
    if (pkg.error?.status === 401 || slots.error?.status === 401) router.replace(loginHref());
  }, [pkg.error, slots.error, router]);

  async function confirm() {
    if (!chosen) return;
    setPending(true);
    setError(null);
    try {
      const b = await api<Booking>("/bookings", { method: "POST", json: { package_code: code, slot_id: chosen.id } });
      router.push(`/bookings?new=${b.id}`);
    } catch (e) {
      const err = e instanceof ApiError ? e : new ApiError(0, "Có lỗi xảy ra");
      setPending(false); // cả khi về đăng nhập: trang được giữ lại, quay về không kẹt "Đang đặt lịch…"
      if (err.status === 401) return router.replace(loginHref()); // Review Focus 2
      if (err.status === 403) setError("Tài khoản tư vấn viên không đặt lịch được");
      else setError(err.message);
      if (err.status === 409) {
        setSelected(null); // Review Focus 3: giờ vừa bị người khác lấy hết chỗ
        slots.retry();
      }
    }
  }

  if (pkg.error) return <ErrorState message={pkg.error.message} onRetry={pkg.error.status === 404 ? undefined : pkg.retry} />;
  if (!pkg.data) return <PageSkeleton />;
  const p = pkg.data;

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_340px]">
      <div className="min-w-0 space-y-6">
        <header className="space-y-1">
          <p className="text-sm text-muted-foreground">Đặt lịch khám</p>
          <h1 className="font-heading text-3xl font-medium tracking-tight">{p.name}</h1>
          <p className="text-base">{p.hospital_name}</p>
        </header>
        <section aria-labelledby="slots-h" className="space-y-3">
          <h2 id="slots-h" className="font-heading text-xl font-medium">
            Chọn giờ khám
          </h2>
          {slots.error ? (
            <ErrorState message={slots.error.message} onRetry={slots.retry} />
          ) : !slots.data ? (
            <PageSkeleton />
          ) : (
            <SlotPicker
              slots={slots.data}
              selectedId={chosen?.id}
              disabled={pending}
              onSelect={(s) => {
                setSelected(s);
                setError(null);
              }}
            />
          )}
        </section>
      </div>
      <aside className="h-fit space-y-4 lg:sticky lg:top-24">
        {chosen ? (
          <BookingSummary hospitalName={p.hospital_name} packageName={p.name} startAt={chosen.start_at} priceVnd={p.price_vnd} />
        ) : (
          <p className="rounded-2xl border border-dashed p-5 text-base text-muted-foreground">Chọn một khung giờ để xem tóm tắt lịch hẹn.</p>
        )}
        {error && (
          <p role="alert" className="rounded-xl bg-destructive/10 px-4 py-3 text-base text-destructive">
            {error}
          </p>
        )}
        <Button className="w-full" disabled={!chosen || pending} onClick={confirm}>
          {pending ? "Đang đặt lịch…" : "Xác nhận đặt lịch"}
        </Button>
        <Disclaimer />
      </aside>
    </div>
  );
}
