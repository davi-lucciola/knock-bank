import type { Metadata } from "next";
import { Roboto } from "next/font/google";

import { cn } from "@/lib/utils";
import { Toaster } from "@/components/ui/sonner";
import { QueryProvider } from "@/providers/query.provider";
import { ThemeProvider } from "@/providers/theme.provider";
import { SessionProvider } from "@/providers/session.provider";
import "./globals.css";

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
    <html lang="pt-BR" suppressHydrationWarning={true}>
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased overflow-x-hidden",
          roboto.variable
        )}
      >
        <ThemeProvider defaultTheme="light">
          <SessionProvider>
            <QueryProvider>{children}</QueryProvider>
            <Toaster />
          </SessionProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
