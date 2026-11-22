"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import { Disclaimer } from "@/components/Disclaimer";
import { ErrorState, PageSkeleton } from "@/components/PageState";
import { buttonVariants } from "@/components/ui/button";
import type { PackageDetail } from "@/lib/api";
import { byCategory, CATEGORY_LABEL } from "@/lib/constants";
import { formatAudience, formatVnd, prepLines } from "@/lib/format";
import { useApi } from "@/lib/useApi";

export function PackageDetailView() {
  const { code } = useParams<{ code: string }>();
  const { data: pkg, error, retry } = useApi<PackageDetail>(`/packages/${encodeURIComponent(code)}`);

  if (error) return <ErrorState message={error.message} onRetry={error.status === 404 ? undefined : retry} />;
  if (!pkg) return <PageSkeleton />;

  const prep = prepLines(pkg.items);
  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_320px]">
      <div className="min-w-0 space-y-8">
        <header className="space-y-2">
          <p className="font-mono text-sm text-muted-foreground">{pkg.code}</p>
          <h1 className="font-heading text-3xl font-medium tracking-tight">{pkg.name}</h1>
          <p className="text-base">
            <Link href={`/hospitals/${pkg.hospital_code}`} className="underline underline-offset-4">
              {pkg.hospital_name}
            </Link>
            {" · "}
            {pkg.city}
          </p>
          {pkg.description && <p className="max-w-prose text-base">{pkg.description}</p>}
        </header>

        <section aria-labelledby="items-h" className="space-y-3">
          <h2 id="items-h" className="font-heading text-xl font-medium">
            Hạng mục ({pkg.items.length})
          </h2>
          <div className="divide-y rounded-2xl border bg-card">
            {byCategory(pkg.items).map(([category, items]) => (
              <div key={category} className="p-4">
                <h3 className="text-sm font-medium text-muted-foreground">{CATEGORY_LABEL[category] ?? category}</h3>
                <ul className="mt-2 space-y-1 text-base">
                  {items.map((i) => (
                    <li key={i.code}>{i.name}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {prep.length > 0 && (
          <section aria-labelledby="prep-h" className="space-y-3">
            <h2 id="prep-h" className="font-heading text-xl font-medium">
              Chuẩn bị trước khám
            </h2>
            <ul className="list-disc space-y-2 pl-5 text-base">
              {prep.map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>
          </section>
        )}
      </div>

      <aside className="h-fit space-y-4 rounded-2xl border bg-card p-5 lg:sticky lg:top-24">
        <p className="text-2xl font-medium tabular-nums">{formatVnd(pkg.price_vnd)}</p>
        <p className="text-base">Dành cho: {formatAudience(pkg)}</p>
        <Link href={`/book/${pkg.code}`} className={buttonVariants({ className: "w-full" })}>
          Đặt lịch
        </Link>
        <Disclaimer />
      </aside>
    </div>
  );
}
