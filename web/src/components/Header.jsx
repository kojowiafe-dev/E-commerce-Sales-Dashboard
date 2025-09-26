import React from "react";
import ModeToggle from "./mode-toggle";
import { AnimatedThemeToggler } from "../components/ui/animated-theme-toggler";

const Header = ({ onMenuClick }) => (
  <header className="sticky top-0 z-20 w-full h-16 flex items-center justify-between bg-white dark:bg-gray-900 shadow px-4 border-b border-gray-200 dark:border-gray-800">
    <button
      className="md:hidden dark:text-white flex items-center justify-center p-2 rounded hover:bg-blue-100 dark:hover:bg-blue-900"
      onClick={onMenuClick}
      aria-label="Open sidebar"
    >
      <svg
        width="24"
        height="24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="lucide lucide-menu"
      >
        <line x1="4" y1="12" x2="20" y2="12" />
        <line x1="4" y1="6" x2="20" y2="6" />
        <line x1="4" y1="18" x2="20" y2="18" />
      </svg>
    </button>
    <div className="font-semibold text-lg text-blue-600 dark:text-blue-400">
      Sales Dashboard
    </div>
    <div>
      <AnimatedThemeToggler />
    </div>
  </header>
);

export default Header;
