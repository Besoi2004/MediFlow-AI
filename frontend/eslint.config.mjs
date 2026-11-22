import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  {
    // Trang chủ nạp bộ kit của taste-skill bằng file thường và sang trang app bằng <a> (tải lại cả trang):
    // trang app không nạp kit, trang chủ không nạp Tailwind.
    files: ["app/page.tsx", "components/home/**"],
    rules: {
      "@next/next/no-html-link-for-pages": "off",
      "@next/next/no-css-tags": "off",
      "@next/next/no-page-custom-font": "off",
    },
  },
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    // Bộ kit của taste-skill, chép nguyên văn (gate cấm sửa)
    "public/assets/**",
  ]),
]);

export default eslintConfig;
