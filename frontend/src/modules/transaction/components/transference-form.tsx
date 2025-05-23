"use client";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { ArrowsLeftRight } from "@phosphor-icons/react/dist/ssr";
import { MoneyInput } from "@/components/money-input";
import { AccountCombobox } from "@/modules/account/components/account-combobox";

import { Loader2 } from "lucide-react";
import { useTransference } from "../hooks/use-transference";

export function TransferenceForm() {
  const { form, isPending, handleTransfer, modal } = useTransference();

  return (
    <Dialog
      open={modal.isOpen}
      onOpenChange={(open) => {
        modal.setIsOpen(open);
        form.setValue("money", 0);
      }}
    >
      <DialogTrigger asChild>
        <Button className="w-full h-16 text-xl flex gap-4 hover:cursor-pointer">
          Transferir
          <ArrowsLeftRight size={32} />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle> Transferir </DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleTransfer)}
            autoComplete="off"
            className="flex flex-col gap-4"
          >
            <FormField
              control={form.control}
              name="money"
              render={({ field }) => (
                <FormItem>
                  <FormLabel> Valor </FormLabel>
                  <FormControl>
                    <MoneyInput
                      value={field.value}
                      onChange={(e) => {
                        const cleanedValue = e.target.value
                          .slice(3)
                          .replaceAll(".", "")
                          .replaceAll(",", ".");

                        field.onChange(Number(cleanedValue));
                      }}
                    />
                  </FormControl>
                  <FormDescription>
                    Valor que deseja transferir.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="accountId"
              render={({ field }) => (
                <FormItem>
                  <FormLabel> Conta Destino </FormLabel>
                  <FormControl>
                    <AccountCombobox
                      accountId={field.value}
                      setAccountId={(accountId: number) =>
                        form.setValue("accountId", accountId)
                      }
                    />
                  </FormControl>
                  <FormDescription>
                    Pesquise pelo nome ou começo do cpf da conta.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button
                type="submit"
                disabled={isPending}
                className="w-full max-w-52 hover:cursor-pointer"
              >
                Transferir
                {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
