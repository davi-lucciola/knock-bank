"use client";

import { toast } from "sonner";
import { ApiError } from "@/lib/api";
import { Account } from "../account.type";
import { useLogout } from "@/modules/auth/hooks/use-logout";
import { useService } from "@/providers/service.provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useBlockAccount(account?: Account) {
  const queryClient = useQueryClient();
  const { handleLogout } = useLogout();
  const { accountService } = useService();

  const { mutateAsync: blockAccountMutation } = useMutation({
    mutationFn: () => accountService.blockAccount(account!.id),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ["current-account"] });
      handleLogout();
      toast.success(result.message);
    },
    onError: (error) => {
      if (error instanceof ApiError) {
        toast.error(error.message);
        return;
      }

      toast.error("Houve um error ao processar sua solicitação.");
    },
  });

  const handleBlockAccount = () => blockAccountMutation();

  return {
    handleBlockAccount,
  };
}
