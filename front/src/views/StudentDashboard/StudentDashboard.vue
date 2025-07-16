<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <div class="logo">学生平台</div>
      <nav>
        <ul>
          <li v-for="item in navItems" :key="item.key" :class="{active: activeNav === item.key}" @click="selectNav(item.key)">
            <span>{{ item.label }}</span>
          </li>
        </ul>
      </nav>
    </aside>
    <div class="main-content">
      <header class="dashboard-header">
        <div class="user-info" :class="{ open: showDropdown }" @click="toggleDropdown">
          <span>欢迎您，{{ username }}</span>
          <span class="dropdown-arrow">▼</span>
          <div v-if="showDropdown" class="dropdown-menu">
            <div class="dropdown-item" @click.stop="goToProfile">个人中心</div>
            <div class="dropdown-item" @click.stop="logout">退出</div>
          </div>
        </div>
      </header>
      <section class="dashboard-body">
        <div v-if="!currentComponent" class="welcome-section">
          <div class="welcome-title">欢迎来到教学资源管理平台</div>
          <div class="image-row">
            <div class="image-wrapper">
              <img :src="imgUrl1" alt="计算机1" />
            </div>
            <div class="image-wrapper">
              <img :src="imgUrl2" alt="计算机2" />
            </div>
            <div class="image-wrapper">
              <img :src="imgUrl3" alt="计算机3" />
            </div>
          </div>
        </div>
        <component :is="currentComponent" v-if="currentComponent" />
      </section>
    </div>
  </div>
</template>

<script>
import imgUrl1 from '@/assets/11.jpg'
import imgUrl2 from '@/assets/22.jpg'
import imgUrl3 from '@/assets/33.jpg'
import AssistedQuestioning from '@/views/StudentDashboard/AssistedQuestioning.vue';
import CommunitySpace from '@/views/StudentDashboard/CommunitySpace.vue';
import StudentLearningAnalysis from '@/views/StudentDashboard/StudentLearningAnalysis.vue';


export default {
  name: "StudentDashboard",
  components: {
    AssistedQuestioning, // 直接注册，不要重复声明
    CommunitySpace,  // 新增
    StudentLearningAnalysis  // 新增
  },
  data() {
    return {
      imgUrl1,
      imgUrl2,
      imgUrl3,
      username: localStorage.getItem('username') || '同学',
      navItems: [
        { key: 'assisted-questioning', label: '智能辅助做题', component: 'AssistedQuestioning' },
        { key: 'learning-analysis', label: '个人学情分析', component: 'StudentLearningAnalysis' },
        { key: 'community-space', label: '社区空间', component: 'CommunitySpace' }
      ],
      activeNav: null,
      showDropdown: false

    }
  },
  mounted() {
    this.updateNavFromRoute(this.$route);
  },
  watch: {
    '$route'(to) {
      this.updateNavFromRoute(to);
    }
  },
  computed: {
    currentComponent() {
      const item = this.navItems.find(i => i.key === this.activeNav);
      return item ? item.component : null;
    }
  },
  methods: {
    updateNavFromRoute(route) {
      const nav = route.query.nav;
      if (nav && this.navItems.some(item => item.key === nav)) {
        this.activeNav = nav;
      } else {
        this.activeNav = null;
      }
    },
    selectNav(key) {
      if (this.$route.query.nav !== key) {
        this.$router.push({ query: { nav: key } });
      }
    },
    backToResource() {
      this.$router.push({ query: { nav: 'resource' } });
    },
    logout() {
      localStorage.removeItem('username');
      this.$router.replace('/');
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    goToProfile() {
      this.$router.push({ name: 'Profile' });
      this.showDropdown = false;
    } 
  }
}
</script>

<style scoped>
.user-info {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  color: white;
  background-color: transparent !important;
  border: none !important;
  padding: 0;
}

.dropdown-arrow {
  margin-left: 8px;
  font-size: 12px;
  transition: transform 0.2s ease-in-out;
}

.user-info.open .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  padding: 5px 0;
  z-index: 1000;
  min-width: 140px;
  border: 1px solid #e7e7e7;
}

.dropdown-item {
  padding: 10px 20px;
  cursor: pointer;
  color: #333;
  font-size: 16px;
  text-align: center;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}
.dashboard-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  background: #fff;
  z-index: 0;
}
.sidebar {
  width: 220px;
  min-width: 220px;
  max-width: 220px;
  background: linear-gradient(180deg, #1976d2 0%, #1565c0 50%, #0d47a1 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding-top: 0;
  border-radius: 0;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  position: relative;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 10;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #fff;
  height: 100vh;
  overflow: auto;
}
.dashboard-header {
  height: 60px;
  min-height: 60px;
  max-height: 60px;
  box-sizing: border-box;
  background: linear-gradient(90deg, #1976d2 0%, #1565c0 100%);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border-bottom: 1px solid rgba(255,255,255,0.2);
  z-index: 5;
  position: relative;
}
.dashboard-body {
  flex: 1;
  padding: 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
}
body, html {
  overflow-x: hidden !important;
  background: #fff;
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar nav li {
  padding: 16px 32px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
  position: relative;
  border-left: 3px solid transparent;
  display: flex;
  align-items: center;
}

.dropdown-menu {
  position: absolute;
  top: 50px;
  right: 0;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  min-width: 120px;
  white-space: nowrap;
  z-index: 100;
}

.dropdown-item {
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #333;
  text-align: center;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.sidebar nav li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 0;
  background: rgba(255, 255, 255, 0.1);
  transition: width 0.3s ease;
}

.sidebar nav li:hover::before {
  width: 100%;
}

.sidebar nav li.active, .sidebar nav li:hover {
  background: rgba(255, 255, 255, 0.15);
  border-left-color: #fff;
  transform: translateX(5px);
}

.sidebar nav li.active {
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}
.user-info {
  font-size: 16px;
  color: #fff;
  cursor: pointer;
  position: relative;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.dropdown-arrow {
  margin-left: 8px;
  font-size: 12px;
}
.logout-btn {
  color: #1976d2;
  margin-left: 12px;
  font-size: 15px;
  cursor: pointer;
}
.dashboard-body {
  flex: 1;
  padding: 32px;
  background: #f5f7fa;
}
.logo {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  padding: 16px 32px;
  height: 60px;
  letter-spacing: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin-bottom: 10px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  white-space: nowrap;
  overflow: hidden;
}
.welcome-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 120px;
  padding: 32px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  margin: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
.welcome-title {
  font-size: 40px;
  font-weight: bold;
  color: #1976d2;
  margin-bottom: 48px;
  text-align: center;
}
.image-row {
  display: flex;
  justify-content: center;
  gap: 60px;
}
.image-wrapper {
  background: none;
  border-radius: 20px;
  box-shadow: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.image-wrapper img {
  width: 220px;
  height: 280px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.3s;
}
.image-wrapper img:hover {
  transform: scale(1.08);
}
.image-wrapper:hover {
  box-shadow: 0 6px 24px rgba(25,118,210,0.18);
}
</style>