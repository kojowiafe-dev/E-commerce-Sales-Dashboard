import React, { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
} from "@tanstack/react-table";
import { Dialog, Transition } from "@headlessui/react";
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

const Orders = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState("");
  const navigate = useNavigate();

  const pageSize = 10;

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/orders/`, {
          params: { page: currentPage, limit: pageSize, search: searchText },
        });
        setOrders(response.data.items);
        setTotalPages(Math.ceil(response.data.total / pageSize));
        console.log("Page:", currentPage, "Orders:", response.data.items);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [currentPage, pageSize, searchText]);

  // const totalPages = Math.ceil(products.length / pageSize)

  const currentOrders = orders;

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
    data: currentOrders,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      globalFilter: searchText,
    },
    onGlobalFilterChange: setSearchText,
  });

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
        {/* <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            onClick={() => navigate("/members/new")}
            className="inline-flex cursor-pointer items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Member
          </button>
        </div> */}
      </div>

      <div className="mt-8 flex flex-col">
        <div className="relative rounded-md shadow-sm mb-4">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            className="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 dark:text-white ring-1 ring-inset ring-gray-300 dark:ring-gray-700 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 outline-0 bg-white dark:bg-gray-800"
            placeholder="Search products..."
          />
        </div>

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
                          className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white"
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
        {/* <Pagination
          className="mt-6"
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
        </Pagination> */}
      </div>

      {/* Delete Confirmation Modal */}
    </div>
  );
};

export default Orders;
