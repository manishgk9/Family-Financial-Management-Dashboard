import React from "react";
import FinDash from "./components/Findash";
import Settings from "./components/Settings";
import Assets from "./components/Assets";
import Navbar from "./components/Navbar";
import Transactions from "./components/Transactions";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Profile from "./components/Profile";
import Notifications from "./components/Notifications";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<FinDash />} />
        <Route path="/assets" element={<Assets />} />
        <Route path="/transactions" element={<Transactions />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Router>
  );
}

export default App;
