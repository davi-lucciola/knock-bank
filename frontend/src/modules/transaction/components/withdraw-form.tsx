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
import { MoneyInput } from "@/components/money-input";
import { ArrowBendLeftDown } from "@phosphor-icons/react/dist/ssr";
import { useWithdraw } from "../hooks/use-withdraw";
import { Loader2 } from "lucide-react";

export function WithdrawForm() {
  const { form, isPending, handleWithdraw, modal } = useWithdraw();

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
          variant="destructive"
        >
          Sacar
          <ArrowBendLeftDown size={32} />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle> Sacar </DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleWithdraw)}
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
                  <FormDescription>Valor que deseja sacar.</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button
                type="submit"
                variant="destructive"
                disabled={isPending}
                className="w-full max-w-52 hover:cursor-pointer"
              >
                Sacar
                {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
