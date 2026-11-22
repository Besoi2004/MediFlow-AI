// Tiền và giờ hiển thị trên giao diện, luôn theo giờ Việt Nam bất kể múi giờ của trình duyệt.

const vnd = new Intl.NumberFormat("vi-VN");
const vnParts = new Intl.DateTimeFormat("vi-VN", {
  timeZone: "Asia/Ho_Chi_Minh",
  weekday: "long",
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  hourCycle: "h23",
});

function partsVN(date: Date) {
  const p = Object.fromEntries(vnParts.formatToParts(date).map((x) => [x.type, x.value]));
  // ICU của vài trình duyệt viết thường "thứ hai": viết hoa chữ đầu mỗi từ cho đồng nhất
  p.weekday = p.weekday.replace(/(^|\s)\p{Ll}/gu, (c) => c.toUpperCase());
  return p;
}

export function formatVnd(n: number): string {
  return `${vnd.format(n)}đ`;
}

export function formatDateTimeVN(iso: string): string {
  const p = partsVN(new Date(iso));
  return `${p.hour}:${p.minute} · ${p.weekday}, ${p.day}/${p.month}/${p.year}`;
}

export function dayKeyVN(iso: string): string {
  const p = partsVN(new Date(iso));
  return `${p.year}-${p.month}-${p.day}`;
}

export function formatDayVN(dayKey: string): string {
  const p = partsVN(new Date(`${dayKey}T12:00:00+07:00`)); // giữa trưa giờ VN: không lệch sang ngày khác
  return `${p.weekday}, ${p.day}/${p.month}/${p.year}`;
}

export function groupSlotsByDay<T extends { start_at: string }>(slots: T[]): { day: string; slots: T[] }[] {
  const groups: { day: string; slots: T[] }[] = [];
  for (const slot of [...slots].sort((a, b) => Date.parse(a.start_at) - Date.parse(b.start_at))) {
    const day = dayKeyVN(slot.start_at);
    const last = groups[groups.length - 1];
    if (last?.day === day) last.slots.push(slot);
    else groups.push({ day, slots: [slot] });
  }
  return groups;
}

export function toggleCode(codes: string[], code: string, max = 3): string[] {
  if (codes.includes(code)) return codes.filter((c) => c !== code);
  return codes.length < max ? [...codes, code] : codes;
}

export function maxFastingHours(items: { fasting_hours: number }[]): number {
  return Math.max(0, ...items.map((i) => i.fasting_hours));
}
