import type { CompareData } from "@/lib/api";
import { byCategory, CATEGORY_LABEL } from "@/lib/constants";
import { formatVnd } from "@/lib/format";

// Trên màn hình hẹp chỉ bảng cuộn ngang, cả trang không cuộn.
export function CompareTable({ data }: { data: CompareData }) {
  const cols = data.packages.length;
  return (
    <div className="relative overflow-x-auto rounded-2xl border bg-card">
      <table className="w-full min-w-[560px] border-collapse text-left text-base">
        <thead>
          <tr className="border-b align-top">
            <th scope="col" className="w-2/5 p-4 text-sm font-medium text-muted-foreground">
              Hạng mục
            </th>
            {data.packages.map((p) => (
              <th key={p.code} scope="col" className="p-4 font-normal">
                <span className="block font-heading text-base font-medium">{p.name}</span>
                <span className="block text-sm text-muted-foreground">{p.hospital_name}</span>
                <span className="mt-1 block font-medium tabular-nums">{formatVnd(p.price_vnd)}</span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {byCategory(data.rows).map(([category, rows]) => [
            <tr key={category} className="bg-muted/60">
              <th colSpan={cols + 1} scope="colgroup" className="px-4 py-2 text-sm font-medium">
                {CATEGORY_LABEL[category] ?? category}
              </th>
            </tr>,
            ...rows.map((r) => (
              <tr key={r.item_code} className="border-b last:border-0">
                <th scope="row" className="p-4 font-normal">
                  {r.item_name}
                </th>
                {r.included.map((yes, i) => (
                  <td key={data.packages[i].code} className="p-4 text-lg">
                    <span aria-hidden="true">{yes ? "✓" : "—"}</span>
                    <span className="sr-only">{yes ? "Có" : "Không có"}</span>
                  </td>
                ))}
              </tr>
            )),
          ])}
        </tbody>
      </table>
    </div>
  );
}
