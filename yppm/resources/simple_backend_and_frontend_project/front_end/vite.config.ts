import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import legacy from '@vitejs/plugin-legacy'

import { resolve } from 'path'
const pathResolve = (dir: string): any => resolve(__dirname, '.', dir)

// https://vitejs.dev/config/

export default defineConfig({
  plugins: [
    vue(),
    legacy({
      polyfills: ['es.promise.finally', 'es/map', 'es/set'],
      modernPolyfills: ['es.promise.finally'],
      targets: ['defaults', 'not IE 11'],
    }),
  ],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
        additionalData: `@import "${pathResolve('src')}/assets/less/variables.less";`
      }
    },
  },
})
