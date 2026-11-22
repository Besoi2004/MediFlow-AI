"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";

import { CompareBar } from "@/components/catalog/CompareBar";
import { PackageCard } from "@/components/catalog/PackageCard";
import { FILTER_KEYS, PackageFilters } from "@/components/catalog/PackageFilters";
import { EmptyState, ErrorState, PageSkeleton } from "@/components/PageState";
import type { Hospital, PackageSummary } from "@/lib/api";
import { toggleCode } from "@/lib/format";
import { useApi } from "@/lib/useApi";

export function PackagesView() {
  const params = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const filters = Object.fromEntries(FILTER_KEYS.map((k) => [k, params.get(k)]));
  const query = new URLSearchParams(FILTER_KEYS.flatMap((k) => (params.get(k) ? [[k, params.get(k)!]] : [])));
  const compare = (params.get("compare") ?? "").split(",").filter(Boolean);

  const packages = useApi<PackageSummary[]>(`/packages?${query}`);
  const hospitals = useApi<Hospital[]>("/hospitals");

  function setParam(key: string, value: string | null) {
    const next = new URLSearchParams(params.toString());
    if (value) next.set(key, value);
    else next.delete(key);
    router.replace(`${pathname}?${next}`, { scroll: false });
  }

  return (
    <div className="space-y-6">
      <h1 className="font-heading text-3xl font-medium tracking-tight">Gói khám</h1>
      <PackageFilters values={filters} hospitals={hospitals.data ?? []} onChange={setParam} />
      {packages.error ? (
        <ErrorState message={packages.error.message} onRetry={packages.retry} />
      ) : !packages.data ? (
        <PageSkeleton />
      ) : packages.data.length === 0 ? (
        <EmptyState message="Không có gói khám nào khớp bộ lọc. Bỏ bớt điều kiện để xem thêm gói." />
      ) : (
        <>
          <p className="text-base text-muted-foreground" aria-live="polite">
            {packages.loading ? "Đang tải…" : `${packages.data.length} gói khám`}
          </p>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {packages.data.map((p) => (
              <PackageCard
                key={p.code}
                pkg={p}
                compareSelected={compare.includes(p.code)}
                onToggleCompare={() => setParam("compare", toggleCode(compare, p.code).join(",") || null)}
              />
            ))}
          </div>
        </>
      )}
      <CompareBar codes={compare} onClear={() => setParam("compare", null)} />
    </div>
  );
}
