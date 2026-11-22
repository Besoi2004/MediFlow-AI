import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { CompareView } from "./_view";

export const metadata: Metadata = { title: "So sánh gói khám · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <CompareView />
    </Suspense>
  );
}
