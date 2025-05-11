"use client";

import { LogOut } from "lucide-react";
// import { useLogout } from "../hooks/use-logout";
// import { useSession } from "next-auth/react";

export function LogoutButton() {
  // const session = useSession();
  // const {} = useLogout();

  return (
    <button>
      <LogOut
        // onClick={handleLogout}
        size={32}
        className="fill-destructive rotate-180"
      />
    </button>
  );
}
