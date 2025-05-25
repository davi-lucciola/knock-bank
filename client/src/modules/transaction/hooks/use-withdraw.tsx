import { toast } from "sonner";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { ApiError } from "@/lib/api";
import {
  BasicTransferencePayload,
  BasicTransferenceSchema,
} from "@/modules/transaction/transaction.type";
import { zodResolver } from "@hookform/resolvers/zod";
import { useService } from "@/providers/service.provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useWithdraw() {
  const queryClient = useQueryClient();
  const { transactionService } = useService();

  const [isOpen, setIsOpen] = useState<boolean>(false);
  const form = useForm<BasicTransferencePayload>({
    resolver: zodResolver(BasicTransferenceSchema),
  });

  const { mutateAsync: withdrawMutation, isPending } = useMutation({
    mutationFn: (data: BasicTransferencePayload) => {
      return transactionService.withdraw(data);
    },
    onSuccess: (result) => {
      toast.success(result.message);
      form.reset();
      setIsOpen(false);

      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["current-account"] });
      queryClient.invalidateQueries({ queryKey: ["transactions-resume"] });
    },
    onError: (error) => {
      if (error instanceof ApiError) {
        toast.error(error.message);
        return;
      }

      toast.error("Houve um error ao processar sua solicitação.");
    },
  });

  const handleWithdraw = (data: BasicTransferencePayload) => {
    withdrawMutation(data);
  };

  return {
    form,
    isPending,
    handleWithdraw,
    modal: {
      isOpen,
      setIsOpen,
    },
  };
}
