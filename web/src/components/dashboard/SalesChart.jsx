import React from "react";
import { Card, CardHeader, CardContent } from "../ui/card";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { date: "2025-09-01", sales: 400 },
  { date: "2025-09-02", sales: 600 },
  { date: "2025-09-03", sales: 300 },
  { date: "2025-09-04", sales: 700 },
  { date: "2025-09-05", sales: 500 },
  { date: "2025-09-06", sales: 800 },
  { date: "2025-09-07", sales: 650 },
];

const SalesChart = () => (
  <Card className="shadow rounded-xl mb-6">
    <CardHeader className="pb-2 text-lg font-semibold text-blue-700 dark:text-blue-300">
      Sales Analysis
    </CardHeader>
    <CardContent className="h-72 p-0">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 16, right: 24, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" tick={{ fill: "#64748b", fontSize: 12 }} />
          <YAxis tick={{ fill: "#64748b", fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              background: "#fff",
              borderRadius: 8,
              boxShadow: "0 2px 8px #0001",
            }}
          />
          <Line
            type="monotone"
            dataKey="sales"
            stroke="#2563eb"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </CardContent>
  </Card>
);

export default SalesChart;
