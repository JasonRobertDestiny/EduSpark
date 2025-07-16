<template>
  <div class="login-container">
    <!-- 添加背景图片容器 -->
    <div class="login-background"></div>
    <div class="login-box">
    
      
      <h2>计算机智能教学管理平台</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <div class="input-wrapper">
            <i class="icon-user"></i>
            <input v-model="username" id="username" type="text" placeholder="请输入用户名" required />
          </div>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-wrapper">
            <i class="icon-lock"></i>
            <input v-model="password" id="password" type="password" placeholder="请输入密码" required />
          </div>
        </div>
        <div class="form-group">
          <label for="role">角色</label>
          <div class="input-wrapper">
            <i class="icon-role"></i>
            <select v-model="role" id="role" required>
              <option value="teacher">老师</option>
              <option value="student">学生</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="submit" class="login-btn">登录</button>
          <button type="button" @click="goToRegister" class="register-btn">注册</button>
        </div>
        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
      </form>
    </div>
    <!-- 添加飘落的星星动画 -->
    <div class="stars">
      <div class="star star-1"></div>
      <div class="star star-2"></div>
      <div class="star star-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const password = ref('');
const role = ref('teacher'); // 默认角色为老师
const errorMsg = ref('');

const handleLogin = () => {
  if (!username.value || !password.value) {
    errorMsg.value = '请输入用户名和密码';
    return;
  }

  let users = JSON.parse(localStorage.getItem('users') || '[]');
  if (!Array.isArray(users)) {
    users = [];
  }
  const user = users.find(u => u.username === username.value && u.role === role.value);

  if (user && password.value === user.password) {
    errorMsg.value = '';
    // 保存当前登录的用户名和角色
    localStorage.setItem('username', username.value);
    localStorage.setItem('role', role.value);
    // 根据角色跳转到不同的主页
    if (role.value === 'teacher') {
      router.push('/dashboard');
    } else {
      router.push('/student-dashboard');
    }
  } else {
    errorMsg.value = '用户名、密码或角色错误';
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
/* 重置一些默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* 修改背景为图片 */
.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* 替换为你的图片路径，确保路径正确 */
  background: url('src/assets/44.png') no-repeat center center fixed;
  background-size: cover; 
  z-index: -1;
}

.login-box {
  width: 500px;  /* 增大宽度 */
  background: rgba(255, 255, 255, 0.7); 
  padding: 60px 60px;  /* 增大内边距 */
  border-radius: 30px;
  box-shadow: 0 10px 30px rgba(255, 152, 0, 0.2);
  backdrop-filter: blur(10px);
  animation: fadeIn 0.5s ease-out, float 3s infinite alternate;
  position: relative;
  z-index: 1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-10px);
  }
}

.login-icon {
  text-align: center;
  margin-bottom: 24px;
}

.login-icon svg {
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.login-box h2 {
  text-align: center;
  margin-bottom: 32px;
  color: hsl(195, 100%, 50%);
  font-size: 28px;
  font-weight: 600;
  font-family: 'Comic Sans MS', cursive;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: hsl(195, 100%, 50%);
  font-size: 16px;
  font-weight: 500;
  font-family: 'Comic Sans MS', cursive;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  border: 2px solid hsl(195, 100%, 50%);
  border-radius: 20px;
  transition: border-color 0.3s;
  background: rgba(255, 255, 255, 0.7);
}

.input-wrapper:hover {
  border-color: hsl(195, 100%, 50%);
}

.input-wrapper i {
  width: 40px;
  text-align: center;
  color:hsl(195, 100%, 50%);
}

.input-wrapper input,
.input-wrapper select {
  flex: 1;
  padding: 12px 16px;
  border: none;
  outline: none;
  background: transparent;
  font-size: 16px;
  font-family: 'Comic Sans MS', cursive;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 32px;
}

.form-actions button {
  padding: 12px 32px;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'Comic Sans MS', cursive;
}

.login-btn {
  background:hsl(195, 100%, 50%);
  color: #fff;
}

.login-btn:hover {
  background: hsl(195, 100%, 50%);
  transform: translateY(-2px) scale(1.05);
}

.register-btn {
  background: #4caf50;
  color: #fff;
}

.register-btn:hover {
  background: #66bb6a;
  transform: translateY(-2px) scale(1.05);
}

.error-msg {
  color: #f44336;
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
  animation: shake 0.5s, pop 0.3s;
  font-family: 'Comic Sans MS', cursive;
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

@keyframes pop {
  0% {
    transform: scale(0);
  }
  80% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.star {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #ffeb3b;
  border-radius: 50%;
  animation: fall 5s linear infinite;
}

.star-1 {
  left: 10%;
  animation-delay: 0s;
}

.star-2 {
  left: 50%;
  animation-delay: 2s;
}

.star-3 {
  left: 90%;
  animation-delay: 4s;
}

@keyframes fall {
  from {
    top: -10px;
    opacity: 1;
  }
  to {
    top: 100%;
    opacity: 0;
  }
}
</style>