export type PaginationQuery = {
  pageSize?: number;
  pageIndex?: number;
};

export type PaginationResponse<T> = {
  data: T[];
  total: number;
  pageSize: number;
  pageIndex: number;
  totalPages: number;
};

export function getPageNumbers(
  pageIndex: number,
  totalPages: number
): number[] {
  const maxPagesToShow = 4;

  if (totalPages <= maxPagesToShow) {
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }

  let start = Math.max(1, pageIndex - Math.floor(maxPagesToShow / 2));
  let end = start + maxPagesToShow - 1;

  if (end > totalPages) {
    end = totalPages;
    start = end - maxPagesToShow + 1;
  }

  return Array.from({ length: maxPagesToShow }, (_, i) => start + i);
}
