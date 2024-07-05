"use client";

import { Api, ApiResponse, ApiUnauthorizedError } from "@/lib/api";
import { createContext, useContext, useEffect, useState } from "react";
import { Account } from "@/modules/account/schemas/account";
import { AccountService } from "@/modules/account/services/account-service";
import { CreateAccountPayload } from "../schemas/create-account";
import { AuthContext } from "@/modules/auth/contexts/auth-context";
import { useUnauthorizedHandler } from "@/modules/auth/hooks/use-unauthorized-handler";

interface IAccountContext {
  isBalanceVisible: boolean;
  toggleIsBalanceVisible: () => void;
  fetchAccount: () => Promise<void>;
  getAccount: () => Account | null;
  setAccount: (account: Account | null) => void;
  createAccount: (account: CreateAccountPayload) => Promise<ApiResponse>;
}

export const AccountContext = createContext({} as IAccountContext);
export function AccountContextProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { getToken } = useContext(AuthContext);
  const { verifyToken, unauthorizedHandler } = useUnauthorizedHandler();
  const [account, setAccount] = useState<Account | null>(null);
  const [isBalanceVisible, setIsBalanceVisible] = useState<boolean>(true);
  const accountService = new AccountService(new Api(getToken() ?? undefined));

  async function fetchAccount() {
    const myAccount = await accountService.getCurrentAccount();
    setAccount(myAccount);
  }

  useEffect(() => {
    verifyToken();
    fetchAccount().catch(unauthorizedHandler);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function toggleIsBalanceVisible() {
    setIsBalanceVisible(!isBalanceVisible);
  }

  function getAccount(): Account | null {
    return account;
  }

  async function createAccount(
    payload: CreateAccountPayload
  ): Promise<ApiResponse> {
    const data = accountService.createAccount(payload);
    return data;
  }

  return (
    <AccountContext.Provider
      value={{
        isBalanceVisible,
        toggleIsBalanceVisible,
        fetchAccount,
        getAccount,
        setAccount,
        createAccount,
      }}
    >
      {children}
    </AccountContext.Provider>
  );
}
