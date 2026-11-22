import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import type { PackageSummary } from "@/lib/api";
import { TAG_LABEL } from "@/lib/constants";
import { formatAudience, formatVnd } from "@/lib/format";
import { cn } from "@/lib/utils";

export function PackageCard({
  pkg,
  compareSelected,
  onToggleCompare,
  compact,
}: {
  pkg: PackageSummary;
  compareSelected?: boolean;
  onToggleCompare?: () => void;
  compact?: boolean; // khung chat của trợ lý (Kế hoạch 5)
}) {
  return (
    <article className={cn("flex flex-col gap-3 rounded-2xl border bg-card", compact ? "p-4" : "p-5")}>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="font-mono text-xs text-muted-foreground">{pkg.code}</p>
          <h3 className="mt-1 font-heading text-lg leading-snug font-medium">{pkg.name}</h3>
          <p className="text-sm text-muted-foreground">{pkg.hospital_name}</p>
        </div>
        <p className="shrink-0 text-lg font-medium tabular-nums">{formatVnd(pkg.price_vnd)}</p>
      </div>
      {!compact && (
        <div className="flex flex-wrap items-center gap-2 text-sm">
          {pkg.tags.map((t) => (
            <Badge key={t} variant="secondary">
              {TAG_LABEL[t] ?? t}
            </Badge>
          ))}
          <span className="text-muted-foreground">{formatAudience(pkg)}</span>
        </div>
      )}
      <div className="mt-auto flex flex-wrap gap-2 pt-1">
        <Link href={`/packages/${pkg.code}`} className={buttonVariants({ variant: "outline", size: "sm" })}>
          Chi tiết
        </Link>
        {onToggleCompare && (
          <Button variant={compareSelected ? "secondary" : "outline"} size="sm" aria-pressed={compareSelected} onClick={onToggleCompare}>
            {compareSelected ? "Bỏ so sánh" : "So sánh"}
          </Button>
        )}
        <Link href={`/book/${pkg.code}`} className={buttonVariants({ size: "sm" })}>
          Đặt lịch
        </Link>
      </div>
    </article>
  );
}
