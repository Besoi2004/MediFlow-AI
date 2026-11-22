import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { PackageDetailView } from "./_view";

export const metadata: Metadata = { title: "Chi tiết gói khám · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <PackageDetailView />
    </Suspense>
  );
}
