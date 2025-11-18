import React from "react";
import { Outlet, Link } from "react-router-dom";

export default function AdminLayout() {
  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-gray-900 text-white p-4">
        <h2 className="text-xl font-bold mb-6">Levelith Admin</h2>
        <nav className="space-y-3">
          <Link to="/" className="block hover:text-blue-300">Dashboard</Link>
          <Link to="/users" className="block hover:text-blue-300">Users</Link>
          <Link to="/experiences" className="block hover:text-blue-300">Experiences</Link>
          <Link to="/settings" className="block hover:text-blue-300">Settings</Link>
        </nav>
      </aside>
      <main className="flex-1 p-6 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
