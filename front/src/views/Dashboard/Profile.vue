<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <h2>个人中心</h2>
      </div>

      <div class="profile-body">
        <!-- Avatar Section -->
        <div class="avatar-section">
          <img :src="user.avatar" alt="User Avatar" class="avatar-image">
          <label for="avatar-upload" class="avatar-upload-label">更换头像</label>
          <input type="file" id="avatar-upload" @change="handleAvatarChange" accept="image/*">
        </div>

        <!-- Form Section -->
        <div class="form-section">
          <div class="tabs">
            <button :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">基本信息</button>
            <button :class="{ active: activeTab === 'password' }" @click="activeTab = 'password'">修改密码</button>
          </div>

          <!-- Basic Info Form -->
          <div v-if="activeTab === 'info'" class="tab-content">
            <div class="form-group">
              <label for="username">用户名</label>
              <input type="text" id="username" v-model="user.username">
            </div>
            <div class="form-group">
              <label for="email">邮箱</label>
              <input type="email" id="email" v-model="user.email">
            </div>
            <div class="form-group">
              <label for="phone">电话号码</label>
              <input type="tel" id="phone" v-model="user.phone">
            </div>
            <div class="form-group">
              <label for="bio">个人简介</label>
              <textarea id="bio" v-model="user.bio" rows="3"></textarea>
            </div>
            <button class="save-btn" @click="saveProfile">保存更改</button>
          </div>

          <!-- Change Password Form -->
          <div v-if="activeTab === 'password'" class="tab-content">
            <div class="form-group">
              <label for="current-password">当前密码</label>
              <input type="password" id="current-password" v-model="password.current">
            </div>
            <div class="form-group">
              <label for="new-password">新密码</label>
              <input type="password" id="new-password" v-model="password.new">
            </div>
            <div class="form-group">
              <label for="confirm-password">确认新密码</label>
              <input type="password" id="confirm-password" v-model="password.confirm">
            </div>
            <button class="save-btn" @click="changePassword">确认修改</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  data() {
    return {
      activeTab: 'info',
      user: {
        username: '',
        email: '',
        phone: '',
        bio: '',
        avatar: 'https://i.pravatar.cc/150?img=32' // Placeholder avatar
      },
      password: {
        current: '',
        new: '',
        confirm: ''
      }
    };
  },
  created() {
    this.loadUserProfile();
  },
  methods: {
    loadUserProfile() {
      // Load user data from localStorage
      this.user.username = localStorage.getItem('username') || '教师';
      const userProfileKey = `userProfile_${this.user.username}`;
      const savedUser = localStorage.getItem(userProfileKey);
      if (savedUser) {
        const userProfile = JSON.parse(savedUser);
        this.user.email = userProfile.email || '';
        this.user.phone = userProfile.phone || '';
        this.user.bio = userProfile.bio || '';
        this.user.avatar = userProfile.avatar || 'https://i.pravatar.cc/150?img=32';
      } else {
        // Initialize if no data is saved
        this.user.email = '';
        this.user.phone = '';
        this.user.bio = '';
      }
    },
    saveProfile() {
      // Save user info to localStorage
      const userProfileKey = `userProfile_${this.user.username}`;
      const profileToSave = {
        email: this.user.email,
        phone: this.user.phone,
        bio: this.user.bio,
        avatar: this.user.avatar
      };
      localStorage.setItem(userProfileKey, JSON.stringify(profileToSave));
      console.log('Saving profile for user:', this.user.username);
      alert('个人信息已更新！');
    },
    changePassword() {
      if (this.password.new !== this.password.confirm) {
        alert('新密码和确认密码不匹配！');
        return;
      }
      if (!this.password.new || this.password.new.length < 6) {
        alert('新密码长度不能少于6位！');
        return;
      }

      const username = localStorage.getItem('username');
      if (!username) {
        alert('用户未登录，无法修改密码。');
        return;
      }

      let users = JSON.parse(localStorage.getItem('users') || '[]');
      if (!Array.isArray(users)) {
          users = [];
      }
      const userIndex = users.findIndex(u => u.username === username);

      if (userIndex === -1 || users[userIndex].password !== this.password.current) {
        alert('当前密码不正确！');
        return;
      }

      // 更新密码
      users[userIndex].password = this.password.new;
      localStorage.setItem('users', JSON.stringify(users));

      console.log('Password changed for user:', username);
      alert('密码已成功修改！');
      this.password = { current: '', new: '', confirm: '' };
    },
    handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.user.avatar = e.target.result;
          // You would typically upload the file to a server here
          console.log('Avatar updated.');
        };
        reader.readAsDataURL(file);
      }
    }
  }
};
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
}

.profile-card {
  width: 100%;
  max-width: 100%;
  background: #fff;
  border-radius: 0;
  box-shadow: none;
  overflow: hidden;
}

.profile-header {
  background-color: #4a90e2;
  color: white;
  padding: 25px 30px;
  text-align: center;
}

.profile-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
}

.profile-header p {
  margin: 5px 0 0;
  font-size: 16px;
  opacity: 0.9;
}

.profile-body {
  display: flex;
  padding: 30px;
  justify-content: center;
  align-items: center;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 30px;
}

.avatar-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.avatar-upload-label {
  background-color: #f0f2f5;
  color: #4a90e2;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: background-color 0.3s, color 0.3s;
}

.avatar-upload-label:hover {
  background-color: #e4e6eb;
}

#avatar-upload {
  display: none;
}

.form-section {
  flex: 1;
  max-width: 500px; /* Or your desired original width */
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #666;
  position: relative;
  transition: color 0.3s;
}

.tabs button.active {
  color: #4a90e2;
}

.tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #4a90e2;
  border-radius: 3px 3px 0 0;
}

.tab-content {
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}

.save-btn {
  width: 100%;
  background-color: #4a90e2;
  color: white;
  padding: 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  transition: background-color 0.3s, transform 0.2s;
}

.save-btn:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.save-btn:active {
  transform: translateY(0);
}
</style>