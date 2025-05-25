import { BalanceCard } from "@/modules/account/components/balance-card";
import { BankStatmentCard } from "@/modules/transaction/components/bank-statment-card";
import { TransactionResumeCard } from "@/modules/transaction/components/transaction-resume-card";

export function Content() {
  return (
    <main className="w-full h-full grid p-8 gap-8 grid-cols-1 grid-rows-3 lg:grid-cols-3 lg:grid-rows-2">
      <BalanceCard />
      <TransactionResumeCard />
      <BankStatmentCard />
    </main>
  );
}
