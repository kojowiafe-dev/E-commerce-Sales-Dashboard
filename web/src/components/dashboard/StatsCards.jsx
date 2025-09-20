import React from "react";
import { Card, CardHeader, CardContent } from "../ui/card";

const stats = [
  { label: "Total Products", value: 120, color: "text-blue-600" },
  { label: "Total Orders", value: 340, color: "text-green-600" },
  { label: "Revenue", value: "$12,400", color: "text-purple-600" },
  { label: "Customers", value: 89, color: "text-yellow-600" },
];

const StatsCards = () => (
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
    {stats.map((stat) => (
      <Card key={stat.label} className="shadow rounded-xl">
        <CardHeader className="pb-2 text-sm font-medium text-gray-500 dark:text-gray-400">
          {stat.label}
        </CardHeader>
        <CardContent
          className={`text-2xl font-bold ${stat.color} dark:text-opacity-90`}
        >
          {stat.value}
        </CardContent>
      </Card>
    ))}
  </div>
);

export default StatsCards;
