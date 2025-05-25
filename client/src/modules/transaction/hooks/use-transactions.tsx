import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useService } from "@/providers/service.provider";
import { TransactionQuery } from "@/modules/transaction/transaction.type";

export function useTransactions() {
  const { transactionService } = useService();
  const [filters, setFilters] = useState<TransactionQuery>({
    pageSize: 10,
    pageIndex: 1,
  });

  const { data: transactions, isPending } = useQuery({
    queryKey: ["transactions", filters],
    queryFn: () => transactionService.getMyTransactions(filters),
  });

  const changePage = (page: number) => {
    setFilters({
      ...filters,
      pageIndex: page,
    });
  };

  return {
    transactions,
    isPending,
    changePage,
    filters,
  };
}
