import React from "react";
import { Routes, Route } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import Dashboard from "./pages/admin/Dashboard";
import Users from "./pages/admin/Users";
import Experiences from "./pages/admin/Experiences";
import NAICSCodes from "./pages/admin/NAICSCodes";
import Settings from "./pages/admin/Settings";
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
