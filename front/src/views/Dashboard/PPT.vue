<template>
  <div class="ppt-page">
    <div class="page-header">
      <h2>智能PPT生成</h2>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 输入表单区域 -->
      <div class="input-section" v-if="!isGenerating && !generatedPPT">
        <div class="form-container">
          <h3>📝 PPT信息输入</h3>
          
          <!-- 基本信息 -->
          <div class="form-group">
            <label>PPT主题 *</label>
            <input 
              v-model="pptConfig.title" 
              type="text" 
              placeholder="请输入PPT的主题，如：人工智能发展趋势"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label>目标受众</label>
            <select v-model="pptConfig.audience" class="form-select">
              <option value="">请选择目标受众</option>
              <option value="students">学生群体</option>
              <option value="professionals">专业人士</option>
              <option value="general">普通大众</option>
              <option value="executives">企业高管</option>
              <option value="technical">技术人员</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>演示时长</label>
            <select v-model="pptConfig.duration" class="form-select">
              <option value="">请选择演示时长</option>
              <option value="5">5分钟</option>
              <option value="10">10分钟</option>
              <option value="15">15分钟</option>
              <option value="20">20分钟</option>
              <option value="30">30分钟</option>
              <option value="45">45分钟</option>
              <option value="60">60分钟</option>
            </select>
          </div>
          
          <!-- 内容描述 -->
          <div class="form-group">
            <label>内容描述 *</label>
            <textarea 
              v-model="pptConfig.description" 
              placeholder="请详细描述PPT的内容要点、结构安排等...\n例如：\n1. 介绍人工智能的定义和发展历程\n2. 分析当前AI技术的应用领域\n3. 探讨未来发展趋势和挑战\n4. 总结和展望"
              class="form-textarea"
              rows="6"
            ></textarea>
          </div>
          
          <!-- 风格设置 -->
          <div class="form-group">
            <label>PPT风格</label>
            <div class="style-options">
              <div 
                v-for="style in styleOptions" 
                :key="style.value"
                :class="['style-option', { active: pptConfig.style === style.value }]"
                @click="pptConfig.style = style.value"
              >
                <div class="style-preview" :style="{ background: style.color }"></div>
                <span>{{ style.name }}</span>
              </div>
            </div>
          </div>
          
          <!-- 页数设置 -->
          <div class="form-group">
            <label>预期页数</label>
            <div class="slider-container">
              <input 
                v-model="pptConfig.slideCount" 
                type="range" 
                min="5" 
                max="50" 
                class="slider"
              />
              <span class="slider-value">{{ pptConfig.slideCount }} 页</span>
            </div>
          </div>
          
          <!-- 高级选项 -->
          <div class="form-group">
            <label>高级选项</label>
            <div class="checkbox-group">
              <label class="checkbox-item">
                <input v-model="pptConfig.includeImages" type="checkbox" />
                <span>包含图片和图表</span>
              </label>
              <label class="checkbox-item">
                <input v-model="pptConfig.includeAnimations" type="checkbox" />
                <span>添加动画效果</span>
              </label>
              <label class="checkbox-item">
                <input v-model="pptConfig.includeNotes" type="checkbox" />
                <span>生成演讲者备注</span>
              </label>
            </div>
          </div>
          
          <!-- AI模型选择 -->
          <div class="form-group">
            <label>AI生成模型</label>
            <select v-model="pptConfig.aiModel" class="form-select">
              <option value="gpt4">GPT-4 (推荐)</option>
              <option value="claude">Claude-3</option>
              <option value="gemini">Gemini Pro</option>
              <option value="local">本地模型</option>
            </select>
            <p class="model-description">{{ getModelDescription() }}</p>
          </div>
          
          <!-- 生成按钮 -->
          <div class="action-buttons">
            <button 
              @click="generatePPT" 
              :disabled="!canGenerate"
              class="generate-btn"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
              开始生成PPT
            </button>
            <button @click="resetForm" class="reset-btn">重置表单</button>
          </div>
        </div>
      </div>
      
      <!-- 生成进度区域 -->
      <div class="generating-section" v-if="isGenerating">
        <div class="progress-container">
          <div class="progress-header">
            <h3>🚀 正在生成您的PPT...</h3>
            <p>{{ currentStep }}</p>
          </div>
          
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <span class="progress-text">{{ progress }}%</span>
          
          <div class="progress-steps">
            <div v-for="(step, index) in generationSteps" :key="index" 
                 :class="['step', { completed: index < currentStepIndex, active: index === currentStepIndex }]">
              <div class="step-icon">
                <svg v-if="index < currentStepIndex" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20,6 9,17 4,12"/>
                </svg>
                <span v-else>{{ index + 1 }}</span>
              </div>
              <span>{{ step }}</span>
            </div>
          </div>
          
          <button @click="cancelGeneration" class="cancel-btn">取消生成</button>
        </div>
      </div>
      
      <!-- PPT预览和操作区域 -->
      <div class="result-section" v-if="generatedPPT">
        <div class="result-header">
          <h3>✅ PPT生成完成</h3>
          <div class="result-actions">
            <button @click="previewPPT" class="preview-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              预览PPT
            </button>
            <button @click="downloadPPT" class="download-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7,10 12,15 17,10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              下载PPT
            </button>
            <button @click="editPPT" class="edit-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              编辑PPT
            </button>
            <button @click="shareePPT" class="share-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="18" cy="5" r="3"/>
                <circle cx="6" cy="12" r="3"/>
                <circle cx="18" cy="19" r="3"/>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
              </svg>
              分享PPT
            </button>
            <button @click="startNew" class="new-btn">生成新PPT</button>
          </div>
        </div>
        
        <!-- PPT信息卡片 -->
        <div class="ppt-info-card">
          <div class="ppt-thumbnail">
            <div class="thumbnail-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <line x1="9" y1="9" x2="15" y2="9"/>
                <line x1="9" y1="12" x2="15" y2="12"/>
                <line x1="9" y1="15" x2="13" y2="15"/>
              </svg>
            </div>
          </div>
          <div class="ppt-details">
            <h4>{{ generatedPPT.title }}</h4>
            <div class="ppt-meta">
              <span><strong>页数：</strong>{{ generatedPPT.slideCount }} 页</span>
              <span><strong>风格：</strong>{{ getStyleName(generatedPPT.style) }}</span>
              <span><strong>生成时间：</strong>{{ formatTime(generatedPPT.createdAt) }}</span>
              <span><strong>文件大小：</strong>{{ generatedPPT.fileSize }}</span>
            </div>
            <div class="ppt-description">{{ generatedPPT.description }}</div>
          </div>
        </div>
        
        <!-- 幻灯片预览 -->
        <div class="slides-preview">
          <h4>幻灯片预览</h4>
          <div class="slides-grid">
            <div v-for="(slide, index) in generatedPPT.slides" :key="index" 
                 class="slide-item" @click="selectSlide(index)">
              <div class="slide-number">{{ index + 1 }}</div>
              <div class="slide-content">
                <h5>{{ slide.title }}</h5>
                <p>{{ slide.content.substring(0, 50) }}...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { generatePPT } from '@/services/api';
