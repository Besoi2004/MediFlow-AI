// Chỉ quay lại đường dẫn trong app: chặn "//evil.test" và "/\evil.test" (trình duyệt hiểu là trang ngoài).
export function safeNext(next: string | null, fallback = "/"): string {
  if (!next || !next.startsWith("/") || next.startsWith("//") || next.startsWith("/\\")) return fallback;
  return next;
}
