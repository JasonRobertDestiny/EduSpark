<template>
  <div class="framework-page">
    <div class="page-header">
      <h2>知识框架生成</h2>
    </div>
    
    <div class="content-area">
      <!-- 输入区域 -->
      <div class="input-section">
        <div class="input-group">
          <label for="knowledge-topic">请输入您想要学习的知识领域：</label>
          <input 
            id="knowledge-topic"
            v-model="knowledgeTopic" 
            type="text" 
            placeholder="例如：机器学习、Vue.js、数据结构与算法等"
            class="topic-input"
            @keyup.enter="generateFramework"
          />
        </div>
        
        <div class="input-group">
          <label for="learning-level">学习深度：</label>
          <select id="learning-level" v-model="learningLevel" class="level-select">
            <option value="beginner">初学者</option>
            <option value="intermediate">中级</option>
            <option value="advanced">高级</option>
          </select>
        </div>
        
        <button 
          @click="generateFramework" 
          :disabled="!knowledgeTopic.trim() || isGenerating"
          class="generate-btn"
        >
          <span v-if="isGenerating">生成中...</span>
          <span v-else>生成知识框架</span>
        </button>
      </div>
      
      <!-- 结果展示区域 -->
      <div v-if="framework" class="result-section">
        <h3>{{ knowledgeTopic }} - 知识框架</h3>
        
        <!-- 框架URL显示 -->
        <div v-if="frameworkUrl" class="url-section">
          <label>框架分享链接：</label>
          <div class="url-container">
            <input 
              :value="frameworkUrl" 
              readonly 
              class="url-input"
              @click="selectUrl"
            />
            <button @click="copyUrl" class="copy-btn">复制链接</button>
          </div>
        </div>
        
        <div class="framework-content">
          <div v-for="(section, index) in framework" :key="index" class="framework-section">
            <h4>{{ section.title }}</h4>
            <ul>
              <li v-for="(item, itemIndex) in section.items" :key="itemIndex">
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
        
        <div class="action-buttons">
          <button @click="exportFramework" class="export-btn">导出框架</button>
          <button @click="clearFramework" class="clear-btn">清空结果</button>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-if="!framework && !isGenerating" class="empty-state">
        <div class="empty-icon">📚</div>
        <p>输入您感兴趣的知识领域，AI将为您生成完整的学习框架</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Framework',
  data() {
    return {
      knowledgeTopic: '',
      learningLevel: 'beginner',
      framework: null,
      isGenerating: false,
      frameworkUrl: ''
    }
  },
  methods: {
    goBack() {
      // 跳转到dashboard并设置activeNav为resource
      this.$router.push('/dashboard?nav=resource');
    },
    
    async generateFramework() {
      if (!this.knowledgeTopic.trim()) return;
      
      this.isGenerating = true;
      
      try {
        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 根据不同主题生成不同的框架结构
        this.framework = this.createFrameworkStructure(this.knowledgeTopic, this.learningLevel);
        
        // 生成框架URL
        this.frameworkUrl = this.generateFrameworkUrl();
        console.log('生成的框架URL:', this.frameworkUrl);
        
        return this.frameworkUrl;
      } catch (error) {
        console.error('生成框架失败:', error);
        alert('生成框架失败，请重试');
      } finally {
        this.isGenerating = false;
      }
    },
    
    createFrameworkStructure(topic, level) {
      // 这里可以根据不同的主题和级别生成不同的框架
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
          ],
          intermediate: [
            {
              title: '1. 进阶算法',
              items: [
                '支持向量机(SVM)',
                '随机森林',
                '神经网络基础',
                '集成学习方法'
              ]
            },
            {
              title: '2. 深度学习',
              items: [
                '卷积神经网络(CNN)',
                '循环神经网络(RNN)',
                'LSTM和GRU',
                '迁移学习'
              ]
            },
            {
              title: '3. 模型优化',
              items: [
                '超参数调优',
                '交叉验证',
                '正则化技术',
                '模型评估指标'
              ]
            },
            {
              title: '4. 工程实践',
              items: [
                'MLOps基础',
                '模型部署',
                'A/B测试',
                '监控与维护'
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
    
    exportFramework() {
      const content = this.formatFrameworkForExport();
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${this.knowledgeTopic}-知识框架.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    },
    
    formatFrameworkForExport() {
      let content = `${this.knowledgeTopic} - 知识框架\n`;
      content += `学习深度: ${this.getLevelText(this.learningLevel)}\n\n`;
      
      this.framework.forEach((section, index) => {
        content += `${section.title}\n`;
        section.items.forEach(item => {
          content += `  • ${item}\n`;
        });
        content += '\n';
      });
      
      return content;
    },
    
    getLevelText(level) {
      const levelMap = {
        beginner: '初学者',
        intermediate: '中级',
        advanced: '高级'
      };
      return levelMap[level] || level;
    },
    
    clearFramework() {
      this.framework = null;
      this.knowledgeTopic = '';
      this.frameworkUrl = '';
    },
    
    selectUrl(event) {
      event.target.select();
    },
    
    async copyUrl() {
      try {
        await navigator.clipboard.writeText(this.frameworkUrl);
        alert('链接已复制到剪贴板！');
      } catch (err) {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = this.frameworkUrl;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        alert('链接已复制到剪贴板！');
      }
    },
    
    generateFrameworkUrl() {
      // 生成基于当前框架的URL
      const baseUrl = window.location.origin;
      const encodedTopic = encodeURIComponent(this.knowledgeTopic);
      const encodedLevel = encodeURIComponent(this.learningLevel);
      
      // 生成唯一的框架ID（基于主题和时间戳）
      // 使用encodeURIComponent处理中文字符，然后转换为Base64安全的字符串
      const rawId = `${this.knowledgeTopic}-${this.learningLevel}-${Date.now()}`;
      const frameworkId = btoa(encodeURIComponent(rawId)).replace(/[+/=]/g, '');
      
      // 构建完整的框架URL
      const frameworkUrl = `${baseUrl}/framework/${frameworkId}?topic=${encodedTopic}&level=${encodedLevel}`;
      
      return frameworkUrl;
    }
  }
}
</script>

<style scoped>
.framework-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background: #f8f9fa;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 28px;
  font-weight: 600;
}

.content-area {
  display: grid;
  gap: 30px;
}

/* 输入区域样式 */
.input-section {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
  font-size: 16px;
}

.topic-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.topic-input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}

