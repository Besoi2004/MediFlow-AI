import { describe, expect, it } from "vitest";
import { dayKeyVN, formatDateTimeVN, formatDayVN, formatVnd, groupSlotsByDay, maxFastingHours, toggleCode } from "./format";

describe("format", () => {
  it("formats VND", () => { expect(formatVnd(1200000)).toBe("1.200.000đ"); expect(formatVnd(990000)).toBe("990.000đ"); });
  it("shows Vietnam time whatever the runtime TZ", () => {          // Review Focus 4 (chạy với TZ=UTC)
    expect(new Date(0).getTimezoneOffset()).toBe(0);                 // vitest.config.ts đặt TZ=UTC
    expect(formatDateTimeVN("2026-11-23T00:00:00Z")).toBe("07:00 · Thứ Hai, 23/11/2026");
    expect(dayKeyVN("2026-11-22T23:30:00Z")).toBe("2026-11-23");
  });
  it("formats a VN day key", () => { expect(formatDayVN("2026-11-29")).toBe("Chủ Nhật, 29/11/2026"); });
  it("groups slots by VN day in order", () => {
    const g = groupSlotsByDay([{ start_at: "2026-11-24T01:00:00Z" }, { start_at: "2026-11-22T23:30:00Z" }, { start_at: "2026-11-23T02:00:00Z" }]);
    expect(g.map((x) => x.day)).toEqual(["2026-11-23", "2026-11-24"]);
    expect(g[0].slots).toHaveLength(2);
  });
  it("toggles compare codes up to 3", () => {
    expect(toggleCode(["A"], "B")).toEqual(["A", "B"]);
    expect(toggleCode(["A", "B"], "A")).toEqual(["B"]);
    expect(toggleCode(["A", "B", "C"], "D")).toEqual(["A", "B", "C"]);
  });
  it("max fasting hours", () => { expect(maxFastingHours([{ fasting_hours: 0 }, { fasting_hours: 8 }, { fasting_hours: 6 }])).toBe(8); expect(maxFastingHours([])).toBe(0); });
});
