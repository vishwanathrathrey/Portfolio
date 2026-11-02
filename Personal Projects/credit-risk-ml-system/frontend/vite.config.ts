import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  // Inside Docker Compose the API is reachable as http://api:8000, not localhost.
  const env = loadEnv(mode, '.', '');
  const apiTarget = env.API_PROXY_TARGET || 'http://localhost:8000';

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        '/health': apiTarget,
        '/metrics': apiTarget,
        '/predict': apiTarget,
      },
    },
  };
});
