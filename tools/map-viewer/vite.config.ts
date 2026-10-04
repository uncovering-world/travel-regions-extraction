import { defineConfig } from "vite";

// 5173 and 3000 are taken by other local apps (Track Your Regions); fail loudly instead of drifting to another port.
export default defineConfig({
  server: { port: 5199, strictPort: true },
  preview: { port: 5198, strictPort: true },
});
