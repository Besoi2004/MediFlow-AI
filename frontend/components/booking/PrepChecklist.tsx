import type { ChecklistItem } from "@/lib/api";

// Việc cần làm trước giờ khám; chữ nhỏ là các hạng mục cần việc đó.
export function PrepChecklist({ items }: { items: ChecklistItem[] }) {
  if (items.length === 0) return <p className="text-base text-muted-foreground">Gói này không cần chuẩn bị gì đặc biệt.</p>;
  return (
    <ul className="space-y-3">
      {items.map((c) => (
        <li key={c.text} className="flex gap-3">
          <span aria-hidden="true" className="mt-2 size-2 shrink-0 rounded-full bg-primary" />
          <span>
            <span className="block text-base">{c.text}</span>
            {c.items.length > 0 && <span className="block text-sm text-muted-foreground">{c.items.join(", ")}</span>}
          </span>
        </li>
      ))}
    </ul>
  );
}
