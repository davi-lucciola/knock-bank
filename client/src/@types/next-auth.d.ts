import { Account } from "@/modules/account/account.type";

declare module "next-auth" {
  interface Session {
    user: Account;
  }
}
