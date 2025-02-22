import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"



// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 7600,
    proxy: {
      "/api": {
        target: "http://localhost:7575",
      }
    }
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  }
})
