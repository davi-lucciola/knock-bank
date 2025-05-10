import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import "./globals.css";

import { cn } from "@/lib/utils";
import { Toaster } from "@/components/ui/sonner";
import { QueryProvider } from "@/providers/query-provider";
import { ThemeProvider } from "@/providers/theme-provider";
// import { AuthContextProvider } from "@/modules/auth/contexts/auth-context";
// import { AccountContextProvider } from "@/modules/account/contexts/account-context";
// import { TransactionContextProvider } from "@/modules/transaction/contexts/transaction-context";

const roboto = Roboto({
  subsets: ["latin"],
  weight: ["300"],
  display: "swap",
  variable: "--font-roboto-mono",
});

export const metadata: Metadata = {
  title: "KnockBank",
  description: "Home page for create an account or login in a existing account",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // <AuthContextProvider>
    //   <AccountContextProvider>
    //     <TransactionContextProvider>

    <html lang="pt-BR" suppressHydrationWarning={true}>
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased overflow-x-hidden",
          roboto.variable
        )}
      >
        <ThemeProvider enableSystem={false}>
          <QueryProvider>{children}</QueryProvider>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>

    //     </TransactionContextProvider>
    //   </AccountContextProvider>
    // </AuthContextProvider>
  );
}
