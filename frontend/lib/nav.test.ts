import { describe, expect, it } from "vitest";
import { consultantAccess, safeNext } from "./nav";

describe("safeNext", () => {                                           // Review Focus 2
  it("keeps internal paths", () => { expect(safeNext("/bookings")).toBe("/bookings"); expect(safeNext("/book/ALP-CB01?x=1")).toBe("/book/ALP-CB01?x=1"); });
  it("rejects external or empty", () => {
    for (const bad of [null, "", "https://evil.test", "//evil.test", "/\\evil.test", "/\t/evil.test", "/\n/evil.test", "/\r/evil.test", "bookings"]) expect(safeNext(bad)).toBe("/");
  });
  it("uses the given fallback", () => { expect(safeNext(null, "/consultant")).toBe("/consultant"); });
});

describe("consultantAccess", () => {
  const consultant = { role: "consultant" }, customer = { role: "customer" };
  it("waits, retries on a server error, sends guests to login", () => {
    expect(consultantAccess({ loading: true, user: null, error: null })).toBe("wait");
    expect(consultantAccess({ loading: false, user: null, error: { status: 0 } })).toBe("retry"); // backend tắt: không phải "không có quyền"
    expect(consultantAccess({ loading: false, user: null, error: null })).toBe("login"); // 401: phiên hết hạn hoặc bị từ chối
  });
  it("lets only consultants in", () => {
    expect(consultantAccess({ loading: false, user: customer, error: null })).toBe("forbidden");
    expect(consultantAccess({ loading: false, user: consultant, error: null })).toBe("ok");
  });
});
