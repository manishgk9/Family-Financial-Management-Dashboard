import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link to="/">
                <span className="text-xl font-bold">FinDash</span>
              </Link>
            </div>
            <NavLinks />
          </div>
          <UserActions />
        </div>
      </div>
    </nav>
  );
}

const NavLinks = () => {
  const location = useLocation();
  const [currentIndex, setCurrentIndex] = useState(0);

  const navItems = [
    { name: "Dashboard", to: "/" },
    { name: "Assets", to: "/assets" },
    { name: "Transactions", to: "/transactions" },
    { name: "Settings", to: "/settings" },
  ];

  const routeIndex = navItems.findIndex(
    (item) => item.to === location.pathname
  );

  const activeIndex = routeIndex !== -1 ? routeIndex : -1;

  if (routeIndex !== -1 && activeIndex !== currentIndex) {
    setCurrentIndex(routeIndex);
  }

  return (
    <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
      {navItems.map((item, index) => (
        <Link
          key={index}
          to={item.to}
          className={`${
            currentIndex === index && activeIndex !== -1
              ? "border-b-2 border-indigo-500 text-gray-900"
              : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
          } inline-flex items-center px-1 pt-1 text-sm font-medium`}
          onClick={() => setCurrentIndex(index)}
        >
          {item.name}
        </Link>
      ))}
    </div>
  );
};

const UserActions = () => {
  const location = useLocation();
  const isNotifications = location.pathname === "/notifications";
  const isProfile = location.pathname === "/profile";

  return (
    <div className="flex items-center">
      <Link to="/notifications">
        <div
          className={`bg-white p-1 rounded-full ${
            isNotifications ? "text-indigo-500" : "text-gray-400"
          } hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
        >
          <span className="sr-only">View notifications</span>
          <i className="fas fa-bell"></i>
        </div>
      </Link>
      <div className="ml-3 relative">
        <Link to="/profile">
          <div
            className={`max-w-xs bg-white flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
              isProfile
                ? "border-2 border-indigo-500"
                : "border-2 border-transparent"
            }`}
            aria-haspopup="true"
            aria-expanded="false"
          >
            <span className="sr-only">Open user menu</span>
            <img
              className="h-8 w-8 rounded-full"
              src="https://placehold.co/32x32"
              alt="User avatar"
            />
          </div>
        </Link>
      </div>
    </div>
  );
};

export default Navbar;
