import { EmptyState } from "@/components/PageState";
import type { Slot } from "@/lib/api";
import { formatDateTimeVN, formatDayVN, groupSlotsByDay } from "@/lib/format";
import { cn } from "@/lib/utils";

// Khung giờ còn chỗ, nhóm theo ngày giờ Việt Nam; mỗi giờ là một nút.
export function SlotPicker({ slots, selectedId, onSelect }: { slots: Slot[]; selectedId?: number; onSelect(slot: Slot): void }) {
  const days = groupSlotsByDay(slots);
  if (days.length === 0) return <EmptyState message="Chưa có khung giờ còn chỗ trong 14 ngày tới." />;
  return (
    <div className="space-y-5">
      {days.map(({ day, slots: daySlots }) => (
        <fieldset key={day} className="space-y-2">
          <legend className="text-sm font-medium">{formatDayVN(day)}</legend>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {daySlots.map((s) => {
              const on = s.id === selectedId;
              return (
                <button
                  key={s.id}
                  type="button"
                  aria-pressed={on}
                  onClick={() => onSelect(s)}
                  className={cn(
                    "flex min-h-14 flex-col items-start justify-center rounded-xl border bg-card px-4 py-2 text-left transition hover:border-primary/50 focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:outline-none",
                    on && "border-primary bg-primary text-primary-foreground hover:border-primary",
                  )}
                >
                  {/* "07:00 · Thứ Hai, ..." → chỉ lấy giờ */}
                  <span className="font-medium tabular-nums">{formatDateTimeVN(s.start_at).slice(0, 5)}</span>
                  <span className={cn("text-sm", on ? "text-primary-foreground/80" : "text-muted-foreground")}>còn {s.remaining} chỗ</span>
                </button>
              );
            })}
          </div>
        </fieldset>
      ))}
    </div>
  );
}
