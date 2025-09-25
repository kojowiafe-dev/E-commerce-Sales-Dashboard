import React from "react";

const PageCard = ({ title, children }) => (
  <div className="bg-white dark:bg-gray-900 shadow p-6">
    {title && (
      <h2 className="text-xl font-semibold mb-4 text-blue-700 dark:text-blue-300">
        {title}
      </h2>
    )}
    {children}
  </div>
);

export default PageCard;
