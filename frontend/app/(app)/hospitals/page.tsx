import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { HospitalsView } from "./_view";

export const metadata: Metadata = { title: "Bệnh viện · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <HospitalsView />
    </Suspense>
  );
}
