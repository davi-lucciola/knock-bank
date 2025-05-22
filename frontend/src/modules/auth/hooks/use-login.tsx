"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { LoginUserPayload, LoginUserSchema } from "@/modules/auth/auth.type";
import { ApiError } from "@/lib/api";
import { toast } from "sonner";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";

export function useLogin() {
  const router = useRouter();
  const form = useForm<LoginUserPayload>({
    resolver: zodResolver(LoginUserSchema),
    defaultValues: {
      cpf: "",
      password: "",
    },
  });

  const { mutateAsync: signInMutation, isPending } = useMutation({
    mutationFn: async (data: LoginUserPayload) => {
      const response = await signIn("credentials", {
        ...data,
        redirect: false,
      });

      if (response?.error) {
        throw new ApiError(response.error);
      }
    },
    onSuccess: () => {
      toast.success("Connectado com sucesso.");
      router.push("/dashboard");
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  const handleLogin = (data: LoginUserPayload) => signInMutation(data);

  return {
    form,
    isPending,
    handleLogin,
  };
}
