"use client";

import { createContext, useState } from "react";


interface IAccountContext {
  isBalanceVisible: boolean;
  toggleIsBalanceVisible: () => void;
}

export const AccountContext = createContext({} as IAccountContext);
export function AccountContextProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isBalanceVisible, setIsBalanceVisible] = useState<boolean>(true);

  function toggleIsBalanceVisible() {
    setIsBalanceVisible(!isBalanceVisible);
  }

  return (
    <AccountContext.Provider
      value={{
        isBalanceVisible,
        toggleIsBalanceVisible,
      }}
    >
      {children}
    </AccountContext.Provider>
  );
}
