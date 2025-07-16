<template>
  <div class="course-manage-container">
    <!-- 功能模块网格 -->
    <div class="modules-grid">
      <!-- 教材资源 -->
      <div class="module-card" @click="goTo('TeachingMaterial')">
        <div class="module-header">
          <div class="module-icon textbook-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H6.5A2.5 2.5 0 0 0 4 4.5v15Z" stroke="currentColor" stroke-width="2"/>
              <path d="M9 9h6M9 13h6M9 17h3" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <h3 class="module-title">教材资源，重难点详解</h3>
        </div>
        <div class="module-content">
          <p class="module-description">管理课程教材、参考书籍和学习资料，提供丰富的教学资源支持</p>
          <div class="module-features">
            <span class="feature-tag">教材管理</span>
            <span class="feature-tag">资源库</span>
            <span class="feature-tag">在线阅读</span>
          </div>
        </div>
      </div>

      <!-- 教学大纲 -->
      <div class="module-card" @click="goTo('Syllabus')">
        <div class="module-header">
          <div class="module-icon syllabus-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2"/>
              <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2"/>
              <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2"/>
              <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <h3 class="module-title">教学大纲（框架）</h3>
        </div>
        <div class="module-content">
          <p class="module-description">制定和管理课程教学大纲，规划教学进度和内容安排</p>
          <div class="module-features">
            <span class="feature-tag">大纲制定</span>
            <span class="feature-tag">进度规划</span>
            <span class="feature-tag">内容管理</span>
          </div>
        </div>
      </div>

      <!-- 重难点详解 -->
      <div class="module-card" @click="goTo('IntTrainManage')">
        <div class="module-header">
          <div class="module-icon keypoints-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" stroke="currentColor" stroke-width="2"/>
              <path d="M12 17h.01" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <h3 class="module-title">智能培养方案</h3>
        </div>
        <div class="module-content">
          <p class="module-description">深入分析课程重点难点，提供详细解析和教学指导</p>
          <div class="module-features">
            <span class="feature-tag">重点分析</span>
            <span class="feature-tag">难点突破</span>
            <span class="feature-tag">教学指导</span>
          </div>
        </div>
      </div>

      <!-- 学情分析 -->
      <div class="module-card" @click="goTo('TeacherLearningAnalysis')">
        <div class="module-header">
          <div class="module-icon analysis-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 3v18h18" stroke="currentColor" stroke-width="2"/>
              <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <h3 class="module-title">学情分析</h3>
        </div>
        <div class="module-content">
          <p class="module-description">全面分析学生学习情况，提供数据驱动的教学决策支持</p>
          <div class="module-features">
            <span class="feature-tag">学习分析</span>
            <span class="feature-tag">数据统计</span>
            <span class="feature-tag">效果评估</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "IntCourseManage",
  methods: {
    goTo(routeName) {
      this.$router.push({ name: routeName });
    }
  }
}
</script>

<style scoped>
.course-manage-container {
  padding: 40px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.module-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.module-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.module-card:hover::before {
  transform: scaleX(1);
}

.module-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.module-icon {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  color: white;
}

.module-icon svg {
  width: 30px;
  height: 30px;
}

.textbook-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.syllabus-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.keypoints-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.analysis-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.module-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
}

.module-content {
  margin-left: 80px;
}

.module-description {
  margin: 0 0 20px 0;
  font-size: 16px;
  color: #7f8c8d;
  line-height: 1.6;
}

.module-features {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.feature-tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .course-manage-container {
    padding: 20px;
  }
  
  .modules-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .module-card {
    padding: 20px;
  }
  
  .module-header {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }
  
  .module-icon {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .module-content {
    margin-left: 0;
  }
  
  .module-title {
    font-size: 20px;
  }
}
</style>