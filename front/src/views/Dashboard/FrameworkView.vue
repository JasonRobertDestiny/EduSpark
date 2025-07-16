<template>
  <div class="framework-view">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        返回
      </button>
      <h2>{{ frameworkTitle }}</h2>
    </div>

    <div class="content-area" v-if="framework">
      <!-- 框架信息 -->
      <div class="framework-info">
        <div class="info-item">
          <span class="label">学习主题:</span>
          <span class="value">{{ topic }}</span>
        </div>
        <div class="info-item">
          <span class="label">学习深度:</span>
          <span class="value">{{ getLevelText(level) }}</span>
        </div>
        <div class="info-item">
          <span class="label">生成时间:</span>
          <span class="value">{{ formatDate(generatedTime) }}</span>
        </div>
      </div>

      <!-- 框架内容 -->
      <div class="framework-content">
        <div class="framework-section" v-for="(section, index) in framework" :key="index">
          <h3>{{ section.title }}</h3>
          <ul>
            <li v-for="(item, itemIndex) in section.items" :key="itemIndex">
              {{ item }}
            </li>
          </ul>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="export-btn" @click="exportFramework">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7,10 12,15 17,10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          导出框架
        </button>
        <button class="share-btn" @click="shareFramework">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="18" cy="5" r="3"/>
            <circle cx="6" cy="12" r="3"/>
            <circle cx="18" cy="19" r="3"/>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
          </svg>
          分享链接
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div class="loading" v-else-if="isLoading">
      <div class="spinner"></div>
      <p>正在加载框架内容...</p>
    </div>

    <!-- 错误状态 -->
    <div class="error" v-else>
      <div class="error-icon">⚠️</div>
      <h3>框架不存在或已过期</h3>
      <p>请检查链接是否正确，或重新生成框架。</p>
      <button class="retry-btn" @click="goToFramework">重新生成框架</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FrameworkView',
  data() {
    return {
      framework: null,
      topic: '',
      level: '',
      generatedTime: null,
      isLoading: true
    }
  },
  computed: {
    frameworkTitle() {
      return this.topic ? `${this.topic} - 知识框架` : '知识框架';
    }
  },
  mounted() {
    this.loadFramework();
  },
  methods: {
    async loadFramework() {
      try {
        const frameworkId = this.$route.params.id;
        const urlParams = new URLSearchParams(this.$route.query);
        
        this.topic = urlParams.get('topic') || '';
        this.level = urlParams.get('level') || 'beginner';
        
        // 解析框架ID获取生成时间
        try {
          // 先将Base64解码，然后URL解码（与生成时相反的操作）
          const decodedId = decodeURIComponent(atob(frameworkId + '==='.slice(0, (4 - frameworkId.length % 4) % 4)));
          const parts = decodedId.split('-');
          if (parts.length >= 3) {
            this.generatedTime = new Date(parseInt(parts[parts.length - 1]));
          }
        } catch (e) {
          console.warn('无法解析框架ID:', e);
        }
        
        // 模拟加载延迟
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 重新生成框架内容（基于URL参数）
        this.framework = this.createFrameworkStructure(this.topic, this.level);
        
      } catch (error) {
        console.error('加载框架失败:', error);
        this.framework = null;
      } finally {
        this.isLoading = false;
      }
    },
    
    createFrameworkStructure(topic, level) {
      // 复用Framework.vue中的框架生成逻辑
      const frameworks = {
        '机器学习': {
          beginner: [
            {
              title: '1. 基础概念',
              items: [
                '什么是机器学习',
                '监督学习 vs 无监督学习',
                '常见算法分类',
                '数据预处理基础'
              ]
            },
            {
              title: '2. 数学基础',
              items: [
                '线性代数基础',
                '概率论与统计',
                '微积分基础',
                '优化理论入门'
              ]
            },
            {
              title: '3. 常用算法',
              items: [
                '线性回归',
                '逻辑回归',
                '决策树',
                'K-means聚类'
              ]
            },
            {
              title: '4. 实践项目',
              items: [
                '房价预测项目',
                '鸢尾花分类',
                '客户分群分析',
                '推荐系统入门'
              ]
            }
          ]
        },
        'Vue.js': {
          beginner: [
            {
              title: '1. Vue基础',
              items: [
                'Vue实例和生命周期',
                '模板语法和指令',
                '数据绑定',
                '事件处理'
              ]
            },
            {
              title: '2. 组件开发',
              items: [
                '组件基础概念',
                'Props和Events',
                '插槽(Slots)',
                '组件通信'
              ]
            },
            {
              title: '3. 路由管理',
              items: [
                'Vue Router基础',
                '路由配置',
                '导航守卫',
                '动态路由'
              ]
            },
            {
              title: '4. 状态管理',
              items: [
                'Vuex基础',
                'State和Getters',
                'Mutations和Actions',
                '模块化管理'
              ]
            }
          ]
        }
      };
      
      // 检查是否有预定义的框架
      const topicKey = Object.keys(frameworks).find(key => 
        topic.toLowerCase().includes(key.toLowerCase()) || 
        key.toLowerCase().includes(topic.toLowerCase())
      );
      
      if (topicKey && frameworks[topicKey][level]) {
        return frameworks[topicKey][level];
      }
      
      // 生成通用框架
      return [
        {
          title: '1. 基础理论',
          items: [
            `${topic}的基本概念`,
            `${topic}的发展历史`,
            `${topic}的应用领域`,
            `${topic}的核心原理`
          ]
        },
        {
          title: '2. 核心技术',
          items: [
            `${topic}的关键技术`,
            `${topic}的实现方法`,
            `${topic}的工具和框架`,
            `${topic}的最佳实践`
          ]
        },
        {
          title: '3. 实践应用',
          items: [
            `${topic}的实际案例`,
            `${topic}的项目实战`,
            `${topic}的问题解决`,
            `${topic}的性能优化`
          ]
        },
        {
          title: '4. 进阶发展',
          items: [
            `${topic}的前沿技术`,
            `${topic}的发展趋势`,
            `${topic}的深入研究`,
            `${topic}的职业发展`
          ]
        }
      ];
    },
    
    getLevelText(level) {
      const levelMap = {
        beginner: '初学者',
        intermediate: '中级',
        advanced: '高级'
      };
      return levelMap[level] || level;
    },
    
    formatDate(date) {
      if (!date || !(date instanceof Date)) return '未知';
      return date.toLocaleString('zh-CN');
    },
    
    goBack() {
      this.$router.go(-1);
    },
    
    goToFramework() {
      this.$router.push('/framework');
    },
    
    exportFramework() {
      const content = this.formatFrameworkForExport();
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${this.topic}-知识框架.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    },
    
    formatFrameworkForExport() {
      let content = `${this.topic} - 知识框架\n`;
      content += `学习深度: ${this.getLevelText(this.level)}\n\n`;
      
      this.framework.forEach((section, index) => {
        content += `${section.title}\n`;
        section.items.forEach(item => {
          content += `  • ${item}\n`;
        });
        content += '\n';
      });
      
      return content;
    },
    
    async shareFramework() {
      const url = window.location.href;
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(url);
          alert('链接已复制到剪贴板！');
        } else {
          // 降级方案
          const textArea = document.createElement('textarea');
          textArea.value = url;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);
          alert('链接已复制到剪贴板！');
        }
      } catch (error) {
        console.error('复制失败:', error);
        alert('复制失败，请手动复制链接');
      }
    }
  }
}
</script>

