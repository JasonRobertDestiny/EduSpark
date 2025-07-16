<template>
  <div class="learning-analysis-container">
    <div class="analysis-content">
      <h1 class="title">学情分析</h1>
      <p class="desc">在这里，您可以查看和分析学生的学习情况。</p>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-else>
        <div v-if="!analysisData">
          <div class="upload-section" :class="{ 'drag-over': isDragOver }" @dragover.prevent="onDragOver" @dragleave.prevent="onDragLeave" @drop.prevent="onDrop">
            <input ref="fileInput" type="file" accept=".xls,.xlsx,.csv" style="display:none" @change="onFileChange" />
            <div v-if="!selectedFile" class="upload-placeholder" @click="triggerFileInput">
              <svg class="upload-icon" viewBox="0 0 24 24"><path fill="#409EFF" d="M5 20h14a1 1 0 0 0 1-1v-2a1 1 0 1 0-2 0v1H6v-1a1 1 0 1 0-2 0v2a1 1 0 0 0 1 1zm7-2a1 1 0 0 0 1-1V8.41l2.3 2.3a1 1 0 1 0 1.4-1.42l-4-4a1 1 0 0 0-1.4 0l-4 4a1 1 0 1 0 1.4 1.42L11 8.41V17a1 1 0 0 0 1 1z"/></svg>
              <div class="upload-text">点击或拖拽上传成绩单（支持xlsx/csv）</div>
            </div>
            <div v-else class="file-preview">
              <span class="file-name">{{ selectedFile.name }}</span>
              <button class="remove-btn" @click="removeFile">移除</button>
            </div>
          </div>
          <button class="analyze-btn" :disabled="!selectedFile || isAnalyzing" @click="startAnalysis">
            {{ isAnalyzing ? '分析中...' : '上传并分析' }}
          </button>
        </div>
        <div v-else class="report-section">
          <!-- 分析报告内容 -->
          <div class="report-header">
            <span class="report-title">分析报告</span>
            <button class="reset-btn" @click="resetAnalysis">重新上传</button>
          </div>
          <div class="report-body">
            <div class="report-row">
              <span>平均分：</span><span class="report-value">{{ analysisData.avgScore }}</span>
            </div>
            <div class="report-row">
              <span>及格率：</span><span class="report-value">{{ analysisData.passRate }}%</span>
            </div>
            <div class="report-row">
              <span>分数分布：</span>
              <span class="report-value">{{ analysisData.scoreDist }}</span>
            </div>
            <div class="report-row">
              <span>薄弱学科：</span>
              <span class="report-value">{{ analysisData.weakSubjects }}</span>
            </div>
            <div class="report-row">
              <span>优势学科：</span>
              <span class="report-value">{{ analysisData.strongSubjects }}</span>
            </div>
            <div class="report-row">
              <span>学习建议：</span>
              <span class="report-value">{{ analysisData.suggestion }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getLearningAnalysis } from '@/services/api';

export default {
  name: 'LearningAnalysis',
  data() {
    return {
      analysisData: null,
      loading: false,
      error: '',
      selectedFile: null,
      isDragOver: false,
      isAnalyzing: false
    };
  },
  // 移除 mounted() { this.fetchAnalysis(); },
  methods: {
    // 移除 fetchAnalysis 方法
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.selectedFile = files[0];
      }
    },
    onDragOver() {
      this.isDragOver = true;
    },
    onDragLeave() {
      this.isDragOver = false;
    },
    onDrop(event) {
      this.isDragOver = false;
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.selectedFile = files[0];
      }
    },
    removeFile() {
      this.selectedFile = null;
      this.$refs.fileInput.value = '';
    },
    async startAnalysis() {
      this.isAnalyzing = true;
      this.analysisData = null;
      this.error = '';
      // 这里应调用后端上传和分析接口，暂用模拟数据
      setTimeout(() => {
        this.analysisData = {
          averageScore: 83,
          passRate: 92,
          maxScore: 100,
          minScore: 56,
          scoreDistribution: {
            '90-100': 12,
            '80-89': 18,
            '70-79': 9,
            '60-69': 6,
            '0-59': 3
          },
          weakPoints: ['历史', '地理', '语文作文'],
          summary: '整体成绩表现良好，理科优势明显，文科需加强。',
          subjects: [
            { name: '数学', score: 95 },
            { name: '物理', score: 92 },
            { name: '化学', score: 85 },
            { name: '语文', score: 78 },
            { name: '英语', score: 80 },
            { name: '历史', score: 65 },
            { name: '地理', score: 70 }
          ],
          strengths: [
            '数学、物理基础扎实，逻辑思维能力强。',
            '化学实验原理掌握良好。'
          ],
          weaknesses: [
            '历史知识体系不完整。',
            '地理读图能力有待加强。',
            '语文作文结构有待优化。'
          ],
          recommendations: [
            '建议制作历史事件时间轴，加强记忆。',
            '多做地理图表分析题，提升读图和分析能力。',
            '阅读优秀范文，学习作文的谋篇布局。',
            '针对薄弱科目，制定专项复习计划。'
          ]
        };
        this.isAnalyzing = false;
      }, 2500);
    }
  }
};
</script>

<style scoped>
.learning-analysis-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f0ff 0%, #b3d8ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.analysis-content {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 4px 32px 0 rgba(64,158,255,0.10);
  padding: 40px 36px 32px 36px;
  width: 420px;
  max-width: 90vw;
  min-width: 320px;
  margin: 48px 0 32px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title {
  color: #2176ff;
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: 1px;
}
.desc {
  color: #4a90e2;
  font-size: 1.1rem;
  margin-bottom: 24px;
}
.upload-section {
  border: 2px dashed #90c2ff;
  border-radius: 14px;
  background: #f7fbff;
  padding: 36px 0 28px 0;
  width: 100%;
  text-align: center;
  margin-bottom: 18px;
  transition: border-color 0.2s, background 0.2s;
}
.upload-section.drag-over {
  border-color: #2176ff;
  background: #e3f0ff;
}
.upload-placeholder {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.upload-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 10px;
}
.upload-text {
  color: #2176ff;
  font-size: 1.1rem;
}
.file-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
.file-name {
  color: #2176ff;
  font-weight: 500;
}
.remove-btn {
  background: #e3f0ff;
  color: #2176ff;
  border: none;
  border-radius: 6px;
  padding: 4px 12px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.remove-btn:hover {
  background: #b3d8ff;
}
.analyze-btn {
  background: linear-gradient(90deg, #409eff 0%, #2176ff 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 0;
  width: 100%;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 8px;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 2px 8px 0 rgba(64,158,255,0.08);
}
.analyze-btn:disabled {
  background: #b3d8ff;
  cursor: not-allowed;
}
.error {
  color: #ff4d4f;
  font-size: 1.1rem;
  margin-bottom: 18px;
  text-align: center;
}
.report-section {
  width: 100%;
  margin-top: 8px;
  background: #f7fbff;
  border-radius: 14px;
  box-shadow: 0 2px 8px 0 rgba(64,158,255,0.06);
  padding: 24px 18px 18px 18px;
}
.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.report-title {
  color: #2176ff;
  font-size: 1.2rem;
  font-weight: 600;
}
.reset-btn {
  background: #e3f0ff;
  color: #2176ff;
  border: none;
  border-radius: 6px;
  padding: 4px 12px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.reset-btn:hover {
  background: #b3d8ff;
}
.report-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.report-row {
  display: flex;
  justify-content: space-between;
  color: #2176ff;
  font-size: 1.05rem;
}
.report-value {
  font-weight: 600;
  color: #409eff;
}
</style>