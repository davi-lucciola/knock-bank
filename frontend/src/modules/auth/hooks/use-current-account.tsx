"use client";

import { useSession } from "next-auth/react";

export function useCurrentAccount() {
  const { data, status } = useSession();
  return {
    account: data?.user,
    isPending: status == "loading",
  };
}
