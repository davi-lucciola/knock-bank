import { Api, ApiResponse } from "@/lib/api";
import {
  BaseAccount,
  Account,
  AccountQuery,
  UpdateAccountPayload,
} from "@/modules/account/account.type";
import { PaginationResponse } from "@/lib/pagination";
import { CreateAccountPayload } from "@/modules/account/account.type";

export class AccountService {
  constructor(private api: Api = new Api()) {}

  async getAccounts(
    query: AccountQuery
  ): Promise<PaginationResponse<BaseAccount>> {
    const urlParams = new URLSearchParams({
      search: query.search,
      ...(query.pageSize && { pageSize: query.pageSize.toString() }),
      ...(query.pageIndex && { pageIndex: query.pageIndex.toString() }),
    });

    const data = this.api.get<PaginationResponse<BaseAccount>>(
      "/account",
      urlParams
    );
    return data;
  }

  async getCurrentAccount(): Promise<Account> {
    const data = this.api.get<Account>("/account/me");
    return data;
  }

  async createAccount(payload: CreateAccountPayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, CreateAccountPayload>(
      "/account",
      payload
    );
    return data;
  }

  async updateAccount(
    accountId: number,
    payload: UpdateAccountPayload
  ): Promise<ApiResponse> {
    const data = this.api.put<ApiResponse, UpdateAccountPayload>(
      `/account/${accountId}`,
      payload
    );
    return data;
  }

  async blockAccount(accountId: number): Promise<ApiResponse> {
    const data = this.api.delete<ApiResponse>(`/account/${accountId}`);
    return data;
  }
}
