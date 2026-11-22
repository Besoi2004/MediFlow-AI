import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { ConsultantView } from "./_view";

export const metadata: Metadata = { title: "Tư vấn viên · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <ConsultantView />
    </Suspense>
  );
}
