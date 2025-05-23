import { toast } from "sonner";
import { useState } from "react";
import { ApiError } from "@/lib/api";
import {
  TransferencePayload,
  TransferenceSchema,
} from "@/modules/transaction/transaction.type";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useService } from "@/providers/service.provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useTransference() {
  const queryClient = useQueryClient();
  const { transactionService } = useService();
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const form = useForm<TransferencePayload>({
    resolver: zodResolver(TransferenceSchema),
  });

  const { mutateAsync: transferMutation, isPending } = useMutation({
    mutationFn: (data: TransferencePayload) => {
      return transactionService.transfer(data);
    },
    onSuccess: (result) => {
      toast.success(result.message);
      form.reset();
      setIsOpen(false);

      queryClient.invalidateQueries({ queryKey: ["transactions"] });
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

  const handleTransfer = (data: TransferencePayload) => transferMutation(data);

  return {
    form,
    isPending,
    handleTransfer,
    modal: {
      isOpen,
      setIsOpen,
    },
  };
}
