"use client";

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
// import { ArrowBendLeftDown, ArrowsLeftRight } from "@phosphor-icons/react";
import { toBrasilianReal } from "@/lib/masks";
import { Hiddleble } from "@/components/hiddeble";
import { BalanceVisibilityToggle } from "@/modules/account/components/balance-visibility-toggle";
import { DailyWithdrawProgress } from "@/modules/account/components/daily-withdraw-progress";
import { DepositForm } from "@/modules/transaction/components/deposit-form";
import { WithdrawForm } from "@/modules/transaction/components/withdraw-form";
import { TransferenceForm } from "@/modules/transaction/components/transference-form";
import { useAccount } from "@/modules/account/contexts/account-context";
import { Skeleton } from "@/components/ui/skeleton";

export function BalanceCard() {
  const { account, isPending } = useAccount();

  if (isPending) {
    return <Skeleton className="h-full shadow-sm lg:col-span-2" />;
  }

  return (
    <Card className="h-full flex flex-col justify-between lg:col-span-2">
      <CardHeader className="w-full flex flex-row justify-between">
        <h2 className="text-2xl font-semibold">Saldo</h2>
        <BalanceVisibilityToggle />
      </CardHeader>
      <CardContent className="w-full flex flex-col items-center gap-12">
        <Hiddleble className="w-48 h-12 shadow-lg">
          <span className="text-5xl font-bold">
            {toBrasilianReal(account?.balance)}
          </span>
        </Hiddleble>
        <DailyWithdrawProgress
          todayWithdraw={account?.todayWithdraw}
          dailyWithdrawLimit={account?.dailyWithdrawLimit}
        />
      </CardContent>
      <CardFooter className="w-full flex flex-col lg:flex-row gap-8">
        <DepositForm />
        <WithdrawForm />
        <TransferenceForm />
      </CardFooter>
    </Card>
  );
}
