import { API_URL, Api, ApiResponse } from "@/lib/api";
import { CreateAccountPayload } from "../schemas/create-account";
import { Account } from "@/modules/account/schemas/account";
import { TransactionMonthResume } from "@/modules/account/schemas/transaction-month-resume";

export class AccountService {
  constructor(private api: Api = new Api()) {}

  async getCurrentAccount(): Promise<Account> {
    const data = this.api.get<Account>(`${API_URL}/account/me`);
    return data;
  }

  async getAccountResume(): Promise<TransactionMonthResume[]> {
    const data = this.api.get<TransactionMonthResume[]>(
      `${API_URL}/account/resume`
    );
    return data;
  }

  async createAccount(payload: CreateAccountPayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, CreateAccountPayload>(
      `${API_URL}/account`,
      payload
    );
    return data;
  }
}
