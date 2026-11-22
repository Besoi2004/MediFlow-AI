import type { Metadata } from "next";
import { JetBrains_Mono, Reddit_Sans } from "next/font/google";

import { AuthProvider } from "@/components/auth/AuthProvider";

// Font do taste-skill chia (Reddit Sans + JetBrains Mono), cả hai có bộ chữ tiếng Việt.
const reddit = Reddit_Sans({ variable: "--font-reddit", subsets: ["vietnamese", "latin"] });
const jetbrains = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["vietnamese", "latin"] });

export const metadata: Metadata = {
  title: "MediFlow",
  description: "Đặt lịch gói khám sức khỏe định kỳ, có trợ lý AI",
};

// CSS không import ở đây: trang chủ nạp bộ giao diện của taste-skill (public/assets),
// các trang app nạp Tailwind + shadcn trong app/(app)/layout.tsx.
export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="vi" className={`${reddit.variable} ${jetbrains.variable}`} suppressHydrationWarning>
      <head>
        {/* Hai dòng đầu trang của taste-skill (hero hiện dần một lần, moment cuộn); vô hại ở trang app */}
        <script
          dangerouslySetInnerHTML={{
            __html:
              "document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700);" +
              "document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)",
          }}
        />
      </head>
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
