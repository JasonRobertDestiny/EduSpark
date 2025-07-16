import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // 可添加更多别名（可选）
      '~assets': path.resolve(__dirname, './src/assets')
    },
    // 明确包含的扩展名（针对Vue文件）
    extensions: ['.js', '.vue', '.json']
  },
  server: {
    fs: {
      allow: [path.resolve(__dirname)]
    },
    // 开发服务器端口配置（可选）
    port: 5173,
    open: true
  },
  build: {
    rollupOptions: {
      output: {
        assetFileNames: 'assets/[name].[hash].[ext]'
      }
    }
  },
  assetsInclude: ['**/*.jpg', '**/*.png', '**/*.svg']
})