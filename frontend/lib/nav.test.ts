import { describe, expect, it } from "vitest";
import { safeNext } from "./nav";

describe("safeNext", () => {                                           // Review Focus 2
  it("keeps internal paths", () => { expect(safeNext("/bookings")).toBe("/bookings"); expect(safeNext("/book/ALP-CB01?x=1")).toBe("/book/ALP-CB01?x=1"); });
  it("rejects external or empty", () => {
    for (const bad of [null, "", "https://evil.test", "//evil.test", "/\\evil.test", "bookings"]) expect(safeNext(bad)).toBe("/");
  });
  it("uses the given fallback", () => { expect(safeNext(null, "/consultant")).toBe("/consultant"); });
});
