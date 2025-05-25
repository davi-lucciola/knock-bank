"use client";

import { useService } from "@/providers/service.provider";
import { useQuery } from "@tanstack/react-query";
import { createContext, useContext, useState } from "react";
import { Account } from "../account.type";

interface IAccountContext {
  account?: Account;
  isPending: boolean;
  isBalanceVisible: boolean;
  toggleIsBalanceVisible: () => void;
}

export const AccountContext = createContext({} as IAccountContext);

export function AccountContextProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { accountService } = useService();

  const { data: account, isPending } = useQuery({
    queryKey: ["current-account"],
    queryFn: () => accountService.getCurrentAccount(),
  });

  const [isBalanceVisible, setIsBalanceVisible] = useState<boolean>(true);

  function toggleIsBalanceVisible() {
    setIsBalanceVisible((prev) => !prev);
  }

  return (
    <AccountContext.Provider
      value={{
        account,
        isPending,
        isBalanceVisible,
        toggleIsBalanceVisible,
      }}
    >
      {children}
    </AccountContext.Provider>
  );
}

export function useAccount() {
  return useContext(AccountContext);
}
