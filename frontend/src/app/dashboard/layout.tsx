"use client";

import { Token } from "@/lib/token";
import { AccountContextProvider } from "@/modules/account/contexts/account-context";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { toast } from "sonner";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();
  const session = useSession();

  useEffect(() => {
    if (session.status == "unauthenticated") {
      Token.clean();
      router.push("/");
      toast.error("Você não está logado, por favor entre com sua conta.");
    }
  }, [session, router]);

  return <AccountContextProvider>{children}</AccountContextProvider>;
}
