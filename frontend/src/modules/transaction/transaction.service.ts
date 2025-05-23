import { PaginationResponse } from "@/lib/pagination";
import { API_URL, Api, ApiResponse } from "@/lib/api";
import {
  Transaction,
  TransactionMonthResume,
  TransactionQuery,
} from "@/modules/transaction/transaction.type";
import {
  BasicTransferencePayload,
  TransferencePayload,
} from "@/modules/transaction/schemas/transference";

export class TransactionService {
  constructor(private api: Api = new Api()) {}

  async getMyTransactions(
    query: TransactionQuery
  ): Promise<PaginationResponse<Transaction>> {
    const urlParams = new URLSearchParams({
      ...(query.pageSize && { pageSize: query.pageSize.toString() }),
      ...(query.pageIndex && { pageIndex: query.pageIndex.toString() }),
      ...(query.transactionDate && {
        transactionDate: query.transactionDate.toISOString(),
      }),
      ...(query.transactionType && {
        transactionDate: query.transactionType.toString(),
      }),
    });

    const data = this.api.get<PaginationResponse<Transaction>>(
      `${API_URL}/transaction`,
      urlParams
    );
    return data;
  }

  async getAccountResume(): Promise<TransactionMonthResume[]> {
    const data = this.api.get<TransactionMonthResume[]>(
      `${API_URL}/transaction/resume`
    );
    return data;
  }

  async deposit(transference: BasicTransferencePayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, BasicTransferencePayload>(
      `${API_URL}/transaction/deposit`,
      transference
    );
    return data;
  }

  async withdraw(transference: BasicTransferencePayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, BasicTransferencePayload>(
      `${API_URL}/transaction/withdraw`,
      transference
    );
    return data;
  }

  async transfer(transference: TransferencePayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, TransferencePayload>(
      `${API_URL}/transaction/transfer`,
      transference
    );
    return data;
  }
}
