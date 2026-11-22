import { formatDateTimeVN, formatVnd } from "@/lib/format";

export function BookingSummary({ hospitalName, packageName, startAt, priceVnd }: {
  hospitalName: string;
  packageName: string;
  startAt: string;
  priceVnd: number;
}) {
  return (
    <dl className="grid gap-3 rounded-2xl border bg-card p-5 text-base">
      <div>
        <dt className="text-sm text-muted-foreground">Gói khám</dt>
        <dd className="font-medium">{packageName}</dd>
      </div>
      <div>
        <dt className="text-sm text-muted-foreground">Bệnh viện</dt>
        <dd>{hospitalName}</dd>
      </div>
      <div>
        <dt className="text-sm text-muted-foreground">Giờ khám</dt>
        <dd className="tabular-nums">{formatDateTimeVN(startAt)}</dd>
      </div>
      <div>
        <dt className="text-sm text-muted-foreground">Giá</dt>
        <dd className="text-lg font-medium tabular-nums">{formatVnd(priceVnd)}</dd>
      </div>
    </dl>
  );
}
