import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { SlotPicker } from "./SlotPicker";

const slots = [
  { id: 1, start_at: "2026-12-07T00:00:00Z", remaining: 4 },
  { id: 2, start_at: "2026-12-08T01:00:00Z", remaining: 5 },
];
const DISABLED = /<fieldset[^>]*\sdisabled=""/g;

describe("SlotPicker", () => {
  it("locks every day's times while a booking is being sent", () => {   // đang gửi yêu cầu đặt lịch: không đổi được giờ
    expect(renderToStaticMarkup(<SlotPicker slots={slots} disabled onSelect={() => {}} />).match(DISABLED)).toHaveLength(2);
    expect(renderToStaticMarkup(<SlotPicker slots={slots} onSelect={() => {}} />)).not.toMatch(DISABLED);
  });
});