export default {
  name: 'PPT',
  data() {
    return {
      // PPT配置
      pptConfig: {
        title: '',
        audience: '',
        duration: '',
        description: '',
        style: 'professional',
        slideCount: 15,
        includeImages: true,
        includeAnimations: false,
        includeNotes: true,
        aiModel: 'gpt4'
      },
      
      // 风格选项
      styleOptions: [
        { value: 'professional', name: '商务专业', color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
        { value: 'creative', name: '创意活泼', color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
        { value: 'minimal', name: '简约清新', color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
        { value: 'academic', name: '学术严谨', color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' },
        { value: 'tech', name: '科技未来', color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' }
      ],
      
      // 生成状态
      isGenerating: false,
      progress: 0,
      currentStep: '',
      currentStepIndex: 0,
      generationSteps: [
        '分析内容需求',
        '生成PPT结构',
        '创建幻灯片内容',
        '应用设计风格',
        '优化布局效果',
        '生成最终文件'
      ],
      
      // 生成结果
      generatedPPT: null,
      
      // 生成定时器
      generationTimer: null
    }
  },
  
  computed: {
    canGenerate() {
      return this.pptConfig.title.trim() && this.pptConfig.description.trim();
    }
  },
  
  methods: {

    
    getModelDescription() {
      const descriptions = {
        'gpt4': '最先进的AI模型，生成质量最高，适合重要演示',
        'claude': '擅长逻辑分析，适合学术和技术类PPT',
        'gemini': '多模态能力强，适合包含图表的PPT',
        'local': '本地部署模型，数据安全，响应较快'
      };
      return descriptions[this.pptConfig.aiModel] || '';
    },
    
    getStyleName(styleValue) {
      const style = this.styleOptions.find(s => s.value === styleValue);
      return style ? style.name : styleValue;
    },
    
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleString('zh-CN');
    },
    
    resetForm() {
      this.pptConfig = {
        title: '',
        audience: '',
        duration: '',
        description: '',
        style: 'professional',
        slideCount: 15,
        includeImages: true,
        includeAnimations: false,
        includeNotes: true,
        aiModel: 'gpt4'
      };
    },
    
    async generatePPT() {
      if (!this.canGenerate) {
        alert('请填写必填项：PPT主题和内容描述');
        return;
      }
      this.isGenerating = true;
      this.progress = 0;
      this.currentStepIndex = 0;
      this.currentStep = '正在提交生成请求...';
      try {
        // 调用后端API生成PPT
        const result = await generatePPT(this.pptConfig);
        this.generatedPPT = result;
        this.isGenerating = false;
        this.progress = 100;
        this.currentStepIndex = this.generationSteps.length;
      } catch (error) {
        console.error('PPT生成失败:', error);
        alert('PPT生成失败，请稍后重试');
        this.isGenerating = false;
      }
    },
    
    async simulateStep(duration, stepIndex) {
      return new Promise(resolve => {
        const startProgress = (stepIndex / this.generationSteps.length) * 100;
        const endProgress = ((stepIndex + 1) / this.generationSteps.length) * 100;
        const startTime = Date.now();
        
        const updateProgress = () => {
          const elapsed = Date.now() - startTime;
          const stepProgress = Math.min(elapsed / duration, 1);
          this.progress = startProgress + (endProgress - startProgress) * stepProgress;
          
          if (stepProgress < 1) {
            requestAnimationFrame(updateProgress);
          } else {
            resolve();
          }
        };
        
        updateProgress();
      });
    },
    
    generateSlides() {
      // 模拟生成幻灯片内容
      const slides = [];
      const slideCount = parseInt(this.pptConfig.slideCount);
      
      for (let i = 0; i < slideCount; i++) {
        slides.push({
          id: i + 1,
          title: `幻灯片 ${i + 1}`,
          content: `这是第 ${i + 1} 张幻灯片的内容，基于您的主题"${this.pptConfig.title}"生成。内容将根据您的描述和选择的风格进行定制。`,
          type: i === 0 ? 'title' : i === slideCount - 1 ? 'conclusion' : 'content'
        });
      }
      
      return slides;
    },
    
    cancelGeneration() {
      this.isGenerating = false;
      this.progress = 0;
      this.currentStepIndex = 0;
      if (this.generationTimer) {
        clearTimeout(this.generationTimer);
      }
    },
    
    previewPPT() {
      // 这里可以打开PPT预览窗口或跳转到预览页面
      alert('PPT预览功能开发中...');
    },
    
    downloadPPT() {
      // 模拟下载PPT文件
      const link = document.createElement('a');
      link.href = '#';
      link.download = `${this.generatedPPT.title}.pptx`;
      link.click();
      alert('PPT下载功能开发中...');
    },
    
    editPPT() {
      // 跳转到PPT编辑器
      alert('PPT编辑功能开发中...');
    },
    
    sharePPT() {
      // 分享PPT
      const shareUrl = `${window.location.origin}/ppt/share/${Date.now()}`;
      navigator.clipboard.writeText(shareUrl).then(() => {
        alert('分享链接已复制到剪贴板！');
      }).catch(() => {
        alert('分享链接：' + shareUrl);
      });
    },
    
    startNew() {
      this.generatedPPT = null;
      this.resetForm();
    },
    
    selectSlide(index) {
      // 选择幻灯片进行详细查看
      console.log('选择幻灯片:', index);
    }
  },
  
  beforeDestroy() {
    if (this.generationTimer) {
      clearTimeout(this.generationTimer);
    }
  }
}
</script>

<style scoped>
/* 页面基础样式 */
.ppt-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background: #f8fafc;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}



h2 {
  margin: 0;
  color: #1a202c;
  font-size: 28px;
  font-weight: 600;
}

/* 主要内容区域 */
.main-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  overflow: hidden;
}

/* 输入表单区域 */
.input-section {
  padding: 30px;
}

.form-container h3 {
  margin: 0 0 30px 0;
  color: #1a202c;
  font-size: 24px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #374151;
  font-weight: 500;
  font-size: 14px;
}

.form-input, .form-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  min-height: 120px;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-textarea:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}

/* 风格选项 */
.style-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-top: 8px;
}

.style-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.style-option:hover {
  border-color: #1976d2;
  transform: translateY(-2px);
}

.style-option.active {
  border-color: #1976d2;
  background: #f0f7ff;
}

.style-preview {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  margin-bottom: 8px;
}

.style-option span {
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  text-align: center;
}

/* 滑块控件 */
.slider-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.slider {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #e5e7eb;
  outline: none;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #1976d2;
  cursor: pointer;
}

.slider-value {
  font-weight: 600;
  color: #1976d2;
  min-width: 60px;
}

/* 复选框组 */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #1976d2;
}

