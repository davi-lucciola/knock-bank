import { z } from "zod";
import { cpf } from "cpf-cnpj-validator";
import { PaginationQuery } from "@/lib/pagination";

export type Person = {
  id: number;
  name: string;
  cpf?: string;
  birthDate?: string;
};

export enum AccountType {
  CURRENT_ACCOUNT = 1,
  SAVING_ACCOUNT = 2,
  SALARY_ACCOUNT = 3,
  PAYMENT_ACCOUNT = 4,
}

export type BaseAccount = {
  id: number;
  person: Person;
  flActive: boolean;
};

export type Account = BaseAccount & {
  balance: number;
  dailyWithdrawLimit: number;
  todayWithdraw: number;
  accountType: AccountType;
};

export type AccountQuery = PaginationQuery & {
  search: string;
};

export const UpdateAccountSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(4, "Seu nome deve conter pelo menos 4 caracteres."),
    birthDate: z.coerce.date({
      errorMap: (issue, { defaultError }) => ({
        message:
          issue.code === "invalid_date"
            ? "A data de nascimento é obrigatória."
            : defaultError,
      }),
    }),
    accountType: z.number(),
    dailyWithdrawLimit: z.coerce
      .string()
      .transform((value) =>
        isNaN(Number(value))
          ? Number(value.replace(/[^0-9]/g, "")) / 100
          : Number(value)
      )
      .refine(
        (value) => value >= 0,
        "Você só pode transferir valores positivos."
      ),
  })
  .transform(({ birthDate, ...props }) => {
    return { birthDate: birthDate.toISOString().split("T")[0], ...props };
  });

export type UpdateAccountPayload = z.infer<typeof UpdateAccountSchema>;

export const CreateAccountSchema = z.object({
  name: z
    .string()
    .trim()
    .min(4, "Seu nome deve conter pelo menos 4 caracteres."),
  cpf: z
    .string()
    .trim()
    .refine((doc) => {
      const replacedDoc = doc.replace(/\D/g, "");
      return replacedDoc.length == 11;
    }, "Seu CPF deve conter 11 caracteres.")
    .refine((doc) => {
      const replacedDoc = doc.replace(/\D/g, "");
      return !!Number(replacedDoc);
    }, "Seu CPF deve conter apenas números.")
    .refine((cpfValue: string) => cpf.isValid(cpfValue), "Cpf inválido.")
    .transform((doc) => doc.replace(/\D/g, "")),
  birthDate: z
    // .date({ required_error: "A data de nascimento é obrigatória." })
    // .transform((date) => date.toISOString().split("T")[0]),
    .string({ required_error: "A data de nascimento é obrigatória." })
    .refine((val) => /^\d{4}-\d{2}-\d{2}$/.test(val), {
      message: "Data em um formato inválido. (YYYY-MM-DD)",
    }),
  accountType: z.number(),
  password: z
    .string()
    .trim()
    .min(8, "Sua senha deve conter pelo menos 8 caracteres.")
    .refine(
      (senha: string) => /[a-z]/.test(senha),
      "Sua senha deve conter pelo menos uma letra minúscula."
    )
    .refine(
      (senha: string) => /[A-Z]/.test(senha),
      "Sua senha deve conter pelo menos uma letra maiúscula."
    )
    .refine(
      (senha: string) => /[0-9]/.test(senha),
      "Sua senha deve conter pelo menos um numero."
    )
    .refine(
      (senha: string) => /\W|_/.test(senha),
      "Sua senha deve conter pelo menos um caractere especial."
    ),
});

export type CreateAccountPayload = z.infer<typeof CreateAccountSchema>;
