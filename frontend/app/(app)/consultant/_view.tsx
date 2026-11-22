"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { useAuth } from "@/components/auth/AuthProvider";
import { EmptyState, ErrorState, PageSkeleton } from "@/components/PageState";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { api, ApiError, type ConsultantBooking, type Hospital } from "@/lib/api";
import { formatDateTimeVN, formatVnd } from "@/lib/format";
import { useApi } from "@/lib/useApi";

const STATUS_ITEMS = { all: "Tất cả", booked: "Đã đặt", cancelled: "Đã hủy" };

export function ConsultantView() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const isConsultant = user?.role === "consultant";

  const qs = new URLSearchParams(["hospital", "status", "date"].flatMap((k) => (params.get(k) ? [[k, params.get(k)!]] : []))).toString();
  const bookings = useApi<ConsultantBooking[]>(isConsultant ? `/consultant/bookings?${qs}` : null);
  const hospitals = useApi<Hospital[]>(isConsultant ? "/hospitals" : null);
  const [target, setTarget] = useState<ConsultantBooking | null>(null);
  const [cancelError, setCancelError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  useEffect(() => {
    if (bookings.error?.status === 401) router.replace(`/login?next=${encodeURIComponent(pathname + (qs ? `?${qs}` : ""))}`);
  }, [bookings.error, router, pathname, qs]);

  function setParam(key: string, value: string | null) {
    const next = new URLSearchParams(params.toString());
    if (value) next.set(key, value);
    else next.delete(key);
    router.replace(`${pathname}?${next}`, { scroll: false });
  }

  async function cancel() {
    if (!target || !bookings.data) return;
    setPending(true);
    setCancelError(null);
    try {
      const updated = await api<ConsultantBooking>(`/consultant/bookings/${target.id}/cancel`, { method: "POST" });
      bookings.mutate(bookings.data.map((b) => (b.id === updated.id ? updated : b)));
      setTarget(null);
    } catch (e) {
      setCancelError(e instanceof ApiError ? e.message : "Có lỗi xảy ra");
    } finally {
      setPending(false);
    }
  }

  if (loading) return <PageSkeleton />;
  if (!isConsultant) return <EmptyState message="Trang này chỉ dành cho tư vấn viên." />;

  const hospitalItems = { all: "Tất cả", ...Object.fromEntries((hospitals.data ?? []).map((h) => [h.code, h.name])) };
  const e = bookings.error;

  return (
    <div className="space-y-6">
      <h1 className="font-heading text-3xl font-medium tracking-tight">Tư vấn viên</h1>
      {/* Kế hoạch 5 thêm tab "Cảnh báo cờ đỏ" */}
      <Tabs defaultValue="bookings">
        <TabsList>
          <TabsTrigger value="bookings">Lịch hẹn</TabsTrigger>
        </TabsList>
        <TabsContent value="bookings" className="space-y-4 pt-4">
          <div className="grid gap-3 rounded-2xl border bg-card p-4 sm:grid-cols-3">
            <div className="grid gap-1.5">
              <label htmlFor="c-hospital" className="text-sm font-medium">
                Bệnh viện
              </label>
              <Select value={params.get("hospital") ?? "all"} items={hospitalItems} onValueChange={(v) => setParam("hospital", v === "all" ? null : String(v))}>
                <SelectTrigger id="c-hospital" className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(hospitalItems).map(([v, l]) => (
                    <SelectItem key={v} value={v}>
                      {l}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="grid gap-1.5">
              <label htmlFor="c-date" className="text-sm font-medium">
                Ngày khám
              </label>
              <Input id="c-date" type="date" value={params.get("date") ?? ""} onChange={(ev) => setParam("date", ev.currentTarget.value || null)} />
            </div>
            <div className="grid gap-1.5">
              <label htmlFor="c-status" className="text-sm font-medium">
                Trạng thái
              </label>
              <Select value={params.get("status") ?? "all"} items={STATUS_ITEMS} onValueChange={(v) => setParam("status", v === "all" ? null : String(v))}>
                <SelectTrigger id="c-status" className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(STATUS_ITEMS).map(([v, l]) => (
                    <SelectItem key={v} value={v}>
                      {l}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {e && e.status !== 401 ? (
            // 422 khi ngày lọc quá xa: hiện đúng lỗi của ô ngày
            <ErrorState message={e.fieldErrors.date ?? e.message} onRetry={e.status === 422 ? undefined : bookings.retry} />
          ) : !bookings.data ? (
            <PageSkeleton />
          ) : bookings.data.length === 0 ? (
            <EmptyState message="Không có lịch hẹn nào khớp bộ lọc." />
          ) : (
            // relative: chữ sr-only (absolute) không thoát khung cuộn ngang
            <div className="relative overflow-x-auto rounded-2xl border bg-card">
              <table className="w-full min-w-[960px] border-collapse text-left text-sm">
                <thead className="text-muted-foreground">
                  <tr className="border-b">
                    {["Giờ khám", "Khách", "Gói", "Bệnh viện", "Giá", "Kênh", "Trạng thái", ""].map((h, i) => (
                      <th key={i} scope="col" className="p-3 font-medium">
                        {h || <span className="sr-only">Thao tác</span>}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {bookings.data.map((b) => (
                    <tr key={b.id} className="border-b align-top last:border-0">
                      <td className="p-3 whitespace-nowrap tabular-nums">{formatDateTimeVN(b.start_at)}</td>
                      <td className="p-3">
                        <span className="block font-medium">{b.customer_name}</span>
                        <span className="block text-muted-foreground">{b.customer_phone ?? "Chưa có SĐT"}</span>
                        <span className="block text-muted-foreground">{b.customer_email}</span>
                      </td>
                      <td className="p-3">{b.package_name}</td>
                      <td className="p-3">{b.hospital_name}</td>
                      <td className="p-3 whitespace-nowrap tabular-nums">{formatVnd(b.price_snapshot_vnd)}</td>
                      <td className="p-3">{b.channel === "assistant" ? "Trợ lý" : "Web"}</td>
                      <td className="p-3">
                        <Badge variant={b.status === "cancelled" ? "outline" : "secondary"}>{b.status === "cancelled" ? "Đã hủy" : "Đã đặt"}</Badge>
                      </td>
                      <td className="p-3">
                        {b.status === "booked" && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setCancelError(null);
                              setTarget(b);
                            }}
                          >
                            Hủy
                          </Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </TabsContent>
      </Tabs>

      <Dialog open={target !== null} onOpenChange={(open) => !open && setTarget(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Hủy lịch hẹn của khách?</DialogTitle>
            <DialogDescription>
              {target && `${target.customer_name}: ${target.package_name}, ${target.hospital_name}, ${formatDateTimeVN(target.start_at)}.`}
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
