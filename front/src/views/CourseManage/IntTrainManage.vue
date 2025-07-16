<template>
  <div class="training-program-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">智能培养方案生成</h1>
      <p class="page-subtitle">输入教学科目，智能生成专业培养方案</p>
    </div>

    <!-- 输入区域 -->
    <div class="input-section">
      <div class="input-card">
        <h3>教学科目输入</h3>
        <div class="input-group">
          <label for="subject">请输入教学科目：</label>
          <input 
            v-model="subjectInput" 
            id="subject" 
            type="text" 
            placeholder="例如：计算机科学与技术、软件工程、人工智能等"
            @keyup.enter="generateProgram"
            class="subject-input"
          />
          <button 
            @click="generateProgram" 
            :disabled="!subjectInput.trim() || isLoading"
            class="generate-btn"
          >
            <span v-if="isLoading">生成中...</span>
            <span v-else>生成培养方案</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 添加过渡动画 -->
    <transition name="fade">
      <!-- 结果展示区域 -->
      <div v-if="programData" class="result-section">
        <div class="result-card">
          <h3>{{ programData.subject }} - 专业培养方案</h3>
          
          <!-- 专业介绍 -->
          <div class="info-block">
            <h4><i class="icon">📚</i>专业介绍</h4>
            <p>{{ programData.introduction }}</p>
          </div>

          <!-- 发展方向 -->
          <div class="info-block">
            <h4><i class="icon">🎯</i>发展方向</h4>
            <ul class="direction-list">
              <li v-for="direction in programData.directions" :key="direction">{{ direction }}</li>
            </ul>
          </div>

          <!-- 培养目标 -->
          <div class="info-block">
            <h4><i class="icon">🎓</i>培养目标</h4>
            <p>{{ programData.objectives }}</p>
          </div>

          <!-- 培养要求 -->
          <div class="info-block">
            <h4><i class="icon">📋</i>培养要求</h4>
            <div class="requirements-grid">
              <div v-for="requirement in programData.requirements" :key="requirement.category" class="requirement-item">
                <h5>{{ requirement.category }}</h5>
                <ul>
                  <li v-for="item in requirement.items" :key="item">{{ item }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- 课程体系 -->
          <div class="info-block">
            <h4><i class="icon">📖</i>主要课程</h4>
            <div class="courses-grid">
              <span v-for="course in programData.courses" :key="course" class="course-tag">{{ course }}</span>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- 添加过渡动画 -->
    <transition name="fade">
      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-section">
        <div class="loading-spinner"></div>
        <p>正在生成培养方案，请稍候...</p>
      </div>
    </transition>

    <!-- 添加过渡动画 -->
    <transition name="fade">
      <!-- 空状态 -->
      <div v-if="!programData && !isLoading" class="empty-state">
        <h3>开始生成您的专业培养方案</h3>
        <p>请在上方输入教学科目，系统将为您智能生成完整的专业培养方案</p>
      </div>
    </transition>
  </div>
</template>

<script>
import { generateTrainingProgram } from '@/services/api';

export default {
  name: 'IntTrainManage',
  data() {
    return {
      subjectInput: '',
      isLoading: false,
      programData: null
    }
  },
  methods: {
    async generateProgram() {
      if (!this.subjectInput.trim()) return;
      
      this.isLoading = true;
      this.programData = null;

      try {
        const data = await generateTrainingProgram(this.subjectInput);
        this.programData = data;
      } catch (error) {
        console.error('生成培养方案失败:', error);
        // 优雅地处理错误，例如显示一个提示信息
        this.programData = null; // 清空旧数据
        alert('生成失败，请检查输入或稍后重试');
      } finally {
        this.isLoading = false;
      }
    },
    // 模拟数据（实际开发时删除）
    getMockData(subject) {
      const mockData = {
        '计算机科学与技术': {
          subject: '计算机科学与技术',
          introduction: '计算机科学与技术专业是一个综合性的学科，涵盖了计算机硬件、软件、网络、算法等多个方面。本专业培养具有良好的科学素养，系统地掌握计算机科学与技术的基本理论、基本知识和基本技能的高级专门人才。',
          directions: [
            '软件开发工程师',
            '系统架构师',
            '数据库管理员',
            '网络安全工程师',
            '人工智能工程师',
            '大数据分析师'
          ],
          objectives: '培养德、智、体、美全面发展，具有良好的科学素养和人文素养，系统地掌握计算机科学与技术的基本理论、基本知识和基本技能，具有较强的实践能力和创新精神，能在科研部门、教育单位、企业、事业、技术和行政管理部门等单位从事计算机教学、科学研究和应用的计算机科学与技术学科的高级专门人才。',
          requirements: [
            {
              category: '知识要求',
              items: [
                '掌握数学、自然科学基础知识',
                '掌握计算机科学与技术的基本理论和方法',
                '掌握计算机系统分析和设计的基本方法',
                '了解计算机科学与技术的发展现状和趋势'
              ]
            },
            {
              category: '能力要求',
              items: [
                '具有运用所学知识分析和解决问题的能力',
                '具有计算机软硬件系统的设计和开发能力',
                '具有较强的实践能力和创新意识',
                '具有良好的团队合作和沟通能力'
              ]
            },
            {
              category: '素质要求',
              items: [
                '具有良好的思想道德品质和职业道德',
                '具有较强的学习能力和适应能力',
                '具有国际视野和跨文化交流能力',
                '具有健康的身心素质'
              ]
            }
          ],
          courses: [
            '高等数学', '线性代数', '概率论与数理统计', 'C语言程序设计',
            '数据结构', '计算机组成原理', '操作系统', '计算机网络',
            '数据库原理', '软件工程', '算法设计与分析', '编译原理',
            'Java程序设计', 'Web开发技术', '人工智能', '机器学习'
          ]
        }
      };
      
      // 如果有匹配的专业数据就返回，否则返回通用模板
      return mockData[subject] || {
        subject: subject,
        introduction: `${subject}是一个重要的学科领域，致力于培养具备扎实理论基础和实践能力的专业人才。本专业注重理论与实践相结合，培养学生的创新思维和解决实际问题的能力。`,
        directions: [
          '专业技术岗位',
          '管理岗位',
          '研发岗位',
          '教育岗位',
          '咨询岗位'
        ],
        objectives: `培养德、智、体、美全面发展，具备${subject}领域的基本理论、基本知识和基本技能，具有较强实践能力和创新精神的高级专门人才。`,
        requirements: [
          {
            category: '知识要求',
            items: [
              '掌握本专业的基础理论知识',
              '了解专业发展前沿和趋势',
              '具备跨学科知识结构',
              '掌握科学研究方法'
            ]
          },
          {
            category: '能力要求',
            items: [
              '具有分析和解决专业问题的能力',
              '具有实践操作和应用能力',
              '具有创新思维和创新能力',
              '具有团队协作和沟通能力'
            ]
          }
        ],
        courses: [
          '专业基础课程', '专业核心课程', '专业选修课程', '实践课程'
        ]
      };
    }
  }
};
</script>

<style scoped>
.training-program-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 60px;
  position: relative;
}

