import React from "react";
import { createBrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import Check from "./Check.jsx";


export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />
  },
  {
    path: "/Check",
    element: <Check />
  }
]

);