import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { PackagesView } from "./_view";

export const metadata: Metadata = { title: "Gói khám · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <PackagesView />
    </Suspense>
  );
}
