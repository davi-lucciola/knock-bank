"use client";

import { SignOut } from "@phosphor-icons/react";
import { useLogout } from "@/modules/auth/hooks/use-logout";
import { AuthService } from "../auth.service";

type LogoutButtonProps = {
  authService: AuthService;
};

export function LogoutButton({ authService }: LogoutButtonProps) {
  const { handleLogout } = useLogout(authService);

  return (
    <button className="hover:cursor-pointer">
      <SignOut
        onClick={handleLogout}
        size={32}
        className="fill-destructive rotate-180"
      />
    </button>
  );
}
