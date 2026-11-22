// Chỉ quay lại đường dẫn trong app: chặn "//evil.test" và "/\evil.test" (trình duyệt hiểu là trang ngoài),
// và mọi ký tự điều khiển: trình phân tích URL bỏ tab, CR, LF nên "/\t/evil.test" thành "//evil.test".
const CONTROL = /[\u0000-\u001F\u007F]/;

export function safeNext(next: string | null, fallback = "/"): string {
  if (!next || !next.startsWith("/") || next.startsWith("//") || next.startsWith("/\\") || CONTROL.test(next)) return fallback;
  return next;
}

// Trang tư vấn viên: lỗi máy chủ khi hỏi /auth/me là "thử lại", chưa đăng nhập (401) là "về đăng nhập",
// không bao giờ báo nhầm "không có quyền" cho một tư vấn viên.
export function consultantAccess(a: {
  loading: boolean;
  user: { role: string } | null;
  error: { status: number } | null;
}): "wait" | "retry" | "login" | "forbidden" | "ok" {
  if (a.loading) return "wait";
  if (a.error) return "retry";
  if (!a.user) return "login";
  return a.user.role === "consultant" ? "ok" : "forbidden";
}
