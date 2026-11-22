"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { api, ApiError, type User } from "@/lib/api";

// error: lỗi khác 401 khi hỏi /auth/me (backend tắt, lỗi máy chủ); 401 chỉ là chưa đăng nhập
type Auth = { user: User | null; loading: boolean; error: ApiError | null; refresh(): Promise<void>; logout(): Promise<void> };

const AuthContext = createContext<Auth | null>(null);

const fetchMe = () =>
  api<User>("/auth/me").then(
    (user) => ({ user, error: null }),
    (e) => ({ user: null, error: e instanceof ApiError && e.status === 401 ? null : e instanceof ApiError ? e : new ApiError(0, "Có lỗi xảy ra") }),
  );

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ApiError | null>(null);

  const refresh = useCallback(async () => {
    const me = await fetchMe();
    setUser(me.user);
    setError(me.error);
    setLoading(false);
  }, []);

  const logout = useCallback(async () => {
    await api("/auth/logout", { method: "POST" });
    setUser(null);
  }, []);

  useEffect(() => {
    fetchMe().then((me) => {
      setUser(me.user);
      setError(me.error);
      setLoading(false);
    });
  }, []);

  const value = useMemo(() => ({ user, loading, error, refresh, logout }), [user, loading, error, refresh, logout]);
  return <AuthContext value={value}>{children}</AuthContext>;
}

export function useAuth(): Auth {
  const auth = useContext(AuthContext);
  if (!auth) throw new Error("useAuth phải nằm trong AuthProvider");
  return auth;
}
