"use client";

import { toast } from "sonner";
import { ApiError } from "@/lib/api";
import { useEffect, useState } from "react";
import {
  Account,
  UpdateAccountPayload,
  UpdateAccountSchema,
} from "@/modules/account/account.type";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useService } from "@/providers/service.provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useUpdateAccount(account?: Account) {
  const queryClient = useQueryClient();
  const { accountService } = useService();

  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [editMode, setEditMode] = useState<boolean>(false);

  const form = useForm<UpdateAccountPayload>({
    resolver: zodResolver(UpdateAccountSchema),
  });

  useEffect(() => {
    if (account) {
      form.setValue("name", account.person.name);
      form.setValue("birthDate", account.person.birthDate!);
      form.setValue("accountType", account.accountType);
      form.setValue("dailyWithdrawLimit", account.dailyWithdrawLimit);
    }
  }, [account, form]);

  const toggleEditMode = () => {
    setEditMode((prev) => !prev);
  };

  const { mutateAsync: updateAccountMutation, isPending } = useMutation({
    mutationFn: (data: UpdateAccountPayload) => {
      return accountService.updateAccount(account!.id, data);
    },
    onSuccess: (result) => {
      toast.success(result.message);
      form.reset();
      setIsOpen(false);
      queryClient.invalidateQueries({ queryKey: ["current-account"] });
    },
    onError: (error) => {
      if (error instanceof ApiError) {
        toast.error(error.message);
        return;
      }

      toast.error("Houve um error ao processar sua solicitação.");
    },
  });

  const handleUpdateAccount = (data: UpdateAccountPayload) => {
    updateAccountMutation(data);
  };

  return {
    form,
    editMode,
    toggleEditMode,
    isPending,
    handleUpdateAccount,
    modal: {
      isOpen,
      setIsOpen,
    },
  };
}
