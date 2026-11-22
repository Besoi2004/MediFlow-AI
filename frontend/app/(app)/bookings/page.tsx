import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { BookingsView } from "./_view";

export const metadata: Metadata = { title: "Lịch của tôi · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <BookingsView />
    </Suspense>
  );
}
