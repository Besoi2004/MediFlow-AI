import { afterEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "./api";

const reply = (status: number, body?: unknown) =>
  vi.stubGlobal("fetch", vi.fn(async () => new Response(body === undefined ? null : JSON.stringify(body), { status })));
afterEach(() => vi.unstubAllGlobals());

describe("api", () => {
  it("returns JSON", async () => { reply(200, [{ code: "ALP" }]); expect(await api("/hospitals")).toEqual([{ code: "ALP" }]); });
  it("maps 422 field errors", async () => {                           // Review Focus 5
    reply(422, { detail: "Dữ liệu không hợp lệ", errors: [{ field: "password", message: "Cần ít nhất 8 ký tự" }] });
    const e = (await api("/auth/register", { method: "POST", json: {} }).catch((x) => x)) as ApiError;
    expect(e).toBeInstanceOf(ApiError);
    expect(e.status).toBe(422);
    expect(e.fieldErrors).toEqual({ password: "Cần ít nhất 8 ký tự" });
  });
  it("uses backend detail for other errors", async () => {
    reply(409, { detail: "Khung giờ đã hết chỗ" });
    await expect(api("/bookings", { method: "POST", json: {} })).rejects.toMatchObject({ status: 409, message: "Khung giờ đã hết chỗ" });
  });
  it("treats a 5xx without JSON as the server being unreachable", async () => {  // Review Focus 1: backend tắt thì rewrites của Next trả 500 dạng chữ
    vi.stubGlobal("fetch", vi.fn(async () => new Response("Internal Server Error", { status: 500 })));
    await expect(api("/packages")).rejects.toMatchObject({ status: 500, message: "Không kết nối được máy chủ, vui lòng thử lại" });
  });
  it("falls back when a 4xx body is not JSON", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("Not Found", { status: 404 })));
    await expect(api("/packages")).rejects.toMatchObject({ status: 404, message: "Có lỗi xảy ra" });
  });
  it("turns network failure into a Vietnamese error", async () => {   // Review Focus 1
    vi.stubGlobal("fetch", vi.fn(async () => { throw new TypeError("Failed to fetch"); }));
    await expect(api("/packages")).rejects.toMatchObject({ status: 0, message: "Không kết nối được máy chủ, vui lòng thử lại" });
  });
  it("returns undefined on 204", async () => { reply(204); expect(await api("/auth/logout", { method: "POST" })).toBeUndefined(); });
  it("rethrows a cancel that lands while the body is read", async () => { // trả null thì useApi xóa dữ liệu cũ, trang nháy skeleton
    const ac = new AbortController();
    const body = new ReadableStream({ pull(c) { ac.abort(); c.error(ac.signal.reason); } });
    vi.stubGlobal("fetch", vi.fn(async () => new Response(body, { status: 200 })));
    await expect(api("/packages", { signal: ac.signal })).rejects.toMatchObject({ name: "AbortError" });
  });
  it("treats a connection lost while reading the body as unreachable", async () => { // 201 bị cắt body: không phải "Có lỗi xảy ra"
    const body = new ReadableStream({ pull(c) { c.error(new TypeError("terminated")); } });
    vi.stubGlobal("fetch", vi.fn(async () => new Response(body, { status: 201 })));
    await expect(api("/bookings", { method: "POST", json: {} })).rejects.toMatchObject({ status: 0, message: "Không kết nối được máy chủ, vui lòng thử lại" });
  });
  it("fails on a 200 whose body is not JSON", async () => {            // trả null thì trang hiện skeleton mãi
    vi.stubGlobal("fetch", vi.fn(async () => new Response("<!doctype html><title>Proxy</title>", { status: 200 })));
    await expect(api("/packages")).rejects.toMatchObject({ status: 200, message: "Có lỗi xảy ra" });
  });
});
