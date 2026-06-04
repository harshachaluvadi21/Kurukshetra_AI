"use client";

import { create } from "zustand";
import { getToken, setToken, removeToken, authHeaders } from "@/lib/auth-token";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type AuthUser = {
  id: string;
  name: string;
  email: string;
  profile_picture?: string | null;
  provider: string;
  created_at?: string | null;
};

type AuthState = {
  user: AuthUser | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;

  initialize: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  loginWithToken: (token: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
};

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isLoading: true,
  isAuthenticated: false,
  error: null,

  initialize: async () => {
    const token = getToken();
    if (!token) {
      set({ isLoading: false, isAuthenticated: false, user: null, token: null });
      return;
    }

    try {
      const res = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        removeToken();
        set({ isLoading: false, isAuthenticated: false, user: null, token: null });
        return;
      }

      const user: AuthUser = await res.json();
      set({ user, token, isLoading: false, isAuthenticated: true });
    } catch {
      removeToken();
      set({ isLoading: false, isAuthenticated: false, user: null, token: null });
    }
  },

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Login failed");
      }

      const data = await res.json();
      setToken(data.access_token);
      set({
        user: data.user,
        token: data.access_token,
        isLoading: false,
        isAuthenticated: true,
        error: null,
      });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Login failed";
      set({ isLoading: false, error: message });
      throw err;
    }
  },

  register: async (name: string, email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Registration failed");
      }

      const data = await res.json();
      setToken(data.access_token);
      set({
        user: data.user,
        token: data.access_token,
        isLoading: false,
        isAuthenticated: true,
        error: null,
      });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Registration failed";
      set({ isLoading: false, error: message });
      throw err;
    }
  },

  loginWithToken: async (token: string) => {
    set({ isLoading: true, error: null });
    setToken(token);

    try {
      const res = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        removeToken();
        throw new Error("Invalid token");
      }

      const user: AuthUser = await res.json();
      set({ user, token, isLoading: false, isAuthenticated: true, error: null });
    } catch (err: unknown) {
      removeToken();
      const message = err instanceof Error ? err.message : "Authentication failed";
      set({ isLoading: false, isAuthenticated: false, user: null, token: null, error: message });
      throw err;
    }
  },

  logout: () => {
    removeToken();
    set({ user: null, token: null, isAuthenticated: false, error: null });
  },

  clearError: () => {
    set({ error: null });
  },
}));
