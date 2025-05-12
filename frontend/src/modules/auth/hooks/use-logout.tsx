import { signOut } from "next-auth/react";
import { useMutation } from "@tanstack/react-query";
import { AuthService } from "@/modules/auth/auth.service";

export function useLogout(authService: AuthService) {
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
