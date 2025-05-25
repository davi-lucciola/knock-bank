"use client";

import { ApiError, ApiUnauthorizedError } from "@/lib/api";
import { Token } from "@/lib/token";
import {
  QueryCache,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import { ReactNode } from "react";
import { toast } from "sonner";

export function QueryProvider({ children }: { children: ReactNode }) {
  const router = useRouter();

  const queryCache = new QueryCache({
    onError: async (error) => {
      if (error instanceof ApiUnauthorizedError) {
        Token.clean();
        router.push("/");
        await signOut({ redirect: false });
        return;
      }

      if (error instanceof ApiError) {
        toast.error(error.message);
        return;
      }

      toast.error("Houve um error ao processar sua solicitação.");
    },
  });
  const queryClient = new QueryClient({ queryCache });
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
