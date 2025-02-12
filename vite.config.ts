import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  // base: '/',
  base: 'https://github.com/maastrichtlawtech/legal-network-textbook',
  plugins: [vue()],
  esbuild: {
    target: 'es2022' // Explicitly set the target for esbuild
  }
})
