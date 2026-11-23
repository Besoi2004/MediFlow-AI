// Mọi request tới backend đi qua api(): /api/* được Next rewrites sang FastAPI, cùng origin nên cookie đi kèm.

export class ApiError extends Error {
  status: number;
  fieldErrors: Record<string, string>;

  constructor(status: number, message: string, fieldErrors: Record<string, string> = {}) {
    super(message);
    this.status = status;
    this.fieldErrors = fieldErrors;
  }
}

const UNREACHABLE = "Không kết nối được máy chủ, vui lòng thử lại";

export async function api<T>(
  path: string,
  opts: { method?: string; json?: unknown; signal?: AbortSignal } = {},
): Promise<T> {
  const hasJson = opts.json !== undefined;
  let res: Response;
  try {
    res = await fetch(`/api${path}`, {
      method: opts.method ?? "GET",
      headers: hasJson ? { "Content-Type": "application/json" } : undefined,
      body: hasJson ? JSON.stringify(opts.json) : undefined,
      signal: opts.signal,
    });
  } catch (e) {
    if (opts.signal?.aborted) throw e; // component đã rời trang, không phải lỗi mạng
    throw new ApiError(0, UNREACHABLE);
  }
  if (res.status === 204) return undefined as T;
  const body = await res.json().catch((e) => {
    if (opts.signal?.aborted) throw e; // bị hủy giữa lúc đọc body: báo hủy như lúc fetch, không trả null
    if (!(e instanceof SyntaxError)) throw new ApiError(0, UNREACHABLE); // mất kết nối giữa lúc đọc body
    return null; // không phải JSON
  });
  if (!res.ok) {
    const errors: { field: string; message: string }[] = body?.errors ?? [];
    // Backend tắt thì rewrites của Next trả 500 dạng chữ, không phải lỗi mạng
    const fallback = res.status >= 500 && body === null ? UNREACHABLE : "Có lỗi xảy ra";
    const detail = typeof body?.detail === "string" ? body.detail : fallback;
    throw new ApiError(res.status, detail, Object.fromEntries(errors.map((e) => [e.field, e.message])));
  }
  if (body === null) throw new ApiError(res.status, "Có lỗi xảy ra"); // 2xx không phải JSON (không API nào trả null)
  return body as T;
}

// Kiểu dữ liệu khớp schema backend (backend/app/schemas.py). Ngày giờ là chuỗi ISO.
export type Gender = "male" | "female";

export type User = {
  id: number;
  email: string;
  full_name: string;
  role: "customer" | "consultant";
  birth_date: string | null;
  gender: Gender | null;
  phone: string | null;
};

export type Hospital = { code: string; name: string; city: string; address: string; phone: string; description: string };

export type PackageSummary = {
  code: string;
  name: string;
  hospital_code: string;
  hospital_name: string;
  city: string;
  price_vnd: number;
  gender_scope: "any" | Gender;
  age_min: number;
  age_max: number | null;
  tags: string[];
};

export type HospitalDetail = Hospital & { packages: PackageSummary[] };

export type PackageItem = { code: string; name: string; category: string; prep_instruction: string; fasting_hours: number };

export type PackageDetail = PackageSummary & { description: string; items: PackageItem[] };

export type CompareData = {
  packages: PackageSummary[];
  rows: { item_code: string; item_name: string; category: string; included: boolean[] }[];
};

export type Slot = { id: number; start_at: string; remaining: number };

export type Booking = {
  id: number;
  status: "booked" | "cancelled";
  channel: "web" | "assistant";
  package_code: string;
  package_name: string;
  hospital_code: string;
  hospital_name: string;
  start_at: string;
  price_snapshot_vnd: number;
  created_at: string;
};

export type ConsultantBooking = Booking & { customer_name: string; customer_phone: string | null; customer_email: string };

export type ChecklistItem = { text: string; items: string[] };
