"use client";

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { TransactionList } from "@/modules/transaction/components/transaction-list";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Skeleton } from "@/components/ui/skeleton";
import { getPageNumbers } from "@/lib/pagination";
import { useTransactions } from "../hooks/use-transactions";

export function BankStatmentCard() {
  const { transactions, isPending, changePage } = useTransactions();

  if (isPending || !transactions) {
    return (
      <Skeleton className="h-full shadow-lg justify-between lg:row-span-2 lg:col-start-3" />
    );
  }

  return (
    <Card className="h-full p-0 gap-0 flex flex-col justify-between lg:row-span-2 lg:col-start-3">
      <CardHeader className="text-2xl font-semibold p-6">Extrato</CardHeader>
      <CardContent className="overflow-auto max-h-176 pb-0 flex-1">
        {transactions.data.length != 0 ? (
          <TransactionList transactions={transactions.data} />
        ) : (
          <p className="text-gray-100 font-light">
            Não há transações para visualizar.
          </p>
        )}
      </CardContent>
      <CardFooter className="p-2">
        <BankStatmentPagination
          pageIndex={transactions.pageIndex}
          totalPages={transactions.totalPages}
          changePage={changePage}
        />
      </CardFooter>
    </Card>
  );
}

type BankStatmentPaginationProps = {
  pageIndex: number;
  totalPages: number;
  changePage: (page: number) => void;
};

function BankStatmentPagination({
  pageIndex,
  totalPages,
  changePage,
}: BankStatmentPaginationProps) {
  const pagesNumberArray = getPageNumbers(pageIndex, totalPages);

  return (
    <Pagination>
      <PaginationContent className="w-full justify-around lg:justify-center">
        <PaginationItem className="hover:cursor-pointer shrink">
          <PaginationPrevious
            onClick={() => {
              const newPageIndex = pageIndex != 1 ? pageIndex - 1 : pageIndex;
              changePage(newPageIndex);
            }}
          />
        </PaginationItem>
        {pagesNumberArray.map((page: number, index: number) => (
          <PaginationItem key={index} className="hover:cursor-pointer">
            <PaginationLink
              onClick={() => changePage(page)}
              isActive={page == pageIndex}
              className="lg:w-full lg:min-w-5 xl:shrink-0 xl:w-10"
            >
              {page}
            </PaginationLink>
          </PaginationItem>
        ))}
        <PaginationItem className="hover:cursor-pointer shrink">
          <PaginationNext
            onClick={() => {
              const newPageIndex =
                pageIndex != totalPages ? pageIndex + 1 : pageIndex;
              changePage(newPageIndex);
            }}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
}
