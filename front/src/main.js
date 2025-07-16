import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/index.js'

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const role = localStorage.getItem('role');
  const username = localStorage.getItem('username');

  if (requiresAuth && !username) {
    // 如果需要认证但用户未登录，则重定向到登录页
    next('/login');
  } else if (requiresAuth && to.meta.role && to.meta.role !== role) {
    // 如果需要特定角色但用户角色不匹配，则重定向到登录页
    // 你也可以重定向到一个“无权限”页面
    next('/login');
  } else {
    // 否则，正常导航
    next();
  }
});

const app = createApp(App);

app.use(router);

app.mount('#app');
