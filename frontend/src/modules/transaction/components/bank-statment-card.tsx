"use client";

// import { useEffect } from "react";
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
import { useQuery } from "@tanstack/react-query";
import { useService } from "@/providers/service.provider";
import { Skeleton } from "@/components/ui/skeleton";

function getPageNumbers(totalPages?: number, pageIndex?: number): number[] {
  return Array.from(new Array(totalPages ?? 4), (_, index) => index + 1).filter(
    (page) => {
      const itemsQuantity = 4;
      if (
        pageIndex! > itemsQuantity / 2 &&
        pageIndex! < totalPages! - itemsQuantity / 2
      ) {
        return (
          page > pageIndex! - itemsQuantity / 2 &&
          page <= pageIndex! + itemsQuantity / 2
        );
      } else if (pageIndex! > totalPages! - itemsQuantity) {
        return page > totalPages! - itemsQuantity;
      } else {
        return page <= itemsQuantity;
      }
    }
  );
}

export function BankStatmentCard() {
  const { transactionService } = useService();

  const { data: transactions, isPending } = useQuery({
    queryKey: ["transactions"],
    queryFn: () => transactionService.getMyTransactions({}),
  });

  // const changePage = (page: number) => {
  //   setTransactionQuery({
  //     ...transactionQuery,
  //     pageIndex: page,
  //   });
  // };

  const pagesNumberArray = getPageNumbers(
    transactions?.totalPages,
    transactions?.pageIndex
  );

  if (isPending || !transactions) {
    return (
      <Skeleton className="h-full justify-between lg:row-span-2 lg:col-start-3" />
    );
  }

  return (
    <Card className="h-full flex flex-col justify-between lg:row-span-2 lg:col-start-3">
      <CardHeader className="text-2xl font-semibold">Extrato</CardHeader>
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
        <Pagination>
          <PaginationContent className="w-full justify-around lg:justify-center">
            <PaginationItem className="hover:cursor-pointer shrink">
              <PaginationPrevious
              // onClick={() => {
              //   const newPageIndex =
              //     transactionQuery.pageIndex! > 1
              //       ? transactionQuery.pageIndex! - 1
              //       : transactionQuery.pageIndex!;

              //   changePage(newPageIndex);
              // }}
              />
            </PaginationItem>
            {pagesNumberArray.map((page: number, index: number) => (
              <PaginationItem key={index} className="hover:cursor-pointer">
                <PaginationLink
                  // onClick={(event: any) => {
                  //   event.preventDefault();
                  //   changePage(page);
                  // }}
                  isActive={page == transactions?.pageIndex}
                  className="lg:w-full lg:min-w-5 xl:shrink-0 xl:w-10"
                >
                  {page}
                </PaginationLink>
              </PaginationItem>
            ))}
            <PaginationItem className="hover:cursor-pointer shrink">
              <PaginationNext
              // onClick={() => {
              //   const newPageIndex =
              //     transactionQuery.pageIndex! < transactions?.totalPages!
              //       ? transactionQuery.pageIndex! + 1
              //       : transactionQuery.pageIndex!;

              //   changePage(newPageIndex);
              // }}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </CardFooter>
    </Card>
  );
}
