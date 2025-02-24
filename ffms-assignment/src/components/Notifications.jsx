// Notifications.js
import React, { useState } from "react";

const Notifications = () => {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      title: "Car Insurance Renewal",
      subtitle: "Due in 5 days - March 15, 2025",
      type: "reminder",
    },
    {
      id: 2,
      title: "Credit Card Payment",
      subtitle: "Due in 2 days - March 12, 2025",
      type: "reminder",
    },
    {
      id: 3,
      title: "Unusual Transaction Detected",
      subtitle: "Amazon Purchase - $499.99",
      type: "alert",
    },
  ]);

  const handleDismiss = (id) => {
    setNotifications(notifications.filter((notif) => notif.id !== id));
  };

  return (
    <div className="bg-green-50 min-h-screen">
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Notifications
          </h2>
          <div className="bg-white shadow rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Recent Notifications
            </h3>
            {notifications.length === 0 ? (
              <p className="text-gray-500">No notifications at this time.</p>
            ) : (
              <ul className="space-y-4">
                {notifications.map((notif) => (
                  <li
                    key={notif.id}
                    className="flex justify-between items-center border-b pb-2"
                  >
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {notif.title}
                      </p>
                      <p className="text-sm text-gray-500">{notif.subtitle}</p>
                      <span
                        className={`text-xs px-2 py-1 rounded-full ${
                          notif.type === "alert"
                            ? "bg-red-100 text-red-800"
                            : "bg-blue-100 text-blue-800"
                        }`}
                      >
                        {notif.type}
                      </span>
                    </div>
                    <button
                      onClick={() => handleDismiss(notif.id)}
                      className="text-gray-400 hover:text-gray-500"
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Notifications;
