"use client";

import { SignOut } from "@phosphor-icons/react";
import { useLogout } from "@/modules/auth/hooks/use-logout";

export function LogoutButton() {
  const { handleLogout } = useLogout();

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
