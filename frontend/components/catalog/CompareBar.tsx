import Link from "next/link";

import { Button, buttonVariants } from "@/components/ui/button";

// Dính dưới màn hình khi đã chọn ít nhất một gói để so sánh.
export function CompareBar({ codes, onClear }: { codes: string[]; onClear: () => void }) {
  if (codes.length === 0) return null;
  const ready = codes.length >= 2;
  return (
    <div className="sticky bottom-4 z-30 mt-6 flex flex-wrap items-center justify-between gap-3 rounded-2xl border bg-card p-4 shadow-lg">
      <p className="text-base">
        Đã chọn {codes.length}/3 gói{ready ? "" : ", chọn thêm ít nhất 1 gói"}
      </p>
      <div className="flex gap-2">
        <Button variant="ghost" size="sm" onClick={onClear}>
          Bỏ chọn
        </Button>
        {ready ? (
          <Link href={`/compare?codes=${codes.join(",")}`} className={buttonVariants({ size: "sm" })}>
            So sánh ({codes.length})
          </Link>
        ) : (
          <Button size="sm" disabled>
            So sánh ({codes.length})
          </Button>
        )}
      </div>
    </div>
  );
}
