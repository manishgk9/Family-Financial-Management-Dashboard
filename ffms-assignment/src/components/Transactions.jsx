import React from "react";
function Transactions() {
  return (
    <div className="bg-green-50 min-h-screen">
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Transactions
          </h2>
          <div className="bg-white shadow rounded-lg p-4">
            <div className="flex justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                Recent Transactions
              </h3>
              <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                Filter
              </button>
            </div>
            <TransactionList />
          </div>
        </div>
      </main>
    </div>
  );
}

const TransactionList = () => (
  <ul className="space-y-4">
    {[
      {
        date: "Feb 20, 2025",
        description: "Amazon Purchase",
        amount: "-$499.99",
        category: "Shopping",
      },
      {
        date: "Feb 19, 2025",
        description: "Salary Deposit",
        amount: "+$5,000.00",
        category: "Income",
      },
      {
        date: "Feb 18, 2025",
        description: "Utility Bill",
        amount: "-$150.00",
        category: "Bills",
      },
    ].map((txn, index) => (
      <li
        key={index}
        className="flex justify-between items-center border-b pb-2"
      >
        <div>
          <p className="text-sm font-medium text-gray-900">{txn.description}</p>
          <p className="text-sm text-gray-500">
            {txn.date} • {txn.category}
          </p>
        </div>
        <p
          className={`text-sm font-semibold ${
            txn.amount.startsWith("-") ? "text-red-500" : "text-green-500"
          }`}
        >
          {txn.amount}
        </p>
      </li>
    ))}
  </ul>
);

export default Transactions;
