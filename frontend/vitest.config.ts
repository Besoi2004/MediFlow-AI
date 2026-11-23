import { defineConfig } from "vitest/config";

// Chạy test ở UTC để test giờ Việt Nam (Review Focus 4) có ý nghĩa cả trên máy đặt giờ VN.
// tsconfigPaths: component được test nhập "@/..." như trong app.
export default defineConfig({ resolve: { tsconfigPaths: true }, test: { env: { TZ: "UTC" } } });
