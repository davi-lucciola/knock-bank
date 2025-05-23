"use client";

import { Token } from "@/lib/token";
import { signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { useService } from "@/providers/service.provider";

export function useLogout() {
  const router = useRouter();
  const { authService } = useService();

  const { mutateAsync: logoutMutation, isPending } = useMutation({
    mutationFn: async () => {
      authService.logout();
      router.push("/");
      await signOut({ redirect: false });
    },
    onSuccess: () => Token.clean(),
  });

  const handleLogout = () => logoutMutation();

  return {
    isPending,
    handleLogout,
  };
}
