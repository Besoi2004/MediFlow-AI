"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";

import { CompareTable } from "@/components/catalog/CompareTable";
import { Disclaimer } from "@/components/Disclaimer";
import { ErrorState, PageSkeleton } from "@/components/PageState";
import type { CompareData } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export function CompareView() {
  const codes = useSearchParams().get("codes");
  const { data, error, retry } = useApi<CompareData>(codes ? `/packages/compare?codes=${encodeURIComponent(codes)}` : null);
  const back = (
    <Link href="/packages" className="font-medium underline underline-offset-4">
      Về trang Gói khám
    </Link>
  );

  return (
    <div className="space-y-6">
      <h1 className="font-heading text-3xl font-medium tracking-tight">So sánh gói khám</h1>
      {!codes ? (
        <p className="text-base">Chọn 2–3 gói ở trang Gói khám để so sánh. {back}</p>
      ) : error ? (
        <div className="space-y-3">
          {/* 400 (số gói sai), 404 (mã gói sai): không thử lại được, chỉ quay về chọn gói */}
          <ErrorState message={error.message} onRetry={error.status >= 500 || error.status === 0 ? retry : undefined} />
          <p className="text-base">{back}</p>
        </div>
      ) : !data ? (
        <PageSkeleton />
      ) : (
        <>
          <CompareTable data={data} />
          <Disclaimer />
        </>
      )}
    </div>
  );
}
