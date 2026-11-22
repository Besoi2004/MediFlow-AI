import Link from "next/link";

import type { Hospital } from "@/lib/api";

export function HospitalCard({ hospital }: { hospital: Hospital }) {
  return (
    <Link
      href={`/hospitals/${hospital.code}`}
      className="flex flex-col gap-2 rounded-2xl border bg-card p-5 transition hover:-translate-y-0.5 hover:border-primary/40 focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:outline-none"
    >
      <p className="text-sm text-muted-foreground">{hospital.city}</p>
      <h3 className="font-heading text-lg leading-snug font-medium">{hospital.name}</h3>
      <p className="text-base">{hospital.description}</p>
      <p className="mt-auto pt-2 text-sm font-medium underline underline-offset-4">Xem các gói khám</p>
    </Link>
  );
}
