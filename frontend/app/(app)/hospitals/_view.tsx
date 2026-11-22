"use client";

import { useRouter, useSearchParams } from "next/navigation";

import { HospitalCard } from "@/components/catalog/HospitalCard";
import { EmptyState, ErrorState, PageSkeleton } from "@/components/PageState";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { Hospital } from "@/lib/api";
import { CITY_OPTIONS } from "@/lib/constants";
import { useApi } from "@/lib/useApi";

const CITY_ITEMS = { all: "Tất cả", ...Object.fromEntries(CITY_OPTIONS.map((c) => [c, c])) };

export function HospitalsView() {
  const router = useRouter();
  const city = useSearchParams().get("city");
  const { data, error, retry } = useApi<Hospital[]>(city ? `/hospitals?city=${encodeURIComponent(city)}` : "/hospitals");

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <h1 className="font-heading text-3xl font-medium tracking-tight">Bệnh viện</h1>
        <div className="grid w-full gap-1.5 sm:w-64">
          <label htmlFor="f-city" className="text-sm font-medium">
            Tỉnh/thành
          </label>
          <Select
            value={city ?? "all"}
            items={CITY_ITEMS}
            onValueChange={(v) => router.replace(v === "all" ? "/hospitals" : `/hospitals?city=${encodeURIComponent(String(v))}`, { scroll: false })}
          >
            <SelectTrigger id="f-city" className="w-full">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(CITY_ITEMS).map(([v, l]) => (
                <SelectItem key={v} value={v}>
                  {l}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
      {error ? (
        <ErrorState message={error.message} onRetry={retry} />
      ) : !data ? (
        <PageSkeleton />
      ) : data.length === 0 ? (
        <EmptyState message="Chưa có bệnh viện nào ở tỉnh/thành này." />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data.map((h) => (
            <HospitalCard key={h.code} hospital={h} />
          ))}
        </div>
      )}
    </div>
  );
}
