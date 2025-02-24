import React from "react";
function Assets() {
  return (
    <div className="bg-green-50 min-h-screen">
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Assets</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <AssetCard
              title="Bank Account"
              value="$124,500.00"
              type="Checking"
              icon="fa-university"
            />
            <AssetCard
              title="Investment Portfolio"
              value="$89,230.50"
              type="Stocks"
              icon="fa-chart-line"
            />
            <AssetCard
              title="Property"
              value="$450,000.00"
              type="Real Estate"
              icon="fa-home"
            />
          </div>
          <div className="mt-8">
            <AssetSummary />
          </div>
        </div>
      </main>
    </div>
  );
}

const AssetCard = ({ title, value, type, icon }) => (
  <div className="bg-white shadow rounded-lg p-4">
    <div className="flex items-center justify-between">
      <div>
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <p className="text-2xl font-semibold text-gray-900">{value}</p>
        <p className="text-sm text-gray-500">{type}</p>
      </div>
      <i className={`fas ${icon} text-gray-400 text-2xl`}></i>
    </div>
  </div>
);

const AssetSummary = () => (
  <div className="bg-white shadow rounded-lg p-4">
    <h3 className="text-lg font-medium text-gray-900">Total Asset Value</h3>
    <p className="text-3xl font-semibold text-gray-900 mt-2">$663,730.50</p>
    <p className="text-sm text-green-500 mt-1">+3.1% from last month</p>
  </div>
);

export default Assets;
