"use client";

import { useEffect } from "react";

// Script của kit sửa DOM (tách chữ h1, thêm class, chèn nút). Nạp sau khi React hydrate xong,
// nếu không React thấy HTML khác bản server và dựng lại cả cây, xóa mất phần kit vừa gắn.
const SCRIPTS = ["backgrounds/backgrounds.js", "system.js", "motion/motion.js", "layout/layout.js"];
let started = false;

export function KitScripts() {
  useEffect(() => {
    if (started) return; // StrictMode chạy effect hai lần
    started = true;
    const load = (i: number) => {
      if (i === SCRIPTS.length) return;
      const s = document.createElement("script");
      s.src = `/assets/${SCRIPTS[i]}`;
      if (i > 0) s.type = "module";
      s.onload = s.onerror = () => load(i + 1); // đúng thứ tự như starter.html
      document.body.appendChild(s);
    };
    load(0);
  }, []);
  return null;
}
