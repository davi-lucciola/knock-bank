"use client";

import { Api } from "@/lib/api";
import { Token } from "@/lib/token";
import { AuthService } from "@/modules/auth/auth.service";
import { Menu } from "@/app/dashboard/components/menu";
import { Header } from "@/app/dashboard/components/header";
import { Content } from "./components/content";

// import { useSession } from "next-auth/react";
// import { Token } from "@/lib/token";
// import { getServerSession } from "next-auth";
// import { nextAuthOptions } from "@/lib/auth";
// import { BalanceCard } from "@/modules/account/components/balance-card";
// import { BankStatmentCard } from "@/modules/transaction/components/bank-statment-card";
// import { AccountResumeCard } from "@/modules/transaction/components/transaction-resume-card";
// import { AccountContext } from "@/modules/account/contexts/account-context";
// import { useUnauthorizedHandler } from "@/modules/auth/hooks/use-unauthorized-handler";
// import { MyAccount } from "@/modules/account/components/my-account";
// import { Account } from "@/modules/account/schemas/account";

export default function DashboardPage() {
  const accessToken = Token.get();

  const api = new Api(accessToken);
  const authService = new AuthService(api);

  return (
    <div className="flex flex-row w-screen min-h-screen">
      <Menu authService={authService} />
      <section className="bg-light-gray flex flex-col w-full ps-24">
        <Header />
        <Content />
      </section>
    </div>
  );
}
