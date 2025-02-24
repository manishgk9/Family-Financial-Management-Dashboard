import React from "react";

function Settings() {
  return (
    <div className="bg-green-50 min-h-screen">
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Settings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <SettingsCard title="User Roles" content={<RoleSettings />} />
            <SettingsCard
              title="Notification Preferences"
              content={<NotificationSettings />}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

const SettingsCard = ({ title, content }) => (
  <div className="bg-white shadow rounded-lg p-4">
    <h3 className="text-lg font-medium text-gray-900">{title}</h3>
    <div className="mt-4">{content}</div>
  </div>
);

const RoleSettings = () => (
  <div>
    <p className="text-sm text-gray-500">Manage family member roles</p>
    <ul className="mt-2 space-y-2">
      <li className="flex justify-between">
        <span>Admin: John Doe</span>
        <button className="text-indigo-600 hover:text-indigo-800">Edit</button>
      </li>
      <li className="flex justify-between">
        <span>Member: Jane Doe</span>
        <button className="text-indigo-600 hover:text-indigo-800">Edit</button>
      </li>
    </ul>
  </div>
);

const NotificationSettings = () => (
  <div>
    <p className="text-sm text-gray-500">Customize alerts</p>
    <div className="mt-2 space-y-2">
      <label className="flex items-center">
        <input type="checkbox" className="mr-2" defaultChecked />
        <span>Email Alerts</span>
      </label>
      <label className="flex items-center">
        <input type="checkbox" className="mr-2" />
        <span>SMS Alerts</span>
      </label>
    </div>
  </div>
);

export default Settings;
