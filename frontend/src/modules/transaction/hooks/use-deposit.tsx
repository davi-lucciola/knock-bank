import { toast } from "sonner";
import { useState } from "react";
import { useForm } from "react-hook-form";
import {
  BasicTransferencePayload,
  BasicTransferenceSchema,
} from "@/modules/transaction/transaction.type";
import { zodResolver } from "@hookform/resolvers/zod";
import { useService } from "@/providers/service.provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ApiError } from "@/lib/api";

export function useDeposit() {
  const queryClient = useQueryClient();
  const { transactionService } = useService();

  const [isOpen, setIsOpen] = useState<boolean>(false);
  const form = useForm<BasicTransferencePayload>({
    resolver: zodResolver(BasicTransferenceSchema),
  });

  const { mutateAsync: depositMutation, isPending } = useMutation({
    mutationFn: (data: BasicTransferencePayload) => {
      return transactionService.deposit(data);
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

  const handleDeposit = (data: BasicTransferencePayload) => {
    depositMutation(data);
  };

  return {
    form,
    isPending,
    handleDeposit,
    modal: {
      isOpen,
      setIsOpen,
    },
  };
}
