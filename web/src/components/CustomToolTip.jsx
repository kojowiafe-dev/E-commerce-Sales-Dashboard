import React from "react";
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white dark:bg-gray-800 p-3 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
        <p className="text-sm font-semibold text-gray-900 dark:text-white">
          {label}
        </p>
        <p className="text-xs text-gray-500 dark:text-gray-400">
          Price:{" "}
          <span className="font-bold text-indigo-600 dark:text-indigo-400">
            ${payload[0].value}
          </span>
        </p>
      </div>
    );
  }
  return null;
};

export default CustomTooltip;
