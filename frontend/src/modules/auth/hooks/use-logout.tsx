"use client";

import { signOut } from "next-auth/react";
import { useMutation } from "@tanstack/react-query";
import { useService } from "@/providers/service.provider";

export function useLogout() {
  const { authService } = useService();

  const { mutateAsync: logoutMutation, isPending } = useMutation({
    mutationFn: async () => {
      authService.logout();
      await signOut({ callbackUrl: "/", redirect: true });
    },
  });

  const handleLogout = () => logoutMutation();

  return {
    isPending,
    handleLogout,
  };
}
