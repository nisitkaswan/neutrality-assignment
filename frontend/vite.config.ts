import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 3000, // This is the port which we will use in docker
    // Thanks to the host: true setting above, the server will accept connections on all network interfaces (0.0.0.0)
    watch: {
      usePolling: true
    }
  }
})