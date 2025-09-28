import React, { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
} from "@tanstack/react-table";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import CustomTooltip from "../components/CustomToolTip";
import { useQuery } from "@tanstack/react-query";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import Page from "../components/Page";
import api from "../api/api";

const pageSize = 10;

const fetchOrderItems = async ({ queryKey }) => {
  const [_key, page, search] = queryKey;
  const response = await api.get("/order-items/", {
    params: { page, limit: pageSize, search },
  });
  return response.data;
};

const OrderItems = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchText, setSearchText] = useState("");

  const { data, isLoading, error } = useQuery({
    queryKey: ["order-items", currentPage, searchText],
    queryFn: fetchOrderItems,
    keepPreviousData: true,
  });

  const orderItems = useMemo(() => data?.items ?? [], [data?.items]);
  const totalPages = Math.ceil((data?.total ?? 0) / pageSize);

  // Chart data (line_total per product)
  const chartData = useMemo(() => {
    return orderItems.map((item) => ({
      order_item_id: item.order_item_id,
      product: item.product?.name ?? "Unknown",
      price_each: item.price_each ?? 0,
      quantity: item.quantity ?? 0,
      line_total: item.line_total ?? 0,
      order_date: item.order?.order_date ?? "",
    }));
  }, [orderItems]);

  const columns = useMemo(
    () => [
      {
        accessorKey: "order_item_id",
        header: "Item ID",
        cell: (info) => <span>{info.getValue()}</span>,
      },
      {
        accessorFn: (row) => row.product?.name ?? "",
        id: "product",
        header: "Product",
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: "quantity",
        header: "Quantity",
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: "price_each",
        header: "Price Each",
        cell: (info) => `$${info.getValue().toFixed(2)}`,
      },
      {
        accessorKey: "line_total",
        header: "Line Total",
        cell: (info) => `$${info.getValue().toFixed(2)}`,
      },
      {
        accessorFn: (row) => row.order?.purchase_address ?? "",
        id: "purchase_address",
        header: "Purchase Address",
        cell: (info) => info.getValue(),
      },
    ],
    []
  );

  const table = useReactTable({
    data: orderItems,
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
    return <div className="p-4 text-red-500">Error loading order items.</div>;
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-8 pt-8 bg-white dark:bg-gray-900">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-poppins font-bold text-gray-900 dark:text-white">
            Order Items
          </h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-400">
            A list of all order items.
          </p>
        </div>
      </div>

      <div className="mt-8 flex flex-col">
        {/* Search Input */}
        <div className="relative rounded-md shadow-sm mb-4">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={searchText}
            onChange={(e) => {
              setSearchText(e.target.value);
              setCurrentPage(1);
            }}
            className="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 dark:text-white ring-1 ring-inset ring-gray-300 dark:ring-gray-700 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 outline-0 bg-white dark:bg-gray-800"
            placeholder="Search order items..."
          />
        </div>

        {/* Table */}
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

          {/* Chart */}
          <div className="mt-6 w-full h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={chartData}
                margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#82ca9d" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="product" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="line_total"
                  stroke="#82ca9d"
                  fillOpacity={1}
                  fill="url(#colorTotal)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pagination */}
        <Page
          currentPage={currentPage}
          totalPages={totalPages}
          setCurrentPage={setCurrentPage}
        />
      </div>
    </div>
  );
};

export default OrderItems;
