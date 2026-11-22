import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { BookView } from "./_view";

export const metadata: Metadata = { title: "Đặt lịch khám · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <BookView />
    </Suspense>
  );
}
