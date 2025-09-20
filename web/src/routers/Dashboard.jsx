import React from "react";
import StatsCards from "../components/dashboard/StatsCards";
import ProductsTable from "../components/dashboard/ProductsTable";
import SalesChart from "../components/dashboard/SalesChart";

const Dashboard = () => (
  <div className="space-y-6">
    <StatsCards />
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <ProductsTable />
      <SalesChart />
    </div>
  </div>
);

export default Dashboard;
