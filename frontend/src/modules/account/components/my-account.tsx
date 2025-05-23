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
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2 } from "lucide-react";
import { AccountType } from "@/modules/account/account.type";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { DatePicker } from "@/components/date-picker";
import { MoneyInput } from "@/components/money-input";
import { ArrowLeft, Lock, Pencil, User } from "@phosphor-icons/react/dist/ssr";
import { useAccount } from "@/modules/account/contexts/account-context";
import { useUpdateAccount } from "@/modules/account/hooks/use-update-account";

export function MyAccount() {
  const { account, isPending } = useAccount();

  const {
    form,
    modal,
    editMode,
    toggleEditMode,
    handleUpdateAccount,
    isPending: isUpdatePending,
  } = useUpdateAccount(account);

  return (
    <Dialog
      open={modal.isOpen}
      onOpenChange={(open) => {
        modal.setIsOpen(open);
        if (editMode) toggleEditMode();
      }}
    >
      <DialogTrigger disabled={isPending} asChild>
        <User
          size={32}
          className={`fill-white duration-300 ${
            !isPending && "hover:fill-primary hover:cursor-pointer"
          }`}
        />
      </DialogTrigger>
      <DialogContent className="w-full max-w-sm rounded-lg lg:rounded-sm lg:max-w-xl">
        <DialogHeader>
          <DialogTitle> Minha Conta </DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleUpdateAccount)}
            autoComplete="off"
            className="flex flex-col gap-8"
          >
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nome</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Davi Lucciola"
                      disabled={!editMode}
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="birthDate"
              render={({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel>Data de Nascimento</FormLabel>
                  <FormControl>
                    <DatePicker
                      date={field.value}
                      disabled={!editMode}
                      onChange={(value: Date) => {
                        const [datePart] = value.toISOString().split("T");
                        field.onChange(datePart);
                      }}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="accountType"
              render={({ field }) => (
                <FormItem>
                  <FormLabel> Tipo de Conta </FormLabel>
                  <FormControl>
                    <Select
                      disabled={!editMode}
                      defaultValue={`${field.value}`}
                      onValueChange={(value) => field.onChange(Number(value))}
                    >
                      <SelectTrigger className="w-full focus:outline-primary">
                        <SelectValue placeholder="Selecione o tipo de conta..." />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectGroup>
                          <SelectLabel>Tipos de Contas</SelectLabel>
                          <SelectItem value={`${AccountType.CURRENT_ACCOUNT}`}>
                            Conta Corrente
                          </SelectItem>
                          <SelectItem value={`${AccountType.PAYMENT_ACCOUNT}`}>
                            Conta Pagamento
                          </SelectItem>
                          <SelectItem value={`${AccountType.SAVING_ACCOUNT}`}>
                            Conta Poupança
                          </SelectItem>
                          <SelectItem value={`${AccountType.SALARY_ACCOUNT}`}>
                            Conta Salário
                          </SelectItem>
                        </SelectGroup>
                      </SelectContent>
                    </Select>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="dailyWithdrawLimit"
              render={({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel>Limite de Saque Diário</FormLabel>
                  <FormControl>
                    <MoneyInput
                      disabled={!editMode}
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
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter
              className={`flex items-center mt-4 w-full ${
                editMode && "lg:justify-between"
              }`}
            >
              {editMode ? (
                <>
                  <div className="p-1 rounded-full duration-300 hover:bg-secondary hover:cursor-pointer">
                    <ArrowLeft size={24} onClick={toggleEditMode} />
                  </div>
                  <Button
                    type="submit"
                    disabled={isUpdatePending}
                    className="w-full max-w-52"
                  >
                    Salvar{" "}
                    {isUpdatePending && (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    )}
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    type="button"
                    variant="destructive"
                    className="flex gap-2"
                    // onClick={onBlockAccount}
                  >
                    Bloquear
                    <Lock size={24} className="fill-white" />
                  </Button>
                  <Button
                    type="button"
                    className="flex gap-2"
                    onClick={(e) => (e.preventDefault(), toggleEditMode())}
                  >
                    Editar
                    <Pencil size={24} className="fill-white" />
                  </Button>
                </>
              )}
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
