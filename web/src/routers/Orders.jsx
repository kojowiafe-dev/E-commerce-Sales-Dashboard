import React, { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
} from "@tanstack/react-table";
import { useQuery } from "@tanstack/react-query";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import Page from "../components/Page";
import api from "../api/api";

const pageSize = 10;

const fetchOrders = async ({ queryKey }) => {
  const [_key, page, search] = queryKey;
  const response = await api.get("/orders/", {
    params: { page, limit: pageSize, search },
  });
  return response.data;
};

const Orders = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchText, setSearchText] = useState("");

  const { data, isLoading, error } = useQuery({
    queryKey: ["orders", currentPage, searchText],
    queryFn: fetchOrders,
    keepPreviousData: true,
  });

  const orders = data?.items ?? [];
  const totalPages = Math.ceil((data?.total ?? 0) / pageSize);

  const columns = useMemo(
    () => [
      {
        accessorKey: "order_id",
        header: "Order ID",
        cell: (info) => {
          const order = info.getValue();
          const colors = {
            married: "bg-green-100 text-green-800",
            single: "bg-blue-100 text-blue-800",
            divorced: "bg-orange-100 text-orange-800",
          };
          return (
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                colors[status] || "bg-gray-100 text-gray-800"
              }`}
            >
              {order}
            </span>
          );
        },
      },
      {
        accessorFn: (row) => row.items[0]?.product?.name ?? "",
        id: "name",
        header: "Product",
        cell: (info) => info.getValue(),
      },
      {
        accessorFn: (row) => row.items[0]?.product?.price_each ?? "",
        header: "Price Each",
        cell: (info) => (
          <span
            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              info.getValue() === "male"
                ? "bg-blue-100 text-blue-800"
                : "bg-pink-100 text-pink-800"
            }`}
          >
            {info.getValue()}
          </span>
        ),
      },
      {
        accessorFn: (row) => `${row.purchase_address}`,
        id: "purchase_address",
        header: "Purchase Address",
        cell: (info) => info.getValue(),
      },
    ],
    []
  );

  const table = useReactTable({
    data: orders,
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
      <div className="flex justify-center items-center h-64">
        <svg
          className="animate-spin h-10 w-10 text-blue-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
          ></path>
        </svg>
      </div>
    );
  }

  if (error) {
    return <div className="p-4 text-red-500">Error loading products.</div>;
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-8 pt-8 bg-white dark:bg-gray-900">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-poppins font-bold text-gray-900 dark:text-white">
            Orders
          </h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-400">
            A list of all orders.
          </p>
        </div>
      </div>

      <div className="mt-8 flex flex-col">
        <div className="relative rounded-md shadow-sm mb-4">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={searchText}
            onChange={(e) => {
              setSearchText(e.target.value);
              setCurrentPage(1); // reset to first page on search
            }}
            className="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 dark:text-white ring-1 ring-inset ring-gray-300 dark:ring-gray-700 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 outline-0 bg-white dark:bg-gray-800"
            placeholder="Search orders..."
          />
        </div>

        <div className="-mx-4 -my-2 sm:-mx-6 lg:-mx-8">
          <div className="py-2 align-middle sm:px-6 lg:px-8 min-w-full">
            <div className="overflow-x-auto w-full">
              <table className="min-w-[900px] divide-y divide-gray-300 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  {table.getHeaderGroups().map((headerGroup) => (
                    <tr key={headerGroup.id}>
                      {headerGroup.headers.map((header) => (
                        <th
                          key={header.id}
                          className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white"
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
                          className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-300"
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

        {/* Pagination UI */}

        <Page
          currentPage={currentPage}
          totalPages={totalPages}
          setCurrentPage={setCurrentPage}
        />
      </div>

      {/* Delete Confirmation Modal */}
    </div>
  );
};

export default Orders;
