import path from "path"
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [react()],
  test: {
    include: ['**/*.test.tsx'],
    environment: "jsdom",
    globals: true,
    setupFiles: [path.resolve(__dirname, 'src/tests/setup.ts')],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})