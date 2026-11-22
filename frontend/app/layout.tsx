import type { Metadata } from "next";
import { JetBrains_Mono, Reddit_Sans } from "next/font/google";

import { AuthProvider } from "@/components/auth/AuthProvider";

// Font do taste-skill chia (Reddit Sans + JetBrains Mono), cả hai có bộ chữ tiếng Việt.
// preload: false vì trang chủ tự nạp font qua link Google Fonts của kit, không dùng bản này.
const reddit = Reddit_Sans({ variable: "--font-reddit", subsets: ["vietnamese", "latin"], preload: false });
const jetbrains = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["vietnamese", "latin"], preload: false });

export const metadata: Metadata = {
  title: "MediFlow",
  description: "Đặt lịch gói khám sức khỏe định kỳ, có trợ lý AI",
};

// CSS không import ở đây: trang chủ nạp bộ giao diện của taste-skill (public/assets),
// các trang app nạp Tailwind + shadcn trong app/(app)/layout.tsx.
export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="vi"
      className={`${reddit.variable} ${jetbrains.variable}`}
      // các thuộc tính của taste-skill (trang chủ); trang app không nạp kit nên không ảnh hưởng
      data-type="software"
      data-radius="round"
      data-ground="sage"
      data-buttons="pill"
      data-motion=""
      suppressHydrationWarning
    >
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
