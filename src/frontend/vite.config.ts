import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Damit Vite auf 0.0.0.0 lauscht
    port: 5173,
    // HIER DEINE DOMAIN ERLAUBEN:
    allowedHosts: [
      'user-story-api.saviwie.com'
    ]
  }
})