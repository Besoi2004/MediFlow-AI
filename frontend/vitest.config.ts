import { defineConfig } from "vitest/config";

// Chạy test ở UTC để test giờ Việt Nam (Review Focus 4) có ý nghĩa cả trên máy đặt giờ VN.
export default defineConfig({ test: { env: { TZ: "UTC" } } });