.checkbox-item span {
  font-size: 14px;
  color: #374151;
}

/* 模型描述 */
.model-description {
  margin-top: 8px;
  font-size: 12px;
  color: #6b7280;
  font-style: italic;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.generate-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #1976d2 0%, #1560a8 100%);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(25, 118, 210, 0.3);
}

.generate-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.reset-btn {
  background: #f3f4f6;
  color: #374151;
  border: 2px solid #e5e7eb;
  padding: 14px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-btn:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

/* 生成进度区域 */
.generating-section {
  padding: 60px 30px;
  text-align: center;
}

.progress-container {
  max-width: 600px;
  margin: 0 auto;
}

.progress-header h3 {
  margin: 0 0 8px 0;
  color: #1a202c;
  font-size: 24px;
  font-weight: 600;
}

.progress-header p {
  margin: 0 0 30px 0;
  color: #6b7280;
  font-size: 16px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: 600;
  color: #1976d2;
  font-size: 14px;
}

.progress-steps {
  margin: 40px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.step.active {
  background: #f0f7ff;
  border: 1px solid #1976d2;
}

.step.completed {
  background: #f0fdf4;
  border: 1px solid #10b981;
}

.step-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.step.active .step-icon {
  background: #1976d2;
  color: white;
}

.step.completed .step-icon {
  background: #10b981;
  color: white;
}

.step:not(.active):not(.completed) .step-icon {
  background: #e5e7eb;
  color: #6b7280;
}

.cancel-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 20px;
}

.cancel-btn:hover {
  background: #dc2626;
}

/* 结果区域 */
.result-section {
  padding: 30px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 16px;
}

.result-header h3 {
  margin: 0;
  color: #1a202c;
  font-size: 24px;
  font-weight: 600;
}

.result-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.result-actions button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.preview-btn {
  background: #1976d2;
  color: white;
}

.download-btn {
  background: #10b981;
  color: white;
}

.edit-btn {
  background: #f59e0b;
  color: white;
}

.share-btn {
  background: #8b5cf6;
  color: white;
}

.new-btn {
  background: #6b7280;
  color: white;
}

.result-actions button:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

/* PPT信息卡片 */
.ppt-info-card {
  display: flex;
  gap: 20px;
  padding: 24px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 30px;
}

.ppt-thumbnail {
  flex-shrink: 0;
}

.thumbnail-placeholder {
  width: 120px;
  height: 90px;
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.ppt-details {
  flex: 1;
}

.ppt-details h4 {
  margin: 0 0 12px 0;
  color: #1a202c;
  font-size: 20px;
  font-weight: 600;
}

.ppt-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 12px;
}

.ppt-meta span {
  font-size: 14px;
  color: #6b7280;
}

.ppt-description {
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
}

/* 幻灯片预览 */
.slides-preview h4 {
  margin: 0 0 20px 0;
  color: #1a202c;
  font-size: 18px;
  font-weight: 600;
}

.slides-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.slide-item {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.slide-item:hover {
  border-color: #1976d2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.slide-number {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #1976d2;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.slide-content h5 {
  margin: 0 0 8px 0;
  color: #1a202c;
  font-size: 14px;
  font-weight: 600;
}

.slide-content p {
  margin: 0;
  color: #6b7280;
  font-size: 12px;
  line-height: 1.4;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .ppt-page {
    padding: 16px;
  }
  
  .page-header {
    padding: 16px;
  }
  
  .input-section, .generating-section, .result-section {
    padding: 20px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .result-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .result-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .ppt-info-card {
    flex-direction: column;
  }
  
  .slides-grid {
    grid-template-columns: 1fr;
  }
}
</style>