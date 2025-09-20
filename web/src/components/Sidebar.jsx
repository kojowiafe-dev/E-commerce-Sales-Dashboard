import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Home, ShoppingCart, List, Package, LogOut } from "lucide-react";

const navItems = [
  { name: "Dashboard", icon: <Home size={20} />, path: "/" },
  { name: "Products", icon: <Package size={20} />, path: "/products" },
  { name: "Orders", icon: <ShoppingCart size={20} />, path: "/orders" },
  { name: "Order Items", icon: <List size={20} />, path: "/order-items" },
  { name: "Dashboard", icon: <List size={20} />, path: "/dashboard" },
];

const Sidebar = ({ onLogout }) => {
  const location = useLocation();
  return (
    <aside className="bg-white dark:bg-gray-900 shadow-lg h-full flex flex-col w-64 fixed z-30 top-0 left-0 border-r border-gray-200 dark:border-gray-800">
      <div className="flex items-center justify-center h-16 font-bold text-xl tracking-tight text-blue-600 dark:text-blue-400 border-b border-gray-200 dark:border-gray-800">
        E-Commerce
      </div>
      <nav className="flex-1 py-4 px-2 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors font-medium text-gray-700 dark:text-gray-200 hover:bg-blue-100 dark:hover:bg-blue-900 hover:text-blue-700 dark:hover:text-blue-300 ${
              location.pathname === item.path
                ? "bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300"
                : ""
            }`}
          >
            {item.icon}
            {item.name}
          </Link>
        ))}
        <button
          onClick={onLogout}
          className="flex items-center gap-3 px-4 py-2 rounded-lg transition-colors font-medium text-gray-700 dark:text-gray-200 hover:bg-red-100 dark:hover:bg-red-900 hover:text-red-700 dark:hover:text-red-300 w-full mt-8"
        >
          <LogOut size={20} /> Logout
        </button>
      </nav>
    </aside>
  );
};

export default Sidebar;
