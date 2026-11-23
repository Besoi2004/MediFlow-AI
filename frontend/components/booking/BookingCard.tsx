"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { PrepChecklist } from "@/components/booking/PrepChecklist";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api, ApiError, type Booking, type ChecklistItem } from "@/lib/api";
import { formatDateTimeVN, formatVnd } from "@/lib/format";
import { loginHref } from "@/lib/nav";
import { cn } from "@/lib/utils";

export function BookingCard({ booking, onCancel, highlight }: { booking: Booking; onCancel?: () => void; highlight?: boolean }) {
  const router = useRouter();
  const [prep, setPrep] = useState<{ open: boolean; items?: ChecklistItem[]; error?: string }>({ open: false });
  const cancelled = booking.status === "cancelled";

  async function togglePrep() {
    if (prep.open) return setPrep((p) => ({ ...p, open: false }));
    setPrep((p) => ({ ...p, open: true, error: undefined }));
    if (prep.items) return;
    try {
      const items = await api<ChecklistItem[]>(`/bookings/${booking.id}/checklist`);
      setPrep({ open: true, items });
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        setPrep({ open: false }); // trang được giữ lại khi về đăng nhập: không kẹt "Đang tải…"
        return router.replace(loginHref());
      }
      setPrep({ open: true, error: e instanceof ApiError ? e.message : "Có lỗi xảy ra" });
    }
  }

  return (
    <article
      className={cn("space-y-3 rounded-2xl border bg-card p-5", cancelled && "opacity-60", highlight && "border-primary ring-3 ring-primary/30")}
      aria-label={highlight ? "Lịch hẹn vừa đặt" : undefined}
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="font-heading text-lg leading-snug font-medium">{booking.package_name}</h3>
          <p className="text-sm text-muted-foreground">{booking.hospital_name}</p>
        </div>
        <Badge variant={cancelled ? "outline" : "secondary"}>{cancelled ? "Đã hủy" : "Đã đặt"}</Badge>
      </div>
      <p className="text-base tabular-nums">
        {formatDateTimeVN(booking.start_at)} · {formatVnd(booking.price_snapshot_vnd)}
      </p>
      {!cancelled && (
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" aria-expanded={prep.open} onClick={togglePrep}>
            {prep.open ? "Ẩn chuẩn bị" : "Xem chuẩn bị"}
          </Button>
          {onCancel && (
            <Button variant="ghost" size="sm" onClick={onCancel}>
              Hủy
            </Button>
          )}
        </div>
      )}
      {prep.open && (
        <div className="rounded-xl bg-muted p-4">
          {prep.error ? (
            <p role="alert" className="text-base">
              {prep.error}
            </p>
          ) : prep.items ? (
            <PrepChecklist items={prep.items} />
          ) : (
            <p className="text-base text-muted-foreground">Đang tải…</p>
          )}
        </div>
      )}
    </article>
  );
}
