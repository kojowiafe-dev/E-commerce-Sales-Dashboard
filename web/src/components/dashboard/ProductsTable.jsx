import React from "react";
import { Card, CardHeader, CardContent } from "../ui/card";

const products = [
  { name: "Wireless Mouse", price: 29.99, stock: 120, sold: 80 },
  { name: "Bluetooth Headphones", price: 59.99, stock: 60, sold: 45 },
  { name: "USB-C Charger", price: 19.99, stock: 200, sold: 150 },
  { name: "Laptop Stand", price: 39.99, stock: 75, sold: 60 },
];

const ProductsTable = () => (
  <Card className="shadow rounded-xl mb-6">
    <CardHeader className="pb-2 text-lg font-semibold text-blue-700 dark:text-blue-300">
      Products
    </CardHeader>
    <CardContent className="overflow-x-auto p-0">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
        <thead className="bg-gray-50 dark:bg-gray-900">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              Name
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              Price
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              Stock
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              Sold
            </th>
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-950 divide-y divide-gray-100 dark:divide-gray-900">
          {products.map((product) => (
            <tr
              key={product.name}
              className="hover:bg-blue-50 dark:hover:bg-blue-900/30 transition"
            >
              <td className="px-4 py-2 font-medium text-gray-700 dark:text-gray-200">
                {product.name}
              </td>
              <td className="px-4 py-2 text-gray-600 dark:text-gray-300">
                ${product.price.toFixed(2)}
              </td>
              <td className="px-4 py-2 text-gray-600 dark:text-gray-300">
                {product.stock}
              </td>
              <td className="px-4 py-2 text-gray-600 dark:text-gray-300">
                {product.sold}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </CardContent>
  </Card>
);

export default ProductsTable;
