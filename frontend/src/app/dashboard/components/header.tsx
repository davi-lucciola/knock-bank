"use client";

import { Skeleton } from "@/components/ui/skeleton";
import { useAccount } from "@/modules/account/contexts/account-context";

export function Header() {
  const { account, isPending } = useAccount();

  return (
    <header className="bg-white h-20 w-full py-3 px-8">
      <small className="text-sm"> Seja bem vindo </small>
      <div className="text-sm">
        {!isPending ? (
          <>
            <span className="text-lg font-bold"> {account?.person.name} </span>{" "}
            (Nº {account?.id})
          </>
        ) : (
          <Skeleton className="w-40 h-6" />
        )}
      </div>
    </header>
  );
}
