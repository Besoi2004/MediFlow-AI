"use client";

import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { Hospital } from "@/lib/api";
import { CITY_OPTIONS, GENDER_LABEL, TAG_LABEL } from "@/lib/constants";

export const FILTER_KEYS = ["hospital", "city", "tag", "gender", "age", "price_max"] as const;
type Key = (typeof FILTER_KEYS)[number];

const PRICE_MAX = { "1000000": "Tối đa 1 triệu", "2000000": "Tối đa 2 triệu", "4000000": "Tối đa 4 triệu", "6000000": "Tối đa 6 triệu" };

function FilterSelect({ id, label, value, items, onChange }: {
  id: string;
  label: string;
  value: string | null;
  items: Record<string, string>;
  onChange: (value: string | null) => void;
}) {
  const all = { all: "Tất cả", ...items };
  return (
    <div className="grid gap-1.5">
      <label htmlFor={id} className="text-sm font-medium">
        {label}
      </label>
      <Select value={value ?? "all"} items={all} onValueChange={(v) => onChange(v === "all" ? null : String(v))}>
        <SelectTrigger id={id} className="w-full">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {Object.entries(all).map(([v, l]) => (
            <SelectItem key={v} value={v}>
              {l}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

// Đọc và ghi bộ lọc trên query string (view giữ URL, component chỉ hiển thị).
export function PackageFilters({ values, hospitals, onChange }: {
  values: Partial<Record<Key, string | null>>;
  hospitals: Hospital[];
  onChange: (key: Key, value: string | null) => void;
}) {
  return (
    <div className="grid grid-cols-2 gap-3 rounded-2xl border bg-card p-4 md:grid-cols-3 lg:grid-cols-6">
      <FilterSelect id="f-hospital" label="Bệnh viện" value={values.hospital ?? null} onChange={(v) => onChange("hospital", v)}
        items={Object.fromEntries(hospitals.map((h) => [h.code, h.name]))} />
      <FilterSelect id="f-city" label="Tỉnh/thành" value={values.city ?? null} onChange={(v) => onChange("city", v)}
        items={Object.fromEntries(CITY_OPTIONS.map((c) => [c, c]))} />
      <FilterSelect id="f-tag" label="Loại gói" value={values.tag ?? null} onChange={(v) => onChange("tag", v)} items={TAG_LABEL} />
      <FilterSelect id="f-gender" label="Giới tính" value={values.gender ?? null} onChange={(v) => onChange("gender", v)} items={GENDER_LABEL} />
      <div className="grid gap-1.5">
        <label htmlFor="f-age" className="text-sm font-medium">
          Tuổi
        </label>
        <Input
          id="f-age"
          type="number"
          inputMode="numeric"
          min={0}
          max={130}
          defaultValue={values.age ?? ""}
          onChange={(e) => {
            const age = e.currentTarget.value;
            if (age === "" || (Number.isInteger(Number(age)) && +age >= 0 && +age <= 130)) onChange("age", age || null);
          }}
        />
      </div>
      <FilterSelect id="f-price" label="Giá" value={values.price_max ?? null} onChange={(v) => onChange("price_max", v)} items={PRICE_MAX} />
    </div>
  );
}
