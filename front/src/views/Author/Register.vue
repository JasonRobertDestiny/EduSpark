<template>
  <div class="register-container">
    <div class="register-box">
      <h2>计算机教学辅导平台注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group-inline">
          <label for="username">用户名</label>
          <input v-model="username" id="username" type="text" placeholder="请输入用户名" required />
        </div>
        <div class="form-group-inline">
          <label for="password">密码</label>
          <input v-model="password" id="password" type="password" placeholder="请输入密码" required />
        </div>
        <div class="form-group-inline">
          <label for="confirmPassword">确认密码</label>
          <input v-model="confirmPassword" id="confirmPassword" type="password" placeholder="请再次输入密码" required />
        </div>
        <div class="form-group-inline">
          <label for="role">角色</label>
          <select v-model="role" id="role" required>
            <option value="teacher">老师</option>
            <option value="student">学生</option>
          </select>
        </div>
        <div class="form-actions">
          <button type="submit">注册</button>
          <button type="button" @click="goToLogin">返回登录</button>
        </div>
        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
        <div v-if="successMsg" class="success-msg">{{ successMsg }}</div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      role: 'teacher', // 默认角色为老师
      errorMsg: '',
      successMsg: ''
    }
  },
  methods: {
    handleRegister() {
      if (!this.username || !this.password || !this.confirmPassword) {
        this.errorMsg = '请填写所有字段';
        this.successMsg = '';
        return;
      }
      if (this.password !== this.confirmPassword) {
        this.errorMsg = '两次输入的密码不一致';
        this.successMsg = '';
        return;
      }

      // 获取或初始化用户列表
      let users = JSON.parse(localStorage.getItem('users') || '[]');
      if (!Array.isArray(users)) {
        users = [];
      }

      // 检查用户名是否已存在
      if (users.find(user => user.username === this.username)) {
        this.errorMsg = '用户名已存在';
        this.successMsg = '';
        return;
      }

      // 添加新用户
      users.push({ username: this.username, password: this.password, role: this.role });

      // 保存更新后的用户列表到localStorage
      localStorage.setItem('users', JSON.stringify(users));
      console.log('用户已注册:', this.username, '当前所有用户:', users);

      this.errorMsg = '';
      this.successMsg = '注册成功！';

      // 可选：注册成功后自动跳转到登录页
      setTimeout(() => {
        this.$router.push('/');
      }, 1000);
    },
    goToLogin() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fa;
}
.register-box {
  background: #fff;
  padding: 40px 32px;
  border-radius: 10px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  width: 480px;
}
.register-box h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #333;
}
.form-group-inline {
  display: flex;
  align-items: center;
  margin-bottom: 28px;
}
.form-group-inline label {
  width: 100px;
  margin-right: 10px;
  color: #666;
  text-align: center;
  font-size: 16px;
}
.form-group-inline input,
.form-group-inline select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
}
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}
.form-actions button {
  padding: 8px 32px;
  border: none;
  border-radius: 4px;
  background: #67c23a;
  color: #fff;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.2s;
}
.form-actions button[type="button"] {
  background: #409eff;
}
.form-actions button:hover {
  opacity: 0.9;
}
.error-msg {
  color: #f56c6c;
  margin-top: 12px;
  text-align: center;
}
.success-msg {
  color: #67c23a;
  margin-top: 12px;
  text-align: center;
}
</style>