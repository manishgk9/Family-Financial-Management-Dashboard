function FinDash() {
  return (
    <div className="bg-green-50 min-h-screen">
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card
              title="Bank Balance"
              amount="$124,500.00"
              change="+2.4% from last month"
              icon="fa-university"
            />
            <Card
              title="Investments"
              amount="$89,230.50"
              change="+5.1% from last month"
              icon="fa-chart-line"
            />
            <Card
              title="Property Value"
              amount="$450,000.00"
              change="+0.8% from last month"
              icon="fa-home"
            />
          </div>

          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
            <ChartCard title="Monthly Spending by Category" />
            <ChartCard title="Spending Trends" />
          </div>

          <Alerts />
        </div>
      </main>
    </div>
  );
}

// Card Component (unchanged)
const Card = ({ title, amount, change, icon }) => (
  <div className="bg-white shadow rounded-lg p-4">
    <div className="flex items-center justify-between">
      <div>
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <p className="text-2xl font-semibold text-gray-900">{amount}</p>
        <p className="text-sm text-green-500">{change}</p>
      </div>
      <i className={`fas ${icon} text-gray-400 text-2xl`}></i>
    </div>
  </div>
);

// ChartCard Component (unchanged)
const ChartCard = ({ title }) => (
  <div className="bg-white shadow rounded-lg p-4">
    <div className="flex items-center justify-between">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <i className="fas fa-ellipsis-h text-gray-400"></i>
    </div>
    <div className="mt-4 h-48 bg-gray-100 flex items-center justify-center">
      <span className="text-gray-400">Chart Visualization</span>
    </div>
  </div>
);

// Alerts Component (unchanged)
const Alerts = () => (
  <div className="mt-8">
    <h3 className="text-lg font-medium text-gray-900">Alerts & Reminders</h3>
    <ul className="mt-4 space-y-4">
      {[
        {
          title: "Car Insurance Renewal",
          subtitle: "Due in 5 days - March 15, 2025",
        },
        {
          title: "Credit Card Payment",
          subtitle: "Due in 2 days - March 12, 2025",
        },
        {
          title: "Unusual Transaction Detected",
          subtitle: "Amazon Purchase - $499.99",
        },
      ].map((alert, index) => (
        <li
          key={index}
          className="bg-white shadow rounded-lg p-4 flex items-center justify-between"
        >
          <div>
            <p className="text-sm font-medium text-gray-900">{alert.title}</p>
            <p className="text-sm text-gray-500">{alert.subtitle}</p>
          </div>
          <button className="text-gray-400 hover:text-gray-500">
            <i className="fas fa-times"></i>
          </button>
        </li>
      ))}
    </ul>
  </div>
);

export default FinDash;
