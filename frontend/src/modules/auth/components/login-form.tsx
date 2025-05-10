"use client";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { formatCpf } from "@/lib/masks";
import { Loader2 } from "lucide-react";
import { useLogin } from "@/modules/auth/hooks/use-login";

export function LoginForm() {
  const { form, isPending, handleLogin } = useLogin();

  return (
    <Dialog>
      <DialogTrigger asChild>
        <button
          className="px-4 py-2 h-fit 
            border-primary border rounded-2xl
            text-xl font-bold
            duration-300
            hover:bg-primary hover:text-white hover:cursor-pointer"
        >
          Fazer Login
        </button>
      </DialogTrigger>
      <DialogContent className="w-full max-w-sm rounded-lg lg:rounded-sm lg:max-w-xl gap-8">
        <DialogHeader>
          <DialogTitle className="text-2xl"> Login </DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleLogin)}
            autoComplete="off"
            className="flex flex-col gap-4"
          >
            <FormField
              control={form.control}
              name="cpf"
              render={({ field: { onChange, ...props } }) => (
                <FormItem>
                  <FormLabel>Cpf</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="000.000.000-14"
                      onChange={(event) => {
                        const { value } = event.target;
                        event.target.value = formatCpf(value);
                        onChange(event);
                      }}
                      {...props}
                    />
                  </FormControl>
                  <FormDescription>
                    Digite o seu cpf onde sua conta está cadastrada.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Senha</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="********" {...field} />
                  </FormControl>
                  <FormDescription>Insira sua senha.</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button
                type="submit"
                className="w-full max-w-52"
                disabled={isPending}
              >
                Entrar{" "}
                {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
