import * as React from "react";
import * as ReactDOM from "react-dom/client";
import axios from 'axios';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Root, { loader as rootLoader } from "./root.jsx";
import Login, { action as loginAction } from "./login.jsx";
import Map from "./map.jsx";
import Event from "./event.jsx";
import Client from "./client.jsx";


axios.defaults.baseURL = import.meta.env.VITE_SNOW_API_SERVER;
axios.defaults.withCredentials = true;

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    loader: rootLoader,
    children: [
      {
        element: <Home />,
        index: true,
      },
      {
        path: "/map",
        element: <Map />,
      },
      {
        path: "/event",
        element: <Event />
      },
      {
        path: "/client",
        element: <Client />
      }
    ]
  },
  {
    path: '/auth/login',
    element: <Login />,
    action: loginAction
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

