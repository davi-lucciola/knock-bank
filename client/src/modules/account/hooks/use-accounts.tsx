import { useState } from "react";
import { AccountQuery } from "@/modules/account/account.type";
import { useQuery } from "@tanstack/react-query";
import { useService } from "@/providers/service.provider";
import { useDebounce } from "@uidotdev/usehooks";

export function useAccounts(accountId: number) {
  const { accountService } = useService();
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const [filters, setFilters] = useState<AccountQuery>({
    search: "",
  });
  const delayFilters = useDebounce(filters, 500);

  const { data: accounts } = useQuery({
    queryKey: ["transfer-accounts", delayFilters],
    queryFn: () => accountService.getAccounts(delayFilters),
  });

  const buttonLabel =
    accounts && accountId
      ? accounts.data.find((account) => account.id == accountId)?.person.name
      : "Selecione uma Conta";

  return {
    accounts,
    filters,
    setFilters,
    buttonLabel,
    popover: {
      isOpen,
      setIsOpen,
    },
  };
}
