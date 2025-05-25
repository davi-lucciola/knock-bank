import {
  Transaction,
  TransactionMonthResume,
  TransactionQuery,
  BasicTransferencePayload,
  TransferencePayload,
} from "@/modules/transaction/transaction.type";
import { PaginationResponse } from "@/lib/pagination";
import { Api, ApiResponse } from "@/lib/api";

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
      "/transaction",
      urlParams
    );
    return data;
  }

  async getTransactionResume(): Promise<TransactionMonthResume[]> {
    const data = this.api.get<TransactionMonthResume[]>("/transaction/resume");
    return data;
  }

  async deposit(transference: BasicTransferencePayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, BasicTransferencePayload>(
      "/transaction/deposit",
      transference
    );
    return data;
  }

  async withdraw(transference: BasicTransferencePayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, BasicTransferencePayload>(
      "/transaction/withdraw",
      transference
    );
    return data;
  }

  async transfer(transference: TransferencePayload): Promise<ApiResponse> {
    const data = this.api.post<ApiResponse, TransferencePayload>(
      "/transaction/transfer",
      transference
    );
    return data;
  }
}