<style scoped>
.framework-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background: #f8f9fa;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f5f5f5;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.3s ease;
  margin-right: 20px;
}

.back-btn:hover {
  background: #e0e0e0;
  color: #333;
}

h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 28px;
  font-weight: 600;
  flex: 1;
}

.framework-info {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 25px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.value {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 600;
}

.framework-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 25px;
}

.framework-section {
  margin-bottom: 30px;
  padding: 25px;
  border-left: 4px solid #1976d2;
  background: #f8f9fa;
  border-radius: 0 8px 8px 0;
}

.framework-section:last-child {
  margin-bottom: 0;
}

.framework-section h3 {
  color: #1976d2;
  font-size: 20px;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.framework-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.framework-section li {
  padding: 8px 0;
  color: #555;
  font-size: 16px;
  position: relative;
  padding-left: 20px;
}

.framework-section li:before {
  content: '•';
  color: #1976d2;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.export-btn, .share-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn {
  background: linear-gradient(135deg, #4caf50, #66bb6a);
  color: white;
}

.export-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.share-btn {
  background: linear-gradient(135deg, #ff9800, #ffb74d);
  color: white;
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1976d2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.error h3 {
  color: #e53e3e;
  font-size: 24px;
  margin: 0 0 15px 0;
}

.error p {
  color: #666;
  font-size: 16px;
  margin: 0 0 25px 0;
  line-height: 1.5;
}

.retry-btn {
  background: linear-gradient(135deg, #1976d2, #42a5f5);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .framework-view {
    padding: 15px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .back-btn {
    margin-right: 0;
  }
  
  h2 {
    font-size: 24px;
  }
  
  .framework-info {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .export-btn, .share-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>