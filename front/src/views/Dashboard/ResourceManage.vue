<template>
  <div class="resource-tools-section">
    <div class="tool-grid">
      <div v-for="tool in resourceTools" :key="tool.key" class="tool-card" @click="handleToolClick(tool)">
        <div class="tool-icon">{{ tool.icon }}</div>
        <div class="tool-title">{{ tool.title }}</div>
        <div class="tool-description">{{ tool.description }}</div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ResourceManage',
  data() {
    return {
      resourceTools: [ 
        { key: 'PPT', title: 'PPT生成', icon: '📊', description: '智能生成精美演示文稿' },
        { key: 'Homework', title: '智能作业生成', icon: '📝', description: '自动创建个性化作业题目' },
        { key: 'Exam', title: '智能试卷生成', icon: '📋', description: '快速生成标准化考试试卷' },
        { key: 'QA', title: '多模态问答', icon: '🤖', description: '支持文字图片语音交互' }
      ]
    }
  },
  methods: {
    handleToolClick(tool) {
      // 通知父组件切换到对应的功能页面
      this.$router.push({ name: tool.key });
    }
  }
}
</script>

<style scoped>



.resource-tools-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0f6ff 0%, #e6f2ff 100%);
}
.tool-grid {
  display: grid;
  grid-template-columns: repeat(2, 350px);
  grid-gap: 60px;
  max-width: 1000px;
}
.tool-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #4a90e2;
  user-select: none;
  position: relative;
  overflow: hidden;
}

.tool-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(74, 144, 226, 0.1), transparent);
  transition: left 0.6s ease;
}

.tool-card:hover::before {
  left: 100%;
}

.tool-card:hover {
  transform: translateY(-10px) scale(1.03);
  box-shadow: 0 20px 40px rgba(74, 144, 226, 0.15);
  border-color: rgba(74, 144, 226, 0.3);
  background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
}

.tool-card:active {
  transform: translateY(-5px) scale(1.01);
}

.tool-icon {
  font-size: 48px;
  margin-bottom: 15px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  transition: transform 0.3s ease;
}

.tool-card:hover .tool-icon {
  transform: scale(1.1) rotate(5deg);
}

.tool-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
  transition: color 0.3s ease;
  text-align: center;
  line-height: 1.4;
  margin: 0;
}

.tool-card:hover .tool-title {
  color: #4a90e2;
}

.tool-description {
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.4;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.tool-card:hover .tool-description {
  opacity: 1;
  color: #5a6c7d;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .tool-grid {
    grid-template-columns: repeat(2, 280px);
    grid-gap: 40px;
  }
}

@media (max-width: 768px) {
  .resource-tools-section {
    padding: 20px 15px;
  }
  .tool-grid {
    grid-template-columns: 1fr;
    grid-gap: 30px;
    max-width: 320px;
  }
  .tool-card {
    height: 180px;
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .tool-card {
    height: 160px;
    font-size: 18px;
  }
  .tool-grid {
    max-width: 280px;
  }
}
</style>