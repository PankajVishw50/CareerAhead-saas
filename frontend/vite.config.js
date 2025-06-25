import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"



// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 7600,
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: "http://backend:7575",
      },
      "/ws": {
        target: "ws://backend:7575",
        ws: true
      },
    }
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  }
})