.level-select {
  padding: 12px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.level-select:focus {
  outline: none;
  border-color: #1976d2;
}

.generate-btn {
  background: linear-gradient(135deg, #1976d2, #42a5f5);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
}

.generate-btn:disabled {
  background: #bbb;
  cursor: not-allowed;
  transform: none;
}

/* 结果展示区域样式 */
.result-section {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.result-section h3 {
  color: #1976d2;
  font-size: 24px;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 3px solid #e3f2fd;
}

/* URL显示区域样式 */
.url-section {
  margin-bottom: 25px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e1e8ed;
}

.url-section label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #2c3e50;
  font-size: 14px;
}

.url-container {
  display: flex;
  gap: 10px;
  align-items: center;
}

.url-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  font-size: 14px;
  color: #555;
  cursor: pointer;
}

.url-input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.copy-btn {
  background: #1976d2;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.copy-btn:hover {
  background: #1560a8;
  transform: translateY(-1px);
}

.framework-content {
  margin-bottom: 30px;
}

.framework-section {
  margin-bottom: 25px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #1976d2;
}

.framework-section h4 {
  color: #2c3e50;
  font-size: 18px;
  margin-bottom: 15px;
  font-weight: 600;
}

.framework-section ul {
  margin: 0;
  padding-left: 20px;
}

.framework-section li {
  margin-bottom: 8px;
  color: #555;
  line-height: 1.6;
  font-size: 15px;
}

.framework-section li:hover {
  color: #1976d2;
  transition: color 0.2s ease;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid #e1e8ed;
}

.export-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background: #45a049;
  transform: translateY(-1px);
}

.clear-btn {
  background: #f44336;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  background: #da190b;
  transform: translateY(-1px);
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state p {
  color: #666;
  font-size: 18px;
  margin: 0;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .framework-page {
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
  
  .input-section,
  .result-section {
    padding: 20px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .topic-input {
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  .url-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .copy-btn {
    margin-top: 10px;
  }
}
</style>