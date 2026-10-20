import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    // Proxy de desarrollo: el panel llama a "/api/..." en su mismo
    // origen (localhost:5173) y Vite reenvía la petición al backend
    // FastAPI quitando el prefijo "/api". Como el navegador nunca
    // habla directamente con otro puerto, no hay bloqueos de CORS.
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