.page-title {
  font-size: 36px;
  color: #2c3e50;
  margin-bottom: 15px;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  font-size: 18px;
  color: #7f8c8d;
  margin: 0;
  letter-spacing: 0.5px;
}

.input-section {
  max-width: 900px;
  margin: 0 auto 60px;
}

.input-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.input-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.input-card h3 {
  margin-bottom: 25px;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group label {
  font-weight: 600;
  color: #555;
  font-size: 18px;
}

.subject-input {
  padding: 18px;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  font-size: 18px;
  transition: border-color 0.3s ease;
}

.subject-input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}

.generate-btn {
  padding: 18px 36px;
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.4);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result-section {
  max-width: 1200px;
  margin: 0 auto;
}

.result-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.result-card > h3 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 35px;
  text-align: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #e1e8ed;
}

.info-block {
  margin-bottom: 40px;
  background: #f9f9f9;
  padding: 25px;
  border-radius: 12px;
  border-left: 4px solid #4a90e2;
}

.info-block h4 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 18px;
  padding: 12px 0;
  border-bottom: 1px solid #e0e0e0;
}

.icon {
  font-size: 24px;
  color: #4a90e2;
}

.info-block p {
  line-height: 1.8;
  color: #555;
  margin: 0;
  font-size: 16px;
}

.direction-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.direction-list li {
  background: #f8f9fa;
  padding: 15px 20px;
  border-radius: 8px;
  border-left: 4px solid #4a90e2;
  transition: transform 0.2s ease;
}

.direction-list li:hover {
  transform: translateX(5px);
}

.requirements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 25px;
}

.requirement-item {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  border: 1px solid #e1e8ed;
  transition: transform 0.2s ease;
}

.requirement-item:hover {
  transform: translateY(-3px);
}

.requirement-item h5 {
  color: #4a90e2;
  margin-bottom: 15px;
  font-size: 18px;
}

.requirement-item ul {
  margin: 0;
  padding-left: 25px;
}

.requirement-item li {
  margin-bottom: 8px;
  color: #555;
  font-size: 16px;
}

.courses-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.course-tag {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  color: white;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  transition: transform 0.2s ease;
}

.course-tag:hover {
  transform: translateY(-2px);
}

.loading-section {
  text-align: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 6px solid #f3f3f3;
  border-top: 6px solid #4a90e2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 30px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 100px 20px;
  color: #7f8c8d;
}

.empty-state h3 {
  margin-bottom: 15px;
  color: #2c3e50;
  font-size: 24px;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .training-program-container {
    padding: 20px;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .input-card, .result-card {
    padding: 30px;
  }
  
  .direction-list {
    grid-template-columns: 1fr;
  }
  
  .requirements-grid {
    grid-template-columns: 1fr;
  }
  
  .course-tag {
    font-size: 14px;
    padding: 8px 15px;
  }
}
</style>