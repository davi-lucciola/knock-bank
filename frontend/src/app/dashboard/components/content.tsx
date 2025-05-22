"use client";

import { Skeleton } from "@/components/ui/skeleton";
import { BalanceCard } from "@/modules/account/components/balance-card";
import { useCurrentAccount } from "@/modules/auth/hooks/use-current-account";

export function Content() {
  const { account, isPending } = useCurrentAccount();

  return (
    <main className="w-full h-full grid p-8 gap-8 grid-cols-1 grid-rows-3 lg:grid-cols-3 lg:grid-rows-2">
      {!isPending ? (
        <BalanceCard
          className="h-full flex flex-col justify-between lg:col-span-2"
          account={account}
        />
      ) : (
        <Skeleton className="h-full lg:col-span-2" />
      )}
      {/* <AccountResumeCard className="w-full flex flex-col row-start-3 lg:row-start-2 lg:col-span-2" /> */}
      <Skeleton className="w-full row-start-3 lg:row-start-2 lg:col-span-2" />
      {/* <BankStatmentCard className="h-full flex flex-col justify-between lg:row-span-2 lg:col-start-3" /> */}
      <Skeleton className="h-full justify-between lg:row-span-2 lg:col-start-3" />
    </main>
  );
}
