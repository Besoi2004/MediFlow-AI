import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Trình duyệt chỉ gọi /api/* trên cùng origin; Next.js chuyển tiếp sang FastAPI.
  rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.BACKEND_URL ?? "http://localhost:8000"}/api/:path*`,
      },
    ];
  },
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
