"use client";

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
import { Button } from "@/components/ui/button";
import { ArrowBendRightUp } from "@phosphor-icons/react";
import { MoneyInput } from "@/components/money-input";
import { useDeposit } from "../hooks/use-deposit";
import { Loader2 } from "lucide-react";

export function DepositForm() {
  const { form, isPending, handleDeposit, modal } = useDeposit();

  return (
    <Dialog
      open={modal.isOpen}
      onOpenChange={(open) => {
        modal.setIsOpen(open);
        form.setValue("money", 0);
      }}
    >
      <DialogTrigger asChild>
        <Button
          className="w-full h-16 text-xl flex gap-4 hover:cursor-pointer"
          variant="success"
        >
          Depositar
          <ArrowBendRightUp size={32} />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle> Depositar </DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleDeposit)}
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
                  <FormDescription>Valor que deseja depositar.</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button
                type="submit"
                variant="success"
                disabled={isPending}
                className="w-full max-w-52 hover:bg-success-hover hover:cursor-pointer"
              >
                Depositar
                {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
