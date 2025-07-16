<template>
  <div class="homework-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">智能作业生成</h1>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧配置区域 -->
      <div class="config-section">
        <!-- 基础配置 -->
        <div class="config-card">
          <h3 class="card-title">基础配置</h3>
          <div class="form-group">
            <label>作业标题</label>
            <input 
              v-model="homeworkConfig.title" 
              type="text" 
              placeholder="请输入作业标题"
              class="form-input"
            >
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>学科</label>
              <select v-model="homeworkConfig.subject" class="form-select">
                <option value="">请选择学科</option>
                <option value="数学">数学</option>
                <option value="计算机">计算机</option>
              </select>
            </div>
            <div class="form-group">
              <label>年级</label>
              <select v-model="homeworkConfig.grade" class="form-select">
                <option value="">请选择年级</option>
                <option value="高中一年级">高中一年级</option>
                <option value="高中二年级">高中二年级</option>
                <option value="高中三年级">高中三年级</option>
                <option value="大学">大学</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>知识点范围</label>
            <textarea 
              v-model="homeworkConfig.knowledgePoints" 
              placeholder="请输入相关知识点，如：二次函数、一元二次方程等"
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>
        </div>

        <!-- 题型配置 -->
        <div class="config-card">
          <h3 class="card-title">题型配置</h3>
          <div class="question-types">
            <div 
              v-for="type in questionTypes" 
              :key="type.id"
              class="type-card"
              :class="{ active: type.enabled }"
              @click="toggleQuestionType(type)"
            >
              <div class="type-header">
                <span class="type-icon">{{ type.icon }}</span>
                <span class="type-name">{{ type.name }}</span>
                <span class="type-toggle" :class="{ active: type.enabled }"></span>
              </div>
              <div v-if="type.enabled" class="type-config" @click.stop>
                <div class="config-item">
                  <label>题目数量</label>
                  <input 
                    v-model.number="type.count" 
                    type="number" 
                    min="1" 
                    max="20"
                    @click.stop
                  >
                </div>
                <div class="config-item">
                  <label>每题分值</label>
                  <input 
                    v-model.number="type.score" 
                    type="number" 
                    min="1" 
                    max="20"
                    @click.stop
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 难度分布 -->
        <div class="config-card">
          <h3 class="card-title">难度分布</h3>
          <div class="difficulty-sliders">
            <div class="slider-group">
              <label>简单 ({{ difficultyDistribution.easy }}%)</label>
              <input 
                type="range" 
                min="0" 
                max="100" 
                v-model="difficultyDistribution.easy"
                @input="adjustDifficulty('easy')"
                class="difficulty-slider easy"
              >
            </div>
            <div class="slider-group">
              <label>中等 ({{ difficultyDistribution.medium }}%)</label>
              <input 
                type="range" 
                min="0" 
                max="100" 
                v-model="difficultyDistribution.medium"
                @input="adjustDifficulty('medium')"
                class="difficulty-slider medium"
              >
            </div>
            <div class="slider-group">
              <label>困难 ({{ difficultyDistribution.hard }}%)</label>
              <input 
                type="range" 
                min="0" 
                max="100" 
                v-model="difficultyDistribution.hard"
                @input="adjustDifficulty('hard')"
                class="difficulty-slider hard"
              >
            </div>
          </div>
        </div>

        <!-- 高级选项 -->
        <div class="config-card">
          <h3 class="card-title">高级选项</h3>
          <div class="advanced-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="homeworkConfig.includeAnswers">
              <span class="checkmark"></span>
              生成参考答案
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="homeworkConfig.includeExplanations">
              <span class="checkmark"></span>
              包含解题思路
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="homeworkConfig.randomOrder">
              <span class="checkmark"></span>
              题目随机排序
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="homeworkConfig.multipleVersions">
              <span class="checkmark"></span>
              生成多个版本
            </label>
          </div>
        </div>

        <!-- AI模型选择 -->
        <div class="config-card">
          <h3 class="card-title">AI模型</h3>
          <select v-model="homeworkConfig.aiModel" class="form-select">
            <option value="gpt-4">GPT-4 (推荐)</option>
            <option value="gpt-3.5">GPT-3.5</option>
            <option value="claude">Claude</option>
            <option value="wenxin">文心一言</option>
          </select>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button 
            @click="generateHomework" 
            :disabled="!canGenerate || isGenerating"
            class="generate-btn"
          >
            <span v-if="isGenerating" class="loading-spinner"></span>
            {{ isGenerating ? '生成中...' : '生成作业' }}
          </button>
          <button @click="resetConfig" class="reset-btn">重置配置</button>
        </div>
      </div>

      <!-- 右侧结果区域 -->
      <div class="result-section">
        <!-- 生成进度 -->
        <div v-if="isGenerating" class="progress-card">
          <h3>生成进度</h3>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <p class="progress-text">{{ progressText }}</p>
        </div>

        <!-- 生成结果 -->
        <div v-if="generatedHomework" class="homework-result">
          <div class="result-header">
            <h3>生成结果</h3>
            <div class="result-actions">
              <button @click="previewHomework" class="action-btn preview">预览</button>
              <button @click="downloadHomework" class="action-btn download">下载</button>
              <button @click="editHomework" class="action-btn edit">编辑</button>
              <button @click="shareHomework" class="action-btn share">分享</button>
              <button @click="newHomework" class="action-btn new">新建</button>
            </div>
          </div>

          <!-- 作业信息卡片 -->
          <div class="homework-card">
            <div class="homework-thumbnail">
              <div class="thumbnail-content">
                <h4>{{ generatedHomework.title }}</h4>
                <p>{{ generatedHomework.subject }} · {{ generatedHomework.grade }}</p>
              </div>
            </div>
            <div class="homework-details">
              <div class="detail-item">
                <span class="label">题目总数:</span>
                <span class="value">{{ generatedHomework.totalQuestions }}题</span>
              </div>
              <div class="detail-item">
                <span class="label">预计用时:</span>
                <span class="value">{{ generatedHomework.estimatedTime }}分钟</span>
              </div>
              <div class="detail-item">
                <span class="label">难度分布:</span>
                <span class="value">简单{{ difficultyDistribution.easy }}% 中等{{ difficultyDistribution.medium }}% 困难{{ difficultyDistribution.hard }}%</span>
              </div>
            </div>
            <div class="homework-meta">
              <span class="meta-item">生成时间: {{ generatedHomework.createdAt }}</span>
              <span class="meta-item">AI模型: {{ homeworkConfig.aiModel.toUpperCase() }}</span>
            </div>
            <div class="homework-description">
              <p>{{ generatedHomework.description }}</p>
            </div>
          </div>

          <!-- 题目预览 -->
          <div class="questions-preview">
            <h4>题目预览 (前5题)</h4>
            <div class="question-list">
              <div 
                v-for="(question, index) in generatedHomework.questions.slice(0, 5)" 
                :key="index"
                class="question-item"
              >
                <div class="question-header">
                  <span class="question-number">{{ index + 1 }}.</span>
                  <span class="question-type">{{ question.type }}</span>
                  <span class="question-score">{{ question.score }}分</span>
                </div>
                <div class="question-content">{{ question.content }}</div>
                <div v-if="question.options" class="question-options">
                  <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option">
                    {{ String.fromCharCode(65 + optIndex) }}. {{ option }}
                  </div>
                </div>
              </div>
            </div>
            <button @click="viewAllQuestions" class="view-all-btn">查看全部 {{ generatedHomework.totalQuestions }} 题</button>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!isGenerating && !generatedHomework" class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>开始生成您的智能作业</h3>
          <p>配置左侧参数，点击"生成作业"按钮开始</p>
        </div>
      </div>
    </div>

    <!-- 预览模态框 -->
    <div v-if="showPreviewModal" class="modal-overlay" @click="showPreviewModal = false">
      <div class="modal-content preview-modal" @click.stop>
        <div class="modal-header">
          <h3>作业预览</h3>
          <button @click="showPreviewModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="homework-preview">
            <div class="homework-header">
              <h2>{{ generatedHomework.title }}</h2>
              <div class="homework-info">
                <span>学科：{{ generatedHomework.subject }}</span>
                <span>年级：{{ generatedHomework.grade }}</span>
                <span>预计用时：{{ generatedHomework.estimatedTime }}分钟</span>
                <span>题目总数：{{ generatedHomework.totalQuestions }}题</span>
              </div>
            </div>
            <div class="questions-container">
              <div v-for="(question, index) in generatedHomework.questions" :key="index" class="preview-question">
                <div class="question-title">
                  <span class="q-number">{{ index + 1 }}.</span>
                  <span class="q-type">[{{ question.type }}]</span>
                  <span class="q-score">({{ question.score }}分)</span>
                </div>
                <div class="question-text">{{ question.content }}</div>
                <div v-if="question.options" class="question-choices">
                  <div v-for="(option, optIndex) in question.options" :key="optIndex" class="choice">
                    {{ String.fromCharCode(65 + optIndex) }}. {{ option }}
                  </div>
                </div>
                <div class="answer-space"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="printHomework" class="print-btn">打印作业</button>
          <button @click="showPreviewModal = false" class="cancel-btn">关闭</button>
        </div>
      </div>
    </div>

    <!-- 编辑模态框 -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content edit-modal" @click.stop>
        <div class="modal-header">
          <h3>编辑作业</h3>
          <button @click="showEditModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="edit-form">
            <div class="form-group">
              <label>作业标题</label>
              <input v-model="editingHomework.title" type="text" class="form-input">
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>学科</label>
                <input v-model="editingHomework.subject" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label>年级</label>
                <input v-model="editingHomework.grade" type="text" class="form-input">
              </div>
            </div>
            <div class="form-group">
              <label>预计用时（分钟）</label>
              <input v-model.number="editingHomework.estimatedTime" type="number" class="form-input">
            </div>
            <div class="form-group">
              <label>作业描述</label>
              <textarea v-model="editingHomework.description" class="form-textarea" rows="3"></textarea>
            </div>
          </div>
          <div class="questions-edit">
            <h4>题目编辑</h4>
            <div v-for="(question, index) in editingHomework.questions" :key="index" class="edit-question">
              <div class="question-header">
                <span class="question-num">第{{ index + 1 }}题</span>
                <span class="question-type">{{ question.type }}</span>
                <button @click="deleteQuestion(index)" class="delete-question-btn">删除</button>
              </div>
              <div class="question-edit-content">
                <div class="form-group">
                  <label>题目内容</label>
                  <textarea 
                    :value="question.content" 
                    @input="updateQuestionText(index, $event.target.value)"
                    class="form-textarea" 
                    rows="2"
                  ></textarea>
                </div>
                <div v-if="question.options" class="options-edit">
                  <label>选项</label>
                  <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option-edit">
                    <span class="option-label">{{ String.fromCharCode(65 + optIndex) }}.</span>
                    <input 
                      :value="option" 
                      @input="updateQuestionOption(index, optIndex, $event.target.value)"
                      type="text" 
                      class="option-input"
                    >
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>答案</label>
                    <input 
                      :value="question.answer" 
                      @input="updateQuestionAnswer(index, $event.target.value)"
                      type="text" 
                      class="form-input"
                    >
                  </div>
                  <div class="form-group">
                    <label>分值</label>
                    <input 
                      :value="question.score" 
                      @input="updateQuestionScore(index, $event.target.value)"
                      type="number" 
                      class="form-input"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="saveHomeworkChanges" class="save-btn">保存修改</button>
          <button @click="showEditModal = false" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>

    <!-- 查看全部题目模态框 -->
    <div v-if="showAllQuestionsModal" class="modal-overlay" @click="showAllQuestionsModal = false">
      <div class="modal-content all-questions-modal" @click.stop>
        <div class="modal-header">
          <h3>全部题目 ({{ generatedHomework.totalQuestions }}题)</h3>
          <button @click="showAllQuestionsModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="all-questions-list">
            <div v-for="(question, index) in generatedHomework.questions" :key="index" class="full-question-item">
              <div class="question-header">
                <span class="question-number">{{ index + 1 }}.</span>
                <span class="question-type">{{ question.type }}</span>
                <span class="question-score">{{ question.score }}分</span>
              </div>
              <div class="question-content">{{ question.content }}</div>
              <div v-if="question.options" class="question-options">
                <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option">
                  {{ String.fromCharCode(65 + optIndex) }}. {{ option }}
                </div>
              </div>
              <div v-if="question.answer" class="question-answer">
                <strong>答案：</strong>{{ question.answer }}
              </div>
              <div v-if="question.explanation" class="question-explanation">
                <strong>解析：</strong>{{ question.explanation }}
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAllQuestionsModal = false" class="close-btn">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Homework',
  data() {
    return {
      // 作业配置
      homeworkConfig: {
        title: '',
        subject: '',
        grade: '',
        knowledgePoints: '',
        includeAnswers: true,
        includeExplanations: false,
        randomOrder: false,
        multipleVersions: false,
        aiModel: 'gpt-4'
      },
      
      // 题型配置
      questionTypes: [
        {
          id: 1,
          name: '选择题',
          icon: '📝',
          enabled: false,
          count: 5,
          score: 4
        },
        {
          id: 2,
          name: '填空题',
          icon: '✏️',
          enabled: false,
          count: 5,
          score: 3
        },
        {
          id: 3,
          name: '判断题',
          icon: '✅',
          enabled: false,
          count: 5,
          score: 2
        },
        {
          id: 4,
          name: '简答题',
          icon: '📄',
          enabled: false,
          count: 3,
          score: 8
        },
        {
          id: 5,
          name: '计算题',
          icon: '🔢',
          enabled: false,
          count: 3,
          score: 10
        },
        {
          id: 6,
          name: '应用题',
          icon: '🧮',
          enabled: false,
          count: 2,
          score: 15
        }
      ],
      
      // 难度分布
      difficultyDistribution: {
        easy: 40,
        medium: 40,
        hard: 20
      },
      
      // 生成状态
      isGenerating: false,
      progress: 0,
      progressText: '',
      
      // 生成结果
      generatedHomework: null,
      
      // 模态框状态
      showPreviewModal: false,
      showEditModal: false,
      showAllQuestionsModal: false,
      
      // 编辑数据
      editingHomework: null
    }
  },
  
  computed: {
    canGenerate() {
      return this.homeworkConfig.title && 
             this.homeworkConfig.subject && 
             this.homeworkConfig.grade &&
             this.questionTypes.some(type => type.enabled);
    },
    
    totalQuestions() {
      return this.questionTypes
        .filter(type => type.enabled)
        .reduce((total, type) => total + type.count, 0);
    }
  },
  
  methods: {
    // 切换题型启用状态
    toggleQuestionType(type) {
      type.enabled = !type.enabled;
    },
    
    // 调整难度分布
    adjustDifficulty(changedType) {
      const total = 100;
      const current = this.difficultyDistribution;
      const changed = parseInt(current[changedType]);
      
      if (changed > total) {
        current[changedType] = total;
        return;
      }
      
      const remaining = total - changed;
      const otherTypes = Object.keys(current).filter(key => key !== changedType);
      
      if (otherTypes.length === 2) {
        const [type1, type2] = otherTypes;
        const ratio = current[type1] / (current[type1] + current[type2]) || 0.5;
        current[type1] = Math.round(remaining * ratio);
        current[type2] = remaining - current[type1];
      }
    },
    
    // 生成作业
    async generateHomework() {
      if (!this.canGenerate) return;
      this.isGenerating = true;
      this.progress = 0;
      this.progressText = '正在请求后端生成作业...';
      try {
        const config = {
          ...this.homeworkConfig,
          questionTypes: this.questionTypes.filter(t => t.enabled).map(t => ({
            name: t.name,
            count: t.count,
            score: t.score
          })),
          difficultyDistribution: { ...this.difficultyDistribution }
        };
        const result = await generateHomework(config);
        this.generatedHomework = result;
      } catch (error) {
        this.$message ? this.$message.error('作业生成失败，请稍后重试') : alert('作业生成失败，请稍后重试');
      } finally {
        this.isGenerating = false;
        this.progress = 100;
        this.progressText = '生成完成';
      }
    },
    
    // 模拟生成过程
    async simulateGeneration() {
      const steps = [
        { text: '分析作业需求...', duration: 800 },
        { text: '匹配知识点...', duration: 1000 },
        { text: '生成题目内容...', duration: 1500 },
        { text: '调整难度分布...', duration: 800 },
        { text: '完善答案解析...', duration: 700 }
      ];
      
      for (let i = 0; i < steps.length; i++) {
        this.progressText = steps[i].text;
        this.progress = ((i + 1) / steps.length) * 100;
        await new Promise(resolve => setTimeout(resolve, steps[i].duration));
      }
    },
    
    // 计算预计用时
    calculateEstimatedTime() {
      let time = 0;
      this.questionTypes.forEach(type => {
        if (type.enabled) {
          const timePerQuestion = {
            '选择题': 2,
            '填空题': 3,
            '判断题': 1,
            '简答题': 8,
            '计算题': 10,
            '应用题': 15
          }[type.name] || 5;
          time += type.count * timePerQuestion;
        }
      });
      return Math.max(time, 10);
    },
    
    // 生成描述
    generateDescription() {
      const enabledTypes = this.questionTypes
        .filter(type => type.enabled)
        .map(type => `${type.name}${type.count}题`)
        .join('、');
      
      return `本次作业包含${enabledTypes}，涵盖${this.homeworkConfig.knowledgePoints || '相关知识点'}，预计用时${this.calculateEstimatedTime()}分钟。`;
    },
    
    // 生成模拟题目
    generateMockQuestions() {
      const questions = [];
      
      this.questionTypes.forEach(type => {
        if (type.enabled) {
          for (let i = 0; i < type.count; i++) {
            questions.push(this.generateMockQuestion(type));
          }
        }
      });
      
      return questions;
    },
    
    // 生成单个模拟题目
    generateMockQuestion(type) {
      const templates = {
        '选择题': {
          content: `关于${this.homeworkConfig.knowledgePoints || '相关知识点'}的问题，下列说法正确的是？`,
          options: ['选项A的内容', '选项B的内容', '选项C的内容', '选项D的内容'],
          answer: 'A'
        },
        '填空题': {
          content: `请填写关于${this.homeworkConfig.knowledgePoints || '相关知识点'}的空白处：______。`,
          answer: '正确答案'
        },
        '判断题': {
          content: `${this.homeworkConfig.knowledgePoints || '相关知识点'}的相关表述是正确的。`,
          answer: '正确'
        },
        '简答题': {
          content: `请简要说明${this.homeworkConfig.knowledgePoints || '相关知识点'}的基本概念和应用。`,
          answer: '参考答案：...'
        },
        '计算题': {
          content: `根据${this.homeworkConfig.knowledgePoints || '相关知识点'}，计算下列问题的结果。`,
          answer: '计算过程和答案'
        },
        '应用题': {
          content: `结合实际情况，运用${this.homeworkConfig.knowledgePoints || '相关知识点'}解决以下问题。`,
          answer: '解题思路和答案'
        }
      };
      
      const template = templates[type.name];
      const question = {
        type: type.name,
        content: template.content,
        score: type.score,
        answer: template.answer
      };
      
      if (template.options) {
        question.options = template.options;
      }
      
      if (this.homeworkConfig.includeExplanations) {
        question.explanation = `这道${type.name}主要考查${this.homeworkConfig.knowledgePoints || '相关知识点'}理解与应用。`;
      }
      
      return question;
    },
    
    // 重置配置
    resetConfig() {
      this.homeworkConfig = {
        title: '',
        subject: '',
        grade: '',
        knowledgePoints: '',
        includeAnswers: true,
        includeExplanations: false,
        randomOrder: false,
        multipleVersions: false,
        aiModel: 'gpt-4'
      };
      
      this.questionTypes.forEach(type => {
        type.enabled = false;
      });
      
      this.difficultyDistribution = {
        easy: 40,
        medium: 40,
        hard: 20
      };
      
      this.generatedHomework = null;
    },
    
    // 预览作业
    previewHomework() {
      this.showPreviewModal = true;
    },
    
    // 下载作业
    downloadHomework() {
      // 创建下载内容
      let content = `${this.generatedHomework.title}\n\n`;
      content += `学科：${this.generatedHomework.subject}\n`;
      content += `年级：${this.generatedHomework.grade}\n`;
      content += `预计用时：${this.generatedHomework.estimatedTime}分钟\n`;
      content += `题目总数：${this.generatedHomework.totalQuestions}题\n\n`;
      
      this.generatedHomework.questions.forEach((question, index) => {
        content += `${index + 1}. [${question.type}] (${question.score}分)\n`;
        content += `${question.content}\n`;
        
        if (question.options) {
          question.options.forEach((option, optIndex) => {
            content += `${String.fromCharCode(65 + optIndex)}. ${option}\n`;
          });
        }
        
        if (this.homeworkConfig.includeAnswers) {
          content += `答案：${question.answer}\n`;
        }
        
        if (question.explanation) {
          content += `解析：${question.explanation}\n`;
        }
        
        content += '\n';
      });
      
      // 创建下载链接
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${this.generatedHomework.title}.txt`;
      link.click();
      URL.revokeObjectURL(url);
    },
    
    // 编辑作业
    editHomework() {
      this.editingHomework = JSON.parse(JSON.stringify(this.generatedHomework));
      this.showEditModal = true;
    },
    
    // 分享作业
    shareHomework() {
      alert('分享功能开发中...');
    },
    
    // 新建作业
    newHomework() {
      this.resetConfig();
    },
    
    // 打印作业
    printHomework() {
      window.print();
    },
    
    // 查看全部题目
    viewAllQuestions() {
      this.showAllQuestionsModal = true;
    },
    
    // 编辑功能
    updateQuestionScore(index, value) {
      this.editingHomework.questions[index].score = parseInt(value) || 0;
    },
    
    updateQuestionText(index, value) {
      this.editingHomework.questions[index].content = value;
    },
    
    updateQuestionOption(questionIndex, optionIndex, value) {
      this.editingHomework.questions[questionIndex].options[optionIndex] = value;
    },
    
    updateQuestionAnswer(index, value) {
      this.editingHomework.questions[index].answer = value;
    },
    
    deleteQuestion(index) {
      this.editingHomework.questions.splice(index, 1);
      this.editingHomework.totalQuestions = this.editingHomework.questions.length;
    },
    
    saveHomeworkChanges() {
      this.generatedHomework = JSON.parse(JSON.stringify(this.editingHomework));
      this.showEditModal = false;
      alert('修改已保存！');
    }
  }
}
</script>

<style scoped>
/* 页面整体样式 */
.homework-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 10px 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

/* 主要内容区域 */
.main-content {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 配置区域 */
.config-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e1e8ed;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #3498db;
}

/* 表单样式 */
.form-group {
  margin-bottom: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: #34495e;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

/* 题型配置 */
.question-types {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.type-card {
  border: 2px solid #e1e8ed;
  border-radius: 10px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafbfc;
}

.type-card:hover {
  border-color: #3498db;
  background: #f8f9ff;
}

.type-card.active {
  border-color: #3498db;
  background: #e8f4fd;
}

.type-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.type-icon {
  font-size: 1.2rem;
  margin-right: 8px;
}

.type-name {
  font-weight: 500;
  color: #2c3e50;
  flex: 1;
}

.type-toggle {
  width: 20px;
  height: 20px;
  border: 2px solid #bdc3c7;
  border-radius: 50%;
  position: relative;
  transition: all 0.3s ease;
}

.type-toggle.active {
  background: #3498db;
  border-color: #3498db;
}

.type-toggle.active::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.type-config {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e1e8ed;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.config-item {
  display: flex;
  flex-direction: column;
}

.config-item label {
  font-size: 0.8rem;
  color: #7f8c8d;
  margin-bottom: 4px;
}

.config-item input {
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

/* 难度分布 */
.difficulty-sliders {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.slider-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.slider-group label {
  font-weight: 500;
  color: #34495e;
  font-size: 0.9rem;
}

.difficulty-slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  outline: none;
  cursor: pointer;
}

.difficulty-slider.easy {
  background: linear-gradient(to right, #2ecc71, #27ae60);
}

.difficulty-slider.medium {
  background: linear-gradient(to right, #f39c12, #e67e22);
}

.difficulty-slider.hard {
  background: linear-gradient(to right, #e74c3c, #c0392b);
}

/* 高级选项 */
.advanced-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.9rem;
  color: #34495e;
}

.checkbox-label input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #bdc3c7;
  border-radius: 4px;
  margin-right: 10px;
  position: relative;
  transition: all 0.3s ease;
}

.checkbox-label input[type="checkbox"]:checked + .checkmark {
  background: #3498db;
  border-color: #3498db;
}

.checkbox-label input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 12px;
}

.generate-btn {
  flex: 1;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.generate-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #2980b9, #1f5f8b);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.generate-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.reset-btn {
  background: #ecf0f1;
  color: #7f8c8d;
  border: 2px solid #bdc3c7;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  background: #d5dbdb;
  border-color: #95a5a6;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 结果区域 */
.result-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 进度卡片 */
.progress-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e1e8ed;
}

.progress-card h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0;
}

/* 作业结果 */
.homework-result {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e1e8ed;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e1e8ed;
}

.result-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.result-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.action-btn.preview {
  background: #3498db;
  color: white;
}

.action-btn.download {
  background: #2ecc71;
  color: white;
}

.action-btn.edit {
  background: #f39c12;
  color: white;
}

.action-btn.share {
  background: #9b59b6;
  color: white;
}

.action-btn.new {
  background: #e74c3c;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* 作业卡片 */
.homework-card {
  border: 1px solid #e1e8ed;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
}

.homework-thumbnail {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
}

.thumbnail-content h4 {
  margin: 0 0 8px 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.thumbnail-content p {
  margin: 0;
  opacity: 0.9;
  font-size: 0.9rem;
}

.homework-details {
  padding: 16px 20px;
  background: #f8f9fa;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item .label {
  font-size: 0.8rem;
  color: #7f8c8d;
  font-weight: 500;
}

.detail-item .value {
  font-size: 0.9rem;
  color: #2c3e50;
  font-weight: 600;
}

.homework-meta {
  padding: 12px 20px;
  background: #ecf0f1;
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #7f8c8d;
}

.homework-description {
  padding: 16px 20px;
  background: white;
}

.homework-description p {
  margin: 0;
  color: #34495e;
  line-height: 1.5;
  font-size: 0.9rem;
}

/* 题目预览 */
.questions-preview h4 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.question-item {
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  padding: 16px;
  background: #fafbfc;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.question-number {
  font-weight: 600;
  color: #2c3e50;
}

.question-type {
  background: #3498db;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.question-score {
  background: #2ecc71;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-left: auto;
}

.question-content {
  color: #34495e;
  line-height: 1.5;
  margin-bottom: 12px;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.option {
  color: #7f8c8d;
  font-size: 0.9rem;
  padding-left: 16px;
}

.view-all-btn {
  width: 100%;
  background: #ecf0f1;
  color: #34495e;
  border: 2px solid #bdc3c7;
  padding: 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-all-btn:hover {
  background: #d5dbdb;
  border-color: #95a5a6;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin: 0 0 12px 0;
  color: #34495e;
  font-size: 1.3rem;
}

.empty-state p {
  margin: 0;
  font-size: 1rem;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.preview-modal {
  width: 800px;
}

.edit-modal {
  width: 900px;
}

.all-questions-modal {
  width: 700px;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e1e8ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #e74c3c;
  color: white;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e1e8ed;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: #f8f9fa;
}

/* 预览模态框特定样式 */
.homework-preview {
  font-family: 'Times New Roman', serif;
}

.homework-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #2c3e50;
}

.homework-header h2 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.homework-info {
  display: flex;
  justify-content: space-around;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.preview-question {
  margin-bottom: 24px;
  page-break-inside: avoid;
}

.question-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 600;
}

.q-number {
  color: #2c3e50;
}

.q-type {
  color: #3498db;
  font-size: 0.8rem;
}

.q-score {
  color: #2ecc71;
  font-size: 0.8rem;
  margin-left: auto;
}

.question-text {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #2c3e50;
}

.question-choices {
  margin-bottom: 16px;
}

.choice {
  margin-bottom: 4px;
  color: #34495e;
}

.answer-space {
  height: 40px;
  border-bottom: 1px solid #bdc3c7;
  margin-bottom: 8px;
}

.print-btn, .save-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.cancel-btn {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

/* 编辑模态框特定样式 */
.edit-form {
  margin-bottom: 24px;
}

.questions-edit h4 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  padding-bottom: 8px;
  border-bottom: 1px solid #e1e8ed;
}

.edit-question {
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  margin-bottom: 16px;
  overflow: hidden;
}

.edit-question .question-header {
  background: #f8f9fa;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-num {
  font-weight: 600;
  color: #2c3e50;
}

.delete-question-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
}

.question-edit-content {
  padding: 16px;
}

.options-edit {
  margin-bottom: 16px;
}

.option-edit {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.option-label {
  font-weight: 600;
  color: #2c3e50;
  min-width: 20px;
}

.option-input {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* 查看全部题目模态框 */
.all-questions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.full-question-item {
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  padding: 16px;
  background: #fafbfc;
}

.question-answer {
  margin-top: 12px;
  padding: 8px 12px;
  background: #e8f5e8;
  border-radius: 6px;
  font-size: 0.9rem;
}

.question-explanation {
  margin-top: 8px;
  padding: 8px 12px;
  background: #fff3cd;
  border-radius: 6px;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 350px 1fr;
  }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .homework-details {
    grid-template-columns: 1fr;
  }
  
  .homework-info {
    flex-direction: column;
    gap: 8px;
  }
  
  .result-actions {
    flex-wrap: wrap;
  }
  
  .modal-content {
    max-width: 95vw;
    margin: 10px;
  }
}

@media print {
  .modal-overlay {
    position: static;
    background: none;
  }
  
  .modal-content {
    box-shadow: none;
    max-width: none;
    max-height: none;
  }
  
  .modal-header, .modal-footer {
    display: none;
  }
  
  .homework-preview {
    font-size: 12pt;
    line-height: 1.5;
  }
}
</style>