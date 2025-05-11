import {
  CreateAccountPayload,
  CreateAccountSchema,
} from "@/modules/account/account.type";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { Api, ApiError } from "@/lib/api";
import { AccountService } from "../account.service";
import { toast } from "sonner";
import { useState } from "react";

export function useCreateAccount() {
  const api = new Api();
  const accountService = new AccountService(api);

  const [isOpen, setIsOpen] = useState(false);

  const form = useForm<CreateAccountPayload>({
    resolver: zodResolver(CreateAccountSchema),
    defaultValues: {
      name: "",
      cpf: "",
      birthDate: "",
      password: "",
      accountType: 1,
    },
  });

  const { mutateAsync: createAccountMutation, isPending } = useMutation({
    mutationFn: async (data: CreateAccountPayload) => {
      return await accountService.createAccount(data);
    },
    onSuccess: (result) => {
      toast.success(result.message);
      form.reset();
      setIsOpen(false);
    },
    onError: (error) => {
      if (error instanceof ApiError) {
        toast.error(error.message);
        return;
      }

      toast.error("Houve um error ao processar sua solicitação.");
    },
  });

  const handleCreateAccount = (data: CreateAccountPayload) => {
    createAccountMutation(data);
  };

  return {
    form,
    isPending,
    handleCreateAccount,
    modal: {
      isOpen,
      setIsOpen,
    },
  };
}
