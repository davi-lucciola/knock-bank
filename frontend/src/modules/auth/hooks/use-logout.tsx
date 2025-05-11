import { signOut } from "next-auth/react";
import { useMutation } from "@tanstack/react-query";
import { Api } from "@/lib/api";
import { AuthService } from "../auth.service";

export function useLogout(accessToken: string) {
  const api = new Api(accessToken);
  const authService = new AuthService(api);

  const { mutateAsync: logoutMutation, isPending } = useMutation({
    mutationFn: async () => {
      await authService.logout();
      // const response = await signOut();
    },
  });

  return {
    isPending,
    logoutMutation,
  };
}
