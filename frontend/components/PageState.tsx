import { Button } from "@/components/ui/button";

export function PageSkeleton() {
  return (
    <div className="space-y-4" aria-busy="true" aria-label="Đang tải">
      <div className="h-9 w-2/3 animate-pulse rounded-lg bg-muted" />
      <div className="h-5 w-1/2 animate-pulse rounded-lg bg-muted" />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="h-40 animate-pulse rounded-2xl bg-muted" />
        ))}
      </div>
    </div>
  );
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div role="alert" className="rounded-2xl border bg-card p-6">
      <p className="text-base">{message}</p>
      {onRetry && (
        <Button className="mt-4" variant="outline" onClick={onRetry}>
          Thử lại
        </Button>
      )}
    </div>
  );
}

export function EmptyState({ message }: { message: string }) {
  return <p className="rounded-2xl border border-dashed p-6 text-base text-muted-foreground">{message}</p>;
}
