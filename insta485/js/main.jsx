import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Feed from "./feed";

// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM was /api/v1/posts/
root.render(
  <StrictMode>
    <Feed url="/api/v1/posts/" />
  </StrictMode>,
);
