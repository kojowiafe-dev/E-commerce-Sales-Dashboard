import React, { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
} from "@tanstack/react-table";
import { useQuery } from "@tanstack/react-query";
import {
  MagnifyingGlassIcon,
  ChevronUpIcon,
  ChevronDownIcon,
} from "@heroicons/react/24/outline";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "../components/ui/pagination";
import api from "../api";

const pageSize = 10;

const fetchProducts = async ({ queryKey }) => {
  const [_key, page, search] = queryKey;
  const response = await api.get("/products/", {
    params: { page, limit: pageSize, search },
  });
  return response.data;
};

const Server = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchText, setSearchText] = useState("");

  const { data, isLoading, error, isFetching } = useQuery({
    queryKey: ["products", currentPage, searchText],
    queryFn: fetchProducts,
    keepPreviousData: true,
  });

  const products = data?.items ?? [];
  const totalPages = Math.ceil((data?.total ?? 0) / pageSize);

  const columns = useMemo(
    () => [
      {
        accessorKey: "product_id",
        header: "Product ID",
        cell: (info) => <span>{info.getValue()}</span>,
      },
      {
        accessorFn: (row) => `${row.name}`,
        id: "name",
        header: "Product",
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: "price_each",
        header: "Price Each",
        cell: (info) => (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
            {info.getValue()}
          </span>
        ),
      },
    ],
    []
  );

  const table = useReactTable({
    data: products,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      globalFilter: searchText,
    },
    onGlobalFilterChange: setSearchText,
  });

  if (isLoading) {
    return (
      <div className="p-4 text-gray-700 dark:text-gray-200">Loading...</div>
    );
  }

  if (error) {
    return <div className="p-4 text-red-500">Error loading products.</div>;
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-8 pt-8 bg-white dark:bg-gray-900 h-full">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-poppins font-bold text-gray-900 dark:text-white">
            Products
          </h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-400 font-bold">
            A list of all products.
          </p>
        </div>
      </div>

      {/* Search Input */}
      <div className="mt-8 flex flex-col">
        <div className="relative rounded-md shadow-sm mb-4">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <MagnifyingGlassIcon className="h-5 w-5 font-bold text-gray-400" />
          </div>
          <input
            type="text"
            value={searchText}
            onChange={(e) => {
              setSearchText(e.target.value);
              setCurrentPage(1); // reset to first page on search
            }}
            className="block w-full rounded-md font-bold border-0 py-1.5 pl-10 text-gray-900 dark:text-white ring-1 ring-inset ring-gray-300 dark:ring-gray-700 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 outline-0 bg-white dark:bg-gray-800"
            placeholder="Search products..."
          />
        </div>

        {/* Table */}
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg bg-white dark:bg-gray-900">
              <table className="min-w-full divide-y divide-gray-300 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  {table.getHeaderGroups().map((headerGroup) => (
                    <tr key={headerGroup.id}>
                      {headerGroup.headers.map((header) => (
                        <th
                          key={header.id}
                          className="px-3 py-3.5 text-left text-sm font-bold text-gray-900 dark:text-white"
                          colSpan={header.colSpan}
                        >
                          {header.isPlaceholder ? null : (
                            <div
                              {...{
                                className: header.column.getCanSort()
                                  ? "cursor-pointer select-none"
                                  : "",
                                onClick:
                                  header.column.getToggleSortingHandler(),
                              }}
                            >
                              {flexRender(
                                header.column.columnDef.header,
                                header.getContext()
                              )}
                              {{
                                asc: (
                                  <ChevronUpIcon className="h-4 w-4 inline" />
                                ),
                                desc: (
                                  <ChevronDownIcon className="h-4 w-4 inline" />
                                ),
                              }[header.column.getIsSorted()] ?? null}
                            </div>
                          )}
                        </th>
                      ))}
                    </tr>
                  ))}
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
                  {table.getRowModel().rows.map((row) => (
                    <tr key={row.id}>
                      {row.getVisibleCells().map((cell) => (
                        <td
                          key={cell.id}
                          className="whitespace-nowrap px-3 py-4 text-sm font-bold text-gray-500 dark:text-gray-300"
                        >
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Pagination */}
        <Pagination
          className="mt-6 font-bold text-black dark:text-white"
          current={currentPage}
          total={totalPages}
          onChange={(page) => setCurrentPage(Number(page))}
        >
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
              />
            </PaginationItem>

            {Array.from({ length: totalPages }).map((_, i) => (
              <PaginationItem key={i}>
                <PaginationLink
                  isActive={currentPage === i + 1}
                  onClick={() => setCurrentPage(i + 1)}
                >
                  {i + 1}
                </PaginationLink>
              </PaginationItem>
            ))}
            <PaginationItem>
              <PaginationNext
                onClick={() =>
                  setCurrentPage((p) => Math.min(p + 1, totalPages))
                }
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>

        {isFetching && (
          <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Updating…
          </div>
        )}
      </div>
    </div>
  );
};

export default Server;

// useEffect(() => {
//   const fetchProducts = async () => {
//     try {
//       setLoading(true);
//       const response = await api.get(`/products/`, {
//         params: { page: currentPage, limit: pageSize, search: searchText },
//       });
//       setProducts(response.data.items);
//       setTotalPages(Math.ceil(response.data.total / pageSize));
//       console.log("Page:", currentPage, "Products:", response.data.items);
//     } catch (error) {
//       console.error(error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   fetchProducts();
// }, [currentPage, pageSize, searchText]);
