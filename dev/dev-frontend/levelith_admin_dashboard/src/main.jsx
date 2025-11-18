import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { DataSourceProvider } from "./context/DataSourceContext";
import App from "./App";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <DataSourceProvider>
      <App />
    </DataSourceProvider>
  </BrowserRouter>
);
