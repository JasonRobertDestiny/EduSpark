<template>
  <div class="exam-page">
    <div class="main-content">
      <!-- 输入配置区域 -->
      <div v-if="!isGenerating && !generatedExam" class="input-section">
        <div class="form-container">
          <h2 class="page-title">智能试卷生成</h2>
          <h3>试卷配置</h3>
          
          <!-- 基础信息 -->
          <div class="form-row">
            <div class="form-group">
              <label>试卷标题 *</label>
              <input 
                v-model="examConfig.title" 
                type="text" 
                class="form-input" 
                placeholder="请输入试卷标题"
              />
            </div>
            <div class="form-group">
              <label>学科类型 *</label>
              <select v-model="examConfig.subject" class="form-select">
                <option value="">请选择学科</option>
                <option value="math">数学</option>
                <option value="chinese">语文</option>
                <option value="english">英语</option>
                <option value="physics">物理</option>
                <option value="chemistry">化学</option>
                <option value="biology">生物</option>
                <option value="history">历史</option>
                <option value="geography">地理</option>
                <option value="politics">政治</option>
                <option value="computer">计算机</option>
              </select>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>年级水平</label>
              <select v-model="examConfig.grade" class="form-select">
                <option value="">请选择年级</option>
                <option value="primary">小学</option>
                <option value="junior">初中</option>
                <option value="senior">高中</option>
                <option value="college">大学</option>
              </select>
            </div>
            <div class="form-group">
              <label>考试时长（分钟）</label>
              <div class="slider-container">
                <input 
                  v-model="examConfig.duration" 
                  type="range" 
                  min="30" 
                  max="180" 
                  step="15" 
                  class="slider"
                />
                <span class="slider-value">{{ examConfig.duration }}分钟</span>
              </div>
            </div>
          </div>
          
          <!-- 知识点范围 -->
          <div class="form-group">
            <label>知识点范围</label>
            <textarea 
              v-model="examConfig.knowledgePoints" 
              class="form-textarea" 
              placeholder="请描述需要考查的知识点范围，例如：函数、导数、积分等"
            ></textarea>
          </div>
          
          <!-- 题型配置 -->
          <div class="question-types-section">
            <h4>题型配置</h4>
            <div class="question-types-grid">
              <div 
                v-for="type in questionTypes" 
                :key="type.id" 
                class="question-type-card"
                :class="{ active: type.enabled }"
                @click="toggleQuestionType(type)"
              >
                <div class="type-header">
                  <div class="type-icon" :style="{ background: type.color }">
                    {{ type.icon }}
                  </div>
                  <div class="type-info">
                    <h5>{{ type.name }}</h5>
                    <p>{{ type.description }}</p>
                  </div>
                  <div class="type-toggle">
                    <input 
                      type="checkbox" 
                      :checked="type.enabled" 
                      @click.stop
                      @change="toggleQuestionType(type)"
                    />
                  </div>
                </div>
                
                <div v-if="type.enabled" class="type-config" @click.stop>
                  <div class="config-row">
                    <label>题目数量</label>
                    <input 
                      v-model.number="type.count" 
                      type="number" 
                      min="1" 
                      max="20" 
                      class="config-input"
                      @click.stop
                    />
                  </div>
                  <div class="config-row">
                    <label>每题分值</label>
                    <input 
                      v-model.number="type.score" 
                      type="number" 
                      min="1" 
                      max="50" 
                      class="config-input"
                      @click.stop
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 难度分布 -->
          <div class="difficulty-section">
            <h4>难度分布</h4>
            <div class="difficulty-sliders">
              <div class="difficulty-item">
                <label>简单 ({{ difficultyDistribution.easy }}%)</label>
                <input 
                  v-model.number="difficultyDistribution.easy" 
                  type="range" 
                  min="0" 
                  max="100" 
                  class="difficulty-slider easy"
                  @input="adjustDifficulty('easy')"
                />
              </div>
              <div class="difficulty-item">
                <label>中等 ({{ difficultyDistribution.medium }}%)</label>
                <input 
                  v-model.number="difficultyDistribution.medium" 
                  type="range" 
                  min="0" 
                  max="100" 
                  class="difficulty-slider medium"
                  @input="adjustDifficulty('medium')"
                />
              </div>
              <div class="difficulty-item">
                <label>困难 ({{ difficultyDistribution.hard }}%)</label>
                <input 
                  v-model.number="difficultyDistribution.hard" 
                  type="range" 
                  min="0" 
                  max="100" 
                  class="difficulty-slider hard"
                  @input="adjustDifficulty('hard')"
                />
              </div>
            </div>
            <div class="difficulty-summary">
              <span>总计: {{ totalDifficulty }}%</span>
              <span v-if="totalDifficulty !== 100" class="warning">请确保总计为100%</span>
            </div>
          </div>
          
          <!-- 高级选项 -->
          <div class="advanced-options">
            <h4>高级选项</h4>
            <div class="options-grid">
              <div class="option-item">
                <input 
                  v-model="examConfig.includeAnswers" 
                  type="checkbox" 
                  id="includeAnswers"
                />
                <label for="includeAnswers">生成答案解析</label>
              </div>
              <div class="option-item">
                <input 
                  v-model="examConfig.includeScoring" 
                  type="checkbox" 
                  id="includeScoring"
                />
                <label for="includeScoring">包含评分标准</label>
              </div>
              <div class="option-item">
                <input 
                  v-model="examConfig.randomOrder" 
                  type="checkbox" 
                  id="randomOrder"
                />
                <label for="randomOrder">题目随机排序</label>
              </div>
              <div class="option-item">
                <input 
                  v-model="examConfig.multipleVersions" 
                  type="checkbox" 
                  id="multipleVersions"
                />
                <label for="multipleVersions">生成多套试卷</label>
              </div>
            </div>
          </div>
          
          <!-- AI模型选择 -->
          <div class="form-group">
            <label>AI生成模型</label>
            <select v-model="examConfig.aiModel" class="form-select">
              <option value="gpt-4">GPT-4 (推荐)</option>
              <option value="gpt-3.5">GPT-3.5</option>
              <option value="claude">Claude</option>
              <option value="wenxin">文心一言</option>
            </select>
            <p class="model-description">{{ getModelDescription() }}</p>
          </div>
          
          <!-- 操作按钮 -->
          <div class="action-buttons">
            <button 
              @click="generateExam" 
              :disabled="!canGenerate" 
              class="generate-btn"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
              </svg>
              生成试卷
            </button>
            <button @click="resetForm" class="reset-btn">重置配置</button>
          </div>
        </div>
      </div>
      
      <!-- 生成进度区域 -->
      <div v-if="isGenerating" class="generating-section">
        <div class="progress-container">
          <div class="progress-header">
            <h3>正在生成试卷...</h3>
            <p>请稍候，AI正在为您精心制作试卷</p>
          </div>
          
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <div class="progress-text">{{ progress }}%</div>
          
          <div class="progress-steps">
            <div 
              v-for="(step, index) in generationSteps" 
              :key="index" 
              class="step"
              :class="{ 
                active: index === currentStep, 
                completed: index < currentStep 
              }"
            >
              <div class="step-icon">{{ index + 1 }}</div>
              <span>{{ step }}</span>
            </div>
          </div>
          
          <button @click="cancelGeneration" class="cancel-btn">取消生成</button>
        </div>
      </div>
      
      <!-- 结果展示区域 -->
      <div v-if="generatedExam" class="result-section">
        <div class="result-header">
          <h3>试卷生成完成</h3>
          <div class="result-actions">
            <button @click="previewExam" class="preview-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
              </svg>
              预览
            </button>
            <button @click="downloadExam" class="download-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
              </svg>
              下载
            </button>
            <button @click="editExam" class="edit-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
              </svg>
              编辑
            </button>
            <button @click="shareExam" class="share-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
              </svg>
              分享
            </button>
            <button @click="createNewExam" class="new-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
              </svg>
              新建
            </button>
          </div>
        </div>
        
        <!-- 试卷信息卡片 -->
        <div class="exam-info-card">
          <div class="exam-thumbnail">
            <div class="thumbnail-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h8c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
              </svg>
            </div>
          </div>
          <div class="exam-details">
            <h4>{{ generatedExam.title }}</h4>
            <div class="exam-meta">
              <span>学科：{{ getSubjectName(generatedExam.subject) }}</span>
              <span>年级：{{ getGradeName(generatedExam.grade) }}</span>
              <span>时长：{{ generatedExam.duration }}分钟</span>
              <span>总分：{{ generatedExam.totalScore }}分</span>
              <span>题目数：{{ generatedExam.totalQuestions }}题</span>
              <span>生成时间：{{ generatedExam.createdAt }}</span>
            </div>
            <p class="exam-description">{{ generatedExam.description }}</p>
          </div>
        </div>
        
        <!-- 题目预览 -->
        <div class="questions-preview">
          <h4>题目预览</h4>
          <div class="questions-list">
            <div 
              v-for="(question, index) in generatedExam.questions.slice(0, 5)" 
              :key="index" 
              class="question-item"
              @click="selectQuestion(question)"
            >
              <div class="question-number">{{ index + 1 }}</div>
              <div class="question-content">
                <div class="question-type">{{ getQuestionTypeName(question.type) }}</div>
                <div class="question-text">{{ question.text }}</div>
                <div class="question-score">{{ question.score }}分</div>
              </div>
            </div>
            <div v-if="generatedExam.questions.length > 5" class="more-questions">
              <span>还有 {{ generatedExam.questions.length - 5 }} 道题目...</span>
              <button @click="viewAllQuestions" class="view-all-btn">查看全部</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { generateExam } from '@/services/api';
