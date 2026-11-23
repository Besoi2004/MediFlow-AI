"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { BookingCard } from "@/components/booking/BookingCard";
import { EmptyState, ErrorState, PageSkeleton } from "@/components/PageState";
import { Button, buttonVariants } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { api, ApiError, type Booking } from "@/lib/api";
import { formatDateTimeVN, orderBookings } from "@/lib/format";
import { loginHref } from "@/lib/nav";
import { useApi } from "@/lib/useApi";

export function BookingsView() {
  const router = useRouter();
  const newId = Number(useSearchParams().get("new"));
  const { data, error, retry, mutate } = useApi<Booking[]>("/bookings");
  const [target, setTarget] = useState<Booking | null>(null);
  const [cancelError, setCancelError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  useEffect(() => {
    if (error?.status === 401) router.replace(loginHref()); // Review Focus 2
  }, [error, router]);

  async function cancel() {
    if (!target || !data) return;
    setPending(true);
    setCancelError(null);
    try {
      const updated = await api<Booking>(`/bookings/${target.id}/cancel`, { method: "POST" });
      mutate(data.map((b) => (b.id === updated.id ? updated : b)));
      setTarget(null);
    } catch (e) {
      const err = e instanceof ApiError ? e : new ApiError(0, "Có lỗi xảy ra");
      if (err.status === 401) {
        setTarget(null); // trang được giữ lại khi về đăng nhập: quay về không còn hộp hủy đang mở
        return router.replace(loginHref());
      }
      setCancelError(err.message); // 400 "Khung giờ đã qua", 409 đã hủy trước đó
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="font-heading text-3xl font-medium tracking-tight">Lịch của tôi</h1>
      {error ? (
        error.status === 401 ? <PageSkeleton /> : <ErrorState message={error.message} onRetry={retry} />
      ) : !data ? (
        <PageSkeleton />
      ) : data.length === 0 ? (
        <div className="space-y-4">
          <EmptyState message="Bạn chưa có lịch hẹn nào." />
          <Link href="/packages" className={buttonVariants()}>
            Chọn gói khám
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {orderBookings(data).map((b) => (
            <BookingCard
              key={b.id}
              booking={b}
              highlight={b.id === newId}
              onCancel={() => {
                setCancelError(null);
                setTarget(b);
              }}
            />
          ))}
        </div>
      )}

      <Dialog open={target !== null} onOpenChange={(open) => !open && setTarget(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Hủy lịch hẹn này?</DialogTitle>
            <DialogDescription>
              {target && `${target.package_name}, ${target.hospital_name}, ${formatDateTimeVN(target.start_at)}. Hủy rồi thì khung giờ được trả lại cho người khác.`}
            </DialogDescription>
          </DialogHeader>
          {cancelError && (
            <p role="alert" className="text-base text-destructive">
              {cancelError}
            </p>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setTarget(null)}>
              Giữ lịch
            </Button>
            <Button variant="destructive" disabled={pending} onClick={cancel}>
              {pending ? "Đang hủy…" : "Hủy lịch"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
