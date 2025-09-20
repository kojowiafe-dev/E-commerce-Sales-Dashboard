import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import Overview from "./routers/Overview";
import Products from "./routers/Products";
import Orders from "./routers/Orders";
import OrderItems from "./routers/OrderItems";
import Login from "./routers/Login";
import Register from "./routers/Register";
import Dashboard from "./routers/Dashboard";
import { ThemeProvider } from "./components/theme-provider";

const Layout = ({ children, onLogout }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex">
      {/* Sidebar for desktop */}
      <div className="hidden md:block">
        <Sidebar onLogout={onLogout} />
      </div>
      {/* Sidebar drawer for mobile */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 flex md:hidden">
          <div
            className="fixed inset-0 bg-black/40"
            onClick={() => setSidebarOpen(false)}
          ></div>
          <div className="relative w-64">
            <Sidebar onLogout={onLogout} />
          </div>
        </div>
      )}
      <div className="flex-1 flex flex-col min-h-screen ml-0 md:ml-64">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
          <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">
            {children}
          </main>
        </ThemeProvider>
      </div>
    </div>
  );
};

const AppRoutes = () => {
  const navigate = useNavigate();
  const handleLogout = () => {
    // Clear session/token logic here
    navigate("/login");
  };
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/*"
        element={
          <Layout onLogout={handleLogout}>
            <Routes>
              <Route path="/" element={<Overview />} />
              <Route path="/products" element={<Products />} />
              <Route path="/orders" element={<Orders />} />
              <Route path="/order-items" element={<OrderItems />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </Layout>
        }
      />
    </Routes>
  );
};

const App = () => (
  <Router>
    <AppRoutes />
  </Router>
);

export default App;