export default {
  name: 'Exam',
  data() {
    return {
      // 试卷配置
      examConfig: {
        title: '',
        subject: '',
        grade: '',
        duration: 90,
        knowledgePoints: '',
        includeAnswers: true,
        includeScoring: true,
        randomOrder: false,
        multipleVersions: false,
        aiModel: 'gpt-4'
      },
      
      // 题型配置
      questionTypes: [
        {
          id: 'choice',
          name: '选择题',
          description: '单选或多选题目',
          icon: 'A',
          color: '#1976d2',
          enabled: true,
          count: 10,
          score: 3
        },
        {
          id: 'blank',
          name: '填空题',
          description: '填写空白处答案',
          icon: '□',
          color: '#388e3c',
          enabled: true,
          count: 5,
          score: 4
        },
        {
          id: 'judge',
          name: '判断题',
          description: '判断对错',
          icon: '✓',
          color: '#f57c00',
          enabled: false,
          count: 5,
          score: 2
        },
        {
          id: 'short',
          name: '简答题',
          description: '简短回答问题',
          icon: '答',
          color: '#7b1fa2',
          enabled: true,
          count: 3,
          score: 8
        },
        {
          id: 'essay',
          name: '论述题',
          description: '详细论述分析',
          icon: '论',
          color: '#c2185b',
          enabled: false,
          count: 2,
          score: 15
        },
        {
          id: 'calculation',
          name: '计算题',
          description: '数学计算题目',
          icon: '∑',
          color: '#00796b',
          enabled: false,
          count: 3,
          score: 10
        }
      ],
      
      // 难度分布
      difficultyDistribution: {
        easy: 30,
        medium: 50,
        hard: 20
      },
      
      // 生成状态
      isGenerating: false,
      progress: 0,
      currentStep: 0,
      generationTimer: null,
      
      // 生成步骤
      generationSteps: [
        '分析试卷需求',
        '匹配知识点',
        '生成题目内容',
        '调整难度分布',
        '完善答案解析'
      ],
      
      // 生成结果
      generatedExam: null
    };
  },
  
  computed: {
    // 是否可以生成试卷
    canGenerate() {
      return this.examConfig.title.trim() && 
             this.examConfig.subject && 
             this.hasEnabledQuestionTypes &&
             this.totalDifficulty === 100;
    },
    
    // 是否有启用的题型
    hasEnabledQuestionTypes() {
      return this.questionTypes.some(type => type.enabled);
    },
    
    // 难度总计
    totalDifficulty() {
      return this.difficultyDistribution.easy + 
             this.difficultyDistribution.medium + 
             this.difficultyDistribution.hard;
    },
    
    // 总题目数
    totalQuestions() {
      return this.questionTypes
        .filter(type => type.enabled)
        .reduce((sum, type) => sum + type.count, 0);
    },
    
    // 总分数
    totalScore() {
      return this.questionTypes
        .filter(type => type.enabled)
        .reduce((sum, type) => sum + (type.count * type.score), 0);
    }
  },
  
  methods: {
    // 切换题型启用状态
    toggleQuestionType(type) {
      type.enabled = !type.enabled;
    },
    
    // 调整难度分布
    adjustDifficulty(changedType) {
      // 确保总和为100%
      const total = this.difficultyDistribution.easy + 
                   this.difficultyDistribution.medium + 
                   this.difficultyDistribution.hard;
      
      if (total > 100) {
        const excess = total - 100;
        const others = ['easy', 'medium', 'hard'].filter(t => t !== changedType);
        
        // 从其他类型中减去多余的部分
        others.forEach(type => {
          const reduction = Math.min(this.difficultyDistribution[type], excess / others.length);
          this.difficultyDistribution[type] = Math.max(0, this.difficultyDistribution[type] - reduction);
        });
      }
    },
    
    // 获取模型描述
    getModelDescription() {
      const descriptions = {
        'gpt-4': '最先进的AI模型，生成质量最高，适合复杂试卷',
        'gpt-3.5': '平衡性能和速度，适合一般试卷生成',
        'claude': '擅长逻辑推理，适合理科试卷',
        'wenxin': '中文优化模型，适合语文等文科试卷'
      };
      return descriptions[this.examConfig.aiModel] || '';
    },
    
    // 生成试卷
    async generateExam() {
      if (!this.canGenerate) return;
      this.isGenerating = true;
      this.progress = 0;
      this.currentStep = 0;
      this.generatedExam = null;
      try {
        // 调用后端API生成试卷
        const result = await generateExam({
          ...this.examConfig,
          questionTypes: this.questionTypes.filter(t => t.enabled).map(t => ({
            id: t.id,
            count: t.count,
            score: t.score
          })),
          difficultyDistribution: this.difficultyDistribution
        });
        this.generatedExam = result;
      } catch (error) {
        console.error('试卷生成失败:', error);
        alert('试卷生成失败，请重试');
      } finally {
        this.isGenerating = false;
        if (this.generationTimer) {
          clearInterval(this.generationTimer);
          this.generationTimer = null;
        }
      }
    },
    
    // 模拟生成过程
    async simulateGeneration() {
      const steps = [
        { name: '分析试卷需求', duration: 1500 },
        { name: '匹配知识点', duration: 2000 },
        { name: '生成题目内容', duration: 3000 },
        { name: '调整难度分布', duration: 1500 },
        { name: '完善答案解析', duration: 1000 }
      ];
      
      let totalDuration = steps.reduce((sum, step) => sum + step.duration, 0);
      let elapsed = 0;
      
      for (let i = 0; i < steps.length; i++) {
        this.currentStep = i;
        
        const stepDuration = steps[i].duration;
        const stepStart = elapsed;
        
        await new Promise(resolve => {
          const stepTimer = setInterval(() => {
            elapsed += 100;
            this.progress = Math.min(100, (elapsed / totalDuration) * 100);
            
            if (elapsed >= stepStart + stepDuration) {
              clearInterval(stepTimer);
              resolve();
            }
          }, 100);
        });
      }
      
      this.currentStep = steps.length;
      this.progress = 100;
    },
    
    // 生成模拟题目数据
    generateMockQuestions() {
      const questions = [];
      let questionNumber = 1;
      
      this.questionTypes
        .filter(type => type.enabled)
        .forEach(type => {
          for (let i = 0; i < type.count; i++) {
            questions.push({
              id: questionNumber,
              type: type.id,
              text: this.generateMockQuestionText(type, questionNumber),
              score: type.score,
              difficulty: this.getRandomDifficulty(),
              answer: '示例答案',
              explanation: '这是答案解析'
            });
            questionNumber++;
          }
        });
      
      return questions;
    },
    
    // 生成模拟题目文本
    generateMockQuestionText(type, number) {
      const templates = {
        choice: `第${number}题：以下哪个选项是正确的？\nA. 选项A\nB. 选项B\nC. 选项C\nD. 选项D`,
        blank: `第${number}题：请填写空白处的内容：______是正确答案。`,
        judge: `第${number}题：判断题：这个陈述是正确的。（）`,
        short: `第${number}题：请简要回答以下问题：这是一个简答题的示例。`,
        essay: `第${number}题：请详细论述以下问题：这是一个论述题的示例，需要详细分析。`,
        calculation: `第${number}题：计算题：求解以下数学问题。`
      };
      return templates[type.id] || `第${number}题：示例题目`;
    },
    
    // 获取随机难度
    getRandomDifficulty() {
      const rand = Math.random() * 100;
      if (rand < this.difficultyDistribution.easy) return 'easy';
      if (rand < this.difficultyDistribution.easy + this.difficultyDistribution.medium) return 'medium';
      return 'hard';
    },
    
    // 取消生成
    cancelGeneration() {
      if (this.generationTimer) {
        clearInterval(this.generationTimer);
        this.generationTimer = null;
      }
      this.isGenerating = false;
      this.progress = 0;
      this.currentStep = 0;
    },
    
    // 重置表单
    resetForm() {
      this.examConfig = {
        title: '',
        subject: '',
        grade: '',
        duration: 90,
        knowledgePoints: '',
        includeAnswers: true,
        includeScoring: true,
        randomOrder: false,
        multipleVersions: false,
        aiModel: 'gpt-4'
      };
      
      this.difficultyDistribution = {
        easy: 30,
        medium: 50,
        hard: 20
      };
      
      this.questionTypes.forEach(type => {
        type.enabled = ['choice', 'blank', 'short'].includes(type.id);
      });
      
      this.generatedExam = null;
    },
    
    // 预览试卷
    previewExam() {
      if (!this.generatedExam) return;
      
      // 创建预览模态框
      const modal = document.createElement('div');
      modal.className = 'exam-preview-modal';
      modal.innerHTML = `
        <div class="modal-overlay" onclick="this.parentElement.remove()">
          <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
              <h3>试卷预览</h3>
              <button class="close-btn" onclick="this.closest('.exam-preview-modal').remove()">×</button>
            </div>
            <div class="modal-body">
              <div class="exam-header">
                <h2>${this.generatedExam.title}</h2>
                <div class="exam-info">
                  <span>学科：${this.getSubjectName(this.generatedExam.subject)}</span>
                  <span>年级：${this.getGradeName(this.generatedExam.grade)}</span>
                  <span>时长：${this.generatedExam.duration}分钟</span>
                  <span>总分：${this.generatedExam.totalScore}分</span>
                </div>
                <div class="exam-instructions">
                  <p><strong>考试说明：</strong></p>
                  <p>1. 本试卷共${this.generatedExam.totalQuestions}题，满分${this.generatedExam.totalScore}分，考试时间${this.generatedExam.duration}分钟。</p>
                  <p>2. 请在答题前仔细阅读各题目要求。</p>
                  <p>3. 答题时请注意字迹清晰，保持卷面整洁。</p>
                </div>
              </div>
              <div class="questions-section">
                ${this.generatedExam.questions.map((question, index) => `
                  <div class="question-preview">
                    <div class="question-title">
                      <span class="question-num">${index + 1}.</span>
                      <span class="question-type-label">[${this.getQuestionTypeName(question.type)}]</span>
                      <span class="question-score-label">(${question.score}分)</span>
                    </div>
                    <div class="question-content">${question.text}</div>
                    ${question.options ? `
                      <div class="question-options">
                        ${question.options.map((option, optIndex) => `
                          <div class="option-item">${'ABCD'[optIndex]}. ${option}</div>
                        `).join('')}
                      </div>
                    ` : ''}
                    <div class="answer-space"></div>
                  </div>
                `).join('')}
              </div>
            </div>
            <div class="modal-footer">
              <button onclick="window.print()" class="print-btn">打印试卷</button>
              <button onclick="this.closest('.exam-preview-modal').remove()" class="close-modal-btn">关闭预览</button>
            </div>
          </div>
        </div>
      `;
      
      // 添加预览样式
      const style = document.createElement('style');
      style.textContent = `
        .exam-preview-modal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 9999;
        }
        .exam-preview-modal .modal-overlay {
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        .exam-preview-modal .modal-content {
          background: white;
          border-radius: 12px;
          max-width: 900px;
          width: 100%;
          max-height: 90vh;
          display: flex;
          flex-direction: column;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .exam-preview-modal .modal-header {
          padding: 20px 24px;
          border-bottom: 1px solid #e9ecef;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .exam-preview-modal .modal-body {
          padding: 24px;
          overflow-y: auto;
          flex: 1;
        }
        .exam-header h2 {
          text-align: center;
          margin-bottom: 16px;
          color: #2c3e50;
          font-size: 24px;
        }
        .exam-info {
          display: flex;
          justify-content: center;
          gap: 24px;
          margin-bottom: 20px;
          font-size: 14px;
          color: #666;
        }
        .exam-instructions {
          background: #f8f9fa;
          padding: 16px;
          border-radius: 8px;
          margin-bottom: 24px;
          font-size: 14px;
          line-height: 1.6;
        }
        .question-preview {
          margin-bottom: 24px;
          padding-bottom: 20px;
          border-bottom: 1px solid #eee;
        }
        .question-title {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 12px;
        }
        .question-num {
          font-weight: bold;
          color: #2c3e50;
        }
        .question-type-label {
          background: #e3f2fd;
          color: #1976d2;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 12px;
        }
        .question-score-label {
          background: #fff3e0;
          color: #f57c00;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 12px;
        }
        .question-content {
          font-size: 15px;
          line-height: 1.6;
          margin-bottom: 12px;
          color: #2c3e50;
        }
        .option-item {
          padding: 4px 0;
          font-size: 14px;
          color: #495057;
        }
        .answer-space {
          height: 40px;
          border-bottom: 1px solid #ddd;
          margin-top: 12px;
        }
        .modal-footer {
          padding: 16px 24px;
          border-top: 1px solid #e9ecef;
          display: flex;
          justify-content: flex-end;
          gap: 12px;
        }
        .print-btn, .close-modal-btn {
          padding: 8px 16px;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.2s;
        }
        .print-btn {
          background: #2196f3;
          color: white;
        }
        .print-btn:hover {
          background: #1976d2;
        }
        .close-modal-btn {
          background: #6c757d;
          color: white;
        }
        .close-modal-btn:hover {
          background: #5a6268;
        }
      `;
      
      document.head.appendChild(style);
      document.body.appendChild(modal);
    },
    
    // 下载试卷
    downloadExam() {
      if (!this.generatedExam) return;
      
      const link = document.createElement('a');
      link.href = '#';
      link.download = `${this.generatedExam.title}.docx`;
      link.click();
      
      alert('试卷下载功能开发中...');
    },
    
    // 编辑试卷
    editExam() {
      if (!this.generatedExam) return;
      
      // 创建编辑模态框
      const modal = document.createElement('div');
      modal.className = 'exam-edit-modal';
      modal.innerHTML = `
        <div class="modal-overlay" onclick="this.parentElement.remove()">
          <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
              <h3>编辑试卷</h3>
              <button class="close-btn" onclick="this.closest('.exam-edit-modal').remove()">×</button>
            </div>
            <div class="modal-body">
              <div class="edit-form">
                <div class="form-group">
                  <label>试卷标题</label>
                  <input type="text" id="edit-title" value="${this.generatedExam.title}" class="form-input">
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>考试时长(分钟)</label>
                    <input type="number" id="edit-duration" value="${this.generatedExam.duration}" class="form-input">
                  </div>
                  <div class="form-group">
                    <label>总分</label>
                    <input type="number" id="edit-total-score" value="${this.generatedExam.totalScore}" class="form-input" readonly>
                  </div>
                </div>
                <div class="form-group">
                  <label>试卷描述</label>
                  <textarea id="edit-description" class="form-textarea">${this.generatedExam.description || ''}</textarea>
                </div>
              </div>
              <div class="questions-edit">
                <h4>题目编辑</h4>
                <div class="questions-list">
                  ${this.generatedExam.questions.map((question, index) => `
                    <div class="question-edit-item" data-index="${index}">
                      <div class="question-header">
                        <span class="question-number">${index + 1}</span>
                        <span class="question-type">${this.getQuestionTypeName(question.type)}</span>
                        <input type="number" value="${question.score}" class="score-input" onchange="updateQuestionScore(${index}, this.value)">
                        <span>分</span>
                        <button class="delete-question-btn" onclick="deleteQuestion(${index})">删除</button>
                      </div>
                      <div class="question-content-edit">
                        <textarea class="question-text-input" onchange="updateQuestionText(${index}, this.value)">${question.text}</textarea>
                        ${question.options ? `
                          <div class="options-edit">
                            ${question.options.map((option, optIndex) => `
                              <div class="option-edit">
                                <span>${'ABCD'[optIndex]}.</span>
                                <input type="text" value="${option}" onchange="updateQuestionOption(${index}, ${optIndex}, this.value)">
                              </div>
                            `).join('')}
                          </div>
                        ` : ''}
                        ${question.answer ? `
                          <div class="answer-edit">
                            <label>答案：</label>
                            <input type="text" value="${question.answer}" onchange="updateQuestionAnswer(${index}, this.value)">
                          </div>
                        ` : ''}
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button onclick="saveExamChanges()" class="save-btn">保存修改</button>
              <button onclick="this.closest('.exam-edit-modal').remove()" class="cancel-btn">取消</button>
            </div>
          </div>
        </div>
      `;
      
      // 添加编辑功能的JavaScript
      const script = document.createElement('script');
      script.textContent = `
        function updateQuestionScore(index, score) {
          // 这里可以添加更新题目分数的逻辑
          console.log('更新题目', index, '分数为', score);
        }
        function updateQuestionText(index, text) {
          console.log('更新题目', index, '内容为', text);
        }
        function updateQuestionOption(questionIndex, optionIndex, text) {
          console.log('更新题目', questionIndex, '选项', optionIndex, '为', text);
        }
        function updateQuestionAnswer(index, answer) {
          console.log('更新题目', index, '答案为', answer);
        }
        function deleteQuestion(index) {
          if (confirm('确定要删除这道题目吗？')) {
            console.log('删除题目', index);
            // 这里可以添加删除题目的逻辑
          }
        }
        function saveExamChanges() {
          const title = document.getElementById('edit-title').value;
          const duration = document.getElementById('edit-duration').value;
          const description = document.getElementById('edit-description').value;
          
          alert('试卷修改已保存！\n标题：' + title + '\n时长：' + duration + '分钟');
          document.querySelector('.exam-edit-modal').remove();
        }
      `;
      
      // 添加编辑样式
      const style = document.createElement('style');
      style.textContent = `
        .exam-edit-modal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 9999;
        }
        .exam-edit-modal .modal-content {
          background: white;
          border-radius: 12px;
          max-width: 1000px;
          width: 100%;
          max-height: 90vh;
          display: flex;
          flex-direction: column;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .edit-form {
          margin-bottom: 24px;
          padding: 20px;
          background: #f8f9fa;
          border-radius: 8px;
        }
        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }
        .questions-edit h4 {
          margin-bottom: 16px;
          color: #2c3e50;
        }
        .question-edit-item {
          margin-bottom: 20px;
          padding: 16px;
          border: 1px solid #e9ecef;
          border-radius: 8px;
          background: white;
        }
        .question-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
        }
        .score-input {
          width: 60px;
          padding: 4px 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }
        .delete-question-btn {
          background: #dc3545;
          color: white;
          border: none;
          padding: 4px 8px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 12px;
          margin-left: auto;
        }
        .question-text-input {
          width: 100%;
          min-height: 60px;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
          margin-bottom: 12px;
          resize: vertical;
        }
        .options-edit {
          margin-bottom: 12px;
        }
        .option-edit {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
        }
        .option-edit input {
          flex: 1;
          padding: 6px 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }
        .answer-edit {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .answer-edit input {
          flex: 1;
          padding: 6px 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }
        .save-btn {
          background: #28a745;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 6px;
          cursor: pointer;
        }
        .cancel-btn {
          background: #6c757d;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 6px;
          cursor: pointer;
        }
      `;
      
      document.head.appendChild(style);
      document.head.appendChild(script);
      document.body.appendChild(modal);
    },
    
    // 分享试卷
    shareExam() {
      if (!this.generatedExam) return;
      
      if (navigator.share) {
        navigator.share({
          title: this.generatedExam.title,
          text: '查看我生成的试卷',
          url: window.location.href
        });
      } else {
        navigator.clipboard.writeText(window.location.href).then(() => {
          alert('链接已复制到剪贴板');
        });
      }
    },
    
    // 创建新试卷
    createNewExam() {
      this.resetForm();
    },
    
    // 选择题目
    selectQuestion(question) {
      console.log('选中题目:', question);
    },
    
    // 查看所有题目
    viewAllQuestions() {
      // 创建一个模态框显示所有题目
      const modal = document.createElement('div');
      modal.className = 'questions-modal';
      modal.innerHTML = `
        <div class="modal-overlay" onclick="this.parentElement.remove()">
          <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
              <h3>全部题目预览</h3>
              <button class="close-btn" onclick="this.closest('.questions-modal').remove()">×</button>
            </div>
            <div class="modal-body">
              ${this.generatedExam.questions.map((question, index) => `
                <div class="question-item-full">
                  <div class="question-header">
                    <span class="question-number">${index + 1}</span>
                    <span class="question-type">${this.getQuestionTypeName(question.type)}</span>
                    <span class="question-score">${question.score}分</span>
                  </div>
                  <div class="question-text">${question.text}</div>
                  ${question.options ? `
                    <div class="question-options">
                      ${question.options.map((option, optIndex) => `
                        <div class="option">${'ABCD'[optIndex]}. ${option}</div>
                      `).join('')}
                    </div>
                  ` : ''}
                  ${question.answer ? `
                    <div class="question-answer">
                      <strong>答案：</strong>${question.answer}
                    </div>
                  ` : ''}
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;
      
      // 添加样式
      const style = document.createElement('style');
      style.textContent = `
        .questions-modal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 9999;
        }
        .modal-overlay {
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        .modal-content {
          background: white;
          border-radius: 12px;
          max-width: 800px;
          width: 100%;
          max-height: 80vh;
          display: flex;
          flex-direction: column;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .modal-header {
          padding: 20px 24px;
          border-bottom: 1px solid #e9ecef;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .modal-header h3 {
          margin: 0;
          color: #2c3e50;
          font-size: 20px;
        }
        .close-btn {
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          color: #6c757d;
          padding: 0;
          width: 30px;
          height: 30px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: all 0.2s;
        }
        .close-btn:hover {
          background: #f8f9fa;
          color: #495057;
        }
        .modal-body {
          padding: 20px 24px;
          overflow-y: auto;
          flex: 1;
        }
        .question-item-full {
          margin-bottom: 24px;
          padding: 16px;
          border: 1px solid #e9ecef;
          border-radius: 8px;
          background: #f8f9fa;
        }
        .question-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
        }
        .question-number {
          background: #2196f3;
          color: white;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: bold;
        }
        .question-type {
          background: #e3f2fd;
          color: #1976d2;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          font-weight: 500;
        }
        .question-score {
          background: #fff3e0;
          color: #f57c00;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          font-weight: 500;
          margin-left: auto;
        }
        .question-text {
          font-size: 14px;
          line-height: 1.6;
          color: #2c3e50;
          margin-bottom: 12px;
        }
        .question-options {
          margin-bottom: 12px;
        }
        .option {
          padding: 6px 0;
          font-size: 14px;
          color: #495057;
        }
        .question-answer {
          padding: 8px 12px;
          background: #e8f5e8;
          border-radius: 6px;
          font-size: 14px;
          color: #2e7d32;
        }
      `;
      
      document.head.appendChild(style);
      document.body.appendChild(modal);
    },
    
    // 获取学科名称
    getSubjectName(subject) {
      const names = {
        math: '数学',
        chinese: '语文',
        english: '英语',
        physics: '物理',
        chemistry: '化学',
        biology: '生物',
        history: '历史',
        geography: '地理',
        politics: '政治',
        computer: '计算机'
      };
      return names[subject] || subject;
    },
    
    // 获取年级名称
    getGradeName(grade) {
      const names = {
        primary: '小学',
        junior: '初中',
        senior: '高中',
        college: '大学'
      };
      return names[grade] || grade;
    },
    
    // 获取题型名称
    getQuestionTypeName(typeId) {
      const type = this.questionTypes.find(t => t.id === typeId);
      return type ? type.name : typeId;
    }
  }
};
</script>

<style scoped>
.exam-page {
  padding: 0;
  background: linear-gradient(135deg, #2196f3 0%, #1976d2 50%, #0d47a1 100%);
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow-y: auto;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 25px 0;
  text-align: center;
  background: linear-gradient(45deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px 20px 20px 20px;
}

.input-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.form-container h3 {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 8px;
  font-size: 14px;
}

.form-input,
.form-select,
.form-textarea {
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.slider {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #e9ecef;
  outline: none;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2196f3;
  cursor: pointer;
}

.slider-value {
  font-weight: 600;
  color: #2c3e50;
  min-width: 80px;
  text-align: right;
}

.question-types-section {
  margin: 30px 0;
}

.question-types-section h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20px;
}

.question-types-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 20px;
}

.question-type-card {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  position: relative;
}

.question-type-card.active {
  border-color: #2196f3;
  background: rgba(33, 150, 243, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(33, 150, 243, 0.15);
}

.model-option.selected {
  border-color: #2196f3;
  background: rgba(33, 150, 243, 0.05);
}

.question-type-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.type-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.type-icon {
  width: 45px;
  height: 45px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
}

.type-info {
  flex: 1;
}

.type-info h5 {
  margin: 0 0 5px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.type-info p {
  margin: 0;
  font-size: 13px;
  color: #6c757d;
}

.type-toggle input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: #2196f3;
}

.type-config {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  padding-top: 15px;
  border-top: 1px solid #e9ecef;
}

.config-row {
  display: flex;
  flex-direction: column;
}

.config-row label {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 5px;
}

.config-input {
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
}

.difficulty-section {
  margin: 30px 0;
}

.difficulty-section h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20px;
}

.difficulty-sliders {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 15px;
}

.difficulty-item {
  text-align: center;
  padding: 20px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  background: white;
}

.difficulty-item label {
  font-weight: 600;
  margin-bottom: 15px;
  display: block;
  color: #495057;
}

.difficulty-slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  outline: none;
  -webkit-appearance: none;
}

.difficulty-slider.easy {
  background: linear-gradient(to right, #28a745 0%, #28a745 var(--value), #e9ecef var(--value), #e9ecef 100%);
}

.difficulty-slider.medium {
  background: linear-gradient(to right, #ffc107 0%, #ffc107 var(--value), #e9ecef var(--value), #e9ecef 100%);
}

.difficulty-slider.hard {
  background: linear-gradient(to right, #dc3545 0%, #dc3545 var(--value), #e9ecef var(--value), #e9ecef 100%);
}

.difficulty-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  border: 3px solid #2196f3;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.difficulty-summary {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  font-weight: 600;
}

.difficulty-summary .warning {
  color: #dc3545;
  margin-left: 15px;
}

.advanced-options {
  margin: 30px 0;
}

.advanced-options h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20px;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-item:hover {
  border-color: #2196f3;
  background: rgba(33, 150, 243, 0.02);
}

.option-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #2196f3;
}

.option-item label {
  font-size: 14px;
  color: #495057;
  cursor: pointer;
  margin: 0;
}

.model-description {
  font-size: 12px;
  color: #6c757d;
  margin-top: 8px;
  font-style: italic;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
  padding-top: 25px;
  border-top: 2px solid #e9ecef;
}

.generate-btn {
  flex: 1;
  padding: 15px 30px;
  background: linear-gradient(45deg, #2196f3, #1976d2);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(33, 150, 243, 0.3);
}

.generate-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.reset-btn {
  padding: 15px 30px;
  background: transparent;
  color: #6c757d;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  border-color: #dc3545;
  color: #dc3545;
}

.generating-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  text-align: center;
}

.progress-container {
  max-width: 600px;
  margin: 0 auto;
}

.progress-header h3 {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
}

.progress-header p {
  color: #6c757d;
  margin-bottom: 30px;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: #e9ecef;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(45deg, #2196f3, #1976d2);
  transition: width 0.5s ease;
}

.progress-text {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 30px;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  position: relative;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 40px;
  right: 40px;
  height: 2px;
  background: #e9ecef;
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
  flex: 1;
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #6c757d;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.step.active .step-icon {
  background: #2196f3;
  color: white;
  animation: pulse 2s infinite;
}

.step.completed .step-icon {
  background: #28a745;
  color: white;
}

.step span {
  font-size: 12px;
  color: #6c757d;
  text-align: center;
  max-width: 100px;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(33, 150, 243, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(33, 150, 243, 0); }
  100% { box-shadow: 0 0 0 0 rgba(33, 150, 243, 0); }
}

.cancel-btn {
  padding: 12px 24px;
  background: transparent;
  color: #dc3545;
  border: 2px solid #dc3545;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #dc3545;
  color: white;
}

.result-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.result-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.result-actions {
  display: flex;
  gap: 10px;
}

.result-actions button {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.preview-btn {
  background: #17a2b8;
  color: white;
}

.download-btn {
  background: #28a745;
  color: white;
}

.edit-btn {
  background: #ffc107;
  color: #212529;
}

.share-btn {
  background: #6f42c1;
  color: white;
}

.new-btn {
  background: #2196f3;
  color: white;
}

.result-actions button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.exam-info-card {
  display: flex;
  gap: 20px;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 25px;
}

.exam-thumbnail {
  width: 80px;
  height: 80px;
  background: #e9ecef;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

.exam-details {
  flex: 1;
}

.exam-details h4 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 10px 0;
}

.exam-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 10px;
}

.exam-meta span {
  font-size: 13px;
  color: #6c757d;
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
}

.exam-description {
  color: #495057;
  margin: 0;
  line-height: 1.5;
}

.questions-preview {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 25px;
}

.questions-preview h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
}

.questions-list {
  max-height: 400px;
  overflow-y: auto;
}

.question-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.question-item:hover {
  border-color: #2196f3;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
  transform: translateY(-1px);
}

.question-number {
  width: 30px;
  height: 30px;
  background: #2196f3;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.question-content {
  flex: 1;
}

.question-type {
  font-size: 12px;
  color: #6c757d;
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 3px;
  display: inline-block;
  margin-bottom: 5px;
}

.question-text {
  color: #495057;
  line-height: 1.5;
  margin-bottom: 5px;
}

.question-score {
  font-size: 12px;
  color: #28a745;
  font-weight: 600;
}

.more-questions {
  text-align: center;
  padding: 20px;
  color: #6c757d;
}

.view-all-btn {
  padding: 8px 16px;
  background: transparent;
  color: #2196f3;
  border: 1px solid #2196f3;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
  margin-left: 10px;
}

.view-all-btn:hover {
  background: #2196f3;
  color: white;
}

@media (max-width: 768px) {
  .exam-page {
    padding: 15px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .question-types-grid {
    grid-template-columns: 1fr;
  }
  
  .difficulty-sliders {
    grid-template-columns: 1fr;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .result-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .result-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .exam-info-card {
    flex-direction: column;
    text-align: center;
  }
  
  .exam-meta {
    justify-content: center;
  }
}
</style>