import { describe, expect, it } from "vitest";
import { dayKeyVN, formatAudience, formatDateTimeVN, formatDayVN, formatVnd, groupSlotsByDay, maxFastingHours, orderBookings, prepLines, toggleCode } from "./format";

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
  it("describes who a package is for", () => {
    expect(formatAudience({ gender_scope: "male", age_min: 30, age_max: null })).toBe("Nam, từ 30 tuổi");
    expect(formatAudience({ gender_scope: "any", age_min: 18, age_max: 45 })).toBe("Nam và nữ, 18–45 tuổi");
  });
  it("lists prep lines with fasting first and no repeats", () => {
    const item = (fasting_hours: number, prep_instruction: string) => ({ fasting_hours, prep_instruction });
    expect(prepLines([item(8, ""), item(0, "Mang kính"), item(6, "Nhịn tiểu"), item(0, "Mang kính")])).toEqual([
      "Nhịn ăn ít nhất 8 tiếng trước giờ khám (được uống nước lọc)", "Mang kính", "Nhịn tiểu",
    ]);
    expect(prepLines([item(0, ""), item(0, "Mang kính")])).toEqual(["Mang kính"]);
  });
  it("puts upcoming booked appointments first, then the rest newest first", () => {
    const b = (id: number, status: string, start_at: string) => ({ id, status, start_at });
    const now = new Date("2026-11-23T00:00:00Z");
    const list = [b(1, "booked", "2026-11-20T00:00:00Z"), b(2, "booked", "2026-11-30T00:00:00Z"), b(3, "cancelled", "2026-11-25T00:00:00Z"), b(4, "booked", "2026-11-24T00:00:00Z")];
    expect(orderBookings(list, now).map((x) => x.id)).toEqual([4, 2, 3, 1]);
  });
});
