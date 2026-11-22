"use client";

import { useParams } from "next/navigation";

import { PackageCard } from "@/components/catalog/PackageCard";
import { EmptyState, ErrorState, PageSkeleton } from "@/components/PageState";
import type { HospitalDetail } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export function HospitalDetailView() {
  const { code } = useParams<{ code: string }>();
  const { data: h, error, retry } = useApi<HospitalDetail>(`/hospitals/${encodeURIComponent(code)}`);

  if (error) return <ErrorState message={error.message} onRetry={error.status === 404 ? undefined : retry} />;
  if (!h) return <PageSkeleton />;

  return (
    <div className="space-y-8">
      <header className="space-y-2">
        <p className="text-sm text-muted-foreground">{h.city}</p>
        <h1 className="font-heading text-3xl font-medium tracking-tight">{h.name}</h1>
        <p className="max-w-prose text-base">{h.description}</p>
        <dl className="grid gap-1 text-base sm:grid-cols-[auto_1fr] sm:gap-x-4">
          <dt className="text-muted-foreground">Địa chỉ</dt>
          <dd>{h.address}</dd>
          <dt className="text-muted-foreground">Điện thoại</dt>
          <dd>{h.phone}</dd>
        </dl>
      </header>
      <section aria-labelledby="pk-h" className="space-y-4">
        <h2 id="pk-h" className="font-heading text-xl font-medium">
          Gói khám ({h.packages.length})
        </h2>
        {h.packages.length === 0 ? (
          <EmptyState message="Bệnh viện chưa có gói khám nào." />
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {h.packages.map((p) => (
              <PackageCard key={p.code} pkg={p} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
