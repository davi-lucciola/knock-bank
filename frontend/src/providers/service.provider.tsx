"use client";

import { createContext, useContext } from "react";
import { Api } from "@/lib/api";
import { Token } from "@/lib/token";
import { AuthService } from "@/modules/auth/auth.service";
import { AccountService } from "@/modules/account/account.service";
import { TransactionService } from "@/modules/transaction/transaction.service";

type IServiceContext = {
  authService: AuthService;
  accountService: AccountService;
  transactionService: TransactionService;
};

export const ServiceContext = createContext({} as IServiceContext);

export function ServiceProvider({ children }: { children: React.ReactNode }) {
  const accessToken = Token.get();
  const api = new Api(accessToken);

  const authService = new AuthService(api);
  const accountService = new AccountService(api);
  const transactionService = new TransactionService(api);

  return (
    <ServiceContext.Provider
      value={{
        authService,
        accountService,
        transactionService,
      }}
    >
      {children}
    </ServiceContext.Provider>
  );
}

export function useService() {
  return useContext(ServiceContext);
}
