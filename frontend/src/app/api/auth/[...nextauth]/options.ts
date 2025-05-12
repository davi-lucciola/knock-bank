/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { cookies } from "next/headers";
import { TOKEN_KEY } from "@/lib/token";
import { Api, ApiError } from "@/lib/api";
import type { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { AuthService } from "@/modules/auth/auth.service";
import { AccountService } from "@/modules/account/account.service";
import { Account } from "@/modules/account/account.type";

export const nextAuthOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        cpf: {
          label: "Cpf",
          type: "text",
          placeholder: "your_email@email.com",
        },
        password: {
          label: "Password",
          type: "password",
          placeholder: "********",
        },
      },
      async authorize(credentials, req) {
        if (!credentials) {
          return null;
        }

        const api = new Api();
        const authService = new AuthService(api);

        try {
          const { accessToken } = await authService.login({
            ...credentials,
          });

          api.setAccessToken(accessToken);

          const cookie = await cookies();
          cookie.set(TOKEN_KEY, accessToken);

          const accountService = new AccountService(api);
          const account = await accountService.getCurrentAccount();

          return account as any;
        } catch (error: unknown) {
          if (error instanceof ApiError) {
            throw error;
          }

          throw new Error("Houve um error inesperado.");
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.user = user;
      }

      return token;
    },
    async session({ session, token }) {
      session.user = token.user as Account;
      return session;
    },
  },
};
