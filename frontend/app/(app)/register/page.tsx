import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { RegisterView } from "./_view";

export const metadata: Metadata = { title: "Đăng ký · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <RegisterView />
    </Suspense>
  );
}
