"use client";

import { useCallback, useEffect, useState } from "react";

import { api, ApiError } from "@/lib/api";

// Tải dữ liệu cho một view. Đổi path thì giữ dữ liệu cũ trên màn hình cho tới khi có dữ liệu mới.
export function useApi<T>(path: string | null) {
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<{ key: string; data?: T; error?: ApiError }>({ key: "" });
  const key = `${path}#${attempt}`;

  useEffect(() => {
    if (path === null) return;
    const ac = new AbortController();
    api<T>(path, { signal: ac.signal }).then(
      (data) => setState({ key, data }),
      (e) => {
        if (!ac.signal.aborted) setState((s) => ({ key, data: s.data, error: e instanceof ApiError ? e : new ApiError(0, "Có lỗi xảy ra") }));
      },
    );
    return () => ac.abort();
  }, [path, key]);

  const retry = useCallback(() => setAttempt((a) => a + 1), []);
  const mutate = useCallback((data: T) => setState({ key, data }), [key]);
  return {
    data: state.data,
    error: state.key === key ? state.error : undefined,
    loading: path !== null && state.key !== key,
    retry,
    mutate,
  };
}
