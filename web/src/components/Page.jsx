import React from "react";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "./ui/pagination";

const Page = ({ currentPage, totalPages, setCurrentPage }) => {
  // const orders = data?.items ?? [];
  // const totalPages = Math.ceil((data?.total ?? 0) / pageSize);

  const pageNumbers = [];
  const maxVisible = 5;

  let start = Math.max(currentPage - Math.floor(maxVisible / 2), 1);
  let end = Math.min(start + maxVisible - 1, totalPages);

  if (end - start + 1 < maxVisible) {
    start = Math.max(end - maxVisible + 1, 1);
  }

  for (let i = start; i <= end; i++) {
    pageNumbers.push(i);
  }

  return (
    <Pagination
      className="mt-6 dark:text-white text-gray-900"
      current={currentPage}
      total={totalPages}
    >
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          />
        </PaginationItem>

        {/* Always show first page */}
        {start > 1 && (
          <>
            <PaginationItem>
              <PaginationLink onClick={() => setCurrentPage(1)}>
                1
              </PaginationLink>
            </PaginationItem>
            {start > 2 && <span className="px-2">...</span>}
          </>
        )}

        {/* Middle pages */}
        {pageNumbers.map((page) => (
          <PaginationItem key={page}>
            <PaginationLink
              isActive={currentPage === page}
              onClick={() => setCurrentPage(page)}
            >
              {page}
            </PaginationLink>
          </PaginationItem>
        ))}

        {/* Always show last page */}
        {end < totalPages && (
          <>
            {end < totalPages - 1 && <span className="px-2">...</span>}
            <PaginationItem>
              <PaginationLink onClick={() => setCurrentPage(totalPages)}>
                {totalPages}
              </PaginationLink>
            </PaginationItem>
          </>
        )}

        <PaginationItem>
          <PaginationNext
            onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
};

export default Page;
