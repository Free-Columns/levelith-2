import React from "react";
import { Routes, Route } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import Experiences from "./pages/Experiences";
import NAICSCodes from "./pages/NAICSCodes";
import Settings from "./pages/Settings";
import Login from "./pages/Login";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<AdminLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="users" element={<Users />} />
        <Route path="experiences" element={<Experiences />} />
        <Route path="naics" element={<NAICSCodes />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
