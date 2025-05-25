"use client";
import {
  SessionProviderProps,
  SessionProvider as NextAuthSessionProvider,
} from "next-auth/react";

export function SessionProvider({ children, session }: SessionProviderProps) {
  return (
    <NextAuthSessionProvider session={session}>
      {children}
    </NextAuthSessionProvider>
  );
}
