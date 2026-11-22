import type { Metadata } from "next";
import { Suspense } from "react";

import { PageSkeleton } from "@/components/PageState";

import { LoginView } from "./_view";

export const metadata: Metadata = { title: "Đăng nhập · MediFlow" };

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <LoginView />
    </Suspense>
  );
}
