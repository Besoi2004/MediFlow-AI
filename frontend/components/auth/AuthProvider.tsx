"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { api, type User } from "@/lib/api";

type Auth = { user: User | null; loading: boolean; refresh(): Promise<void>; logout(): Promise<void> };

const AuthContext = createContext<Auth | null>(null);

// 401 là chưa đăng nhập; lỗi mạng cũng coi như chưa đăng nhập
const fetchMe = () => api<User>("/auth/me").catch(() => null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setUser(await fetchMe());
    setLoading(false);
  }, []);

  const logout = useCallback(async () => {
    await api("/auth/logout", { method: "POST" });
    setUser(null);
  }, []);

  useEffect(() => {
    fetchMe().then((u) => {
      setUser(u);
      setLoading(false);
    });
  }, []);

  const value = useMemo(() => ({ user, loading, refresh, logout }), [user, loading, refresh, logout]);
  return <AuthContext value={value}>{children}</AuthContext>;
}

export function useAuth(): Auth {
  const auth = useContext(AuthContext);
  if (!auth) throw new Error("useAuth phải nằm trong AuthProvider");
  return auth;
}
