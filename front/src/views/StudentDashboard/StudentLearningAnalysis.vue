<template>
  <div class="analysis-container">
    <header class="analysis-header">
      <h1>个人学情分析</h1>
      <p>上传您的成绩单或试卷，获取详细的学情分析报告。</p>
    </header>

    <div v-if="!analysisResult" class="upload-section">
      <div 
        class="drop-zone"
        @dragover.prevent="onDragOver"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
        :class="{ 'drag-over': isDragOver }"
        @click="triggerFileInput"
      >
        <input type="file" ref="fileInput" @change="onFileChange" style="display: none" accept=".pdf,.jpg,.png,.jpeg,.doc,.docx">
        <div v-if="!selectedFile" class="upload-placeholder">
          <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/></svg>
          <p>将文件拖拽到此处，或点击选择文件</p>
          <button class="upload-btn" @click.stop="triggerFileInput">选择文件</button>
          <small>支持 PDF, JPG, PNG, DOCX 等格式</small>
        </div>
        <div v-else class="file-preview">
          <p>已选择文件: {{ selectedFile.name }}</p>
          <button class="remove-file-btn" @click.stop="removeFile">移除</button>
        </div>
      </div>
      <button class="analyze-btn" @click="startAnalysis" :disabled="!selectedFile || isAnalyzing">
        <span v-if="isAnalyzing" class="spinner"></span>
        {{ isAnalyzing ? '分析中...' : '开始分析' }}
      </button>
    </div>

    <div v-if="isAnalyzing && !analysisResult" class="loading-section">
      <div class="spinner-large"></div>
      <p>正在为您生成学情报告，请稍候...</p>
    </div>

    <div v-if="analysisResult" class="results-section">
      <div class="results-header">
        <h2>学情分析报告</h2>
        <button class="re-upload-btn" @click="reset">重新上传分析</button>
      </div>
      
      <div class="summary-card">
        <h3>总体评估</h3>
        <p>{{ analysisResult.summary }}</p>
        <div class="overall-score">
          <strong>综合得分:</strong>
          <span>{{ analysisResult.overallScore }} / 100</span>
        </div>
      </div>

      <div class="details-grid">
        <div class="chart-card">
          <h3>各科表现</h3>
          <div class="bar-chart">
            <div class="bar-item" v-for="subject in analysisResult.subjects" :key="subject.name">
              <div class="bar-label">{{ subject.name }}</div>
              <div class="bar-wrapper">
                <div class="bar" :style="{ width: subject.score + '%', backgroundColor: getScoreColor(subject.score) }"></div>
              </div>
              <div class="bar-value">{{ subject.score }}</div>
            </div>
          </div>
        </div>

        <div class="strengths-card">
          <h3>优势分析</h3>
          <ul>
            <li v-for="strength in analysisResult.strengths" :key="strength">{{ strength }}</li>
          </ul>
        </div>

        <div class="weaknesses-card">
          <h3>待提高项</h3>
          <ul>
            <li v-for="weakness in analysisResult.weaknesses" :key="weakness">{{ weakness }}</li>
          </ul>
        </div>

        <div class="recommendations-card">
          <h3>学习建议</h3>
          <ul>
            <li v-for="rec in analysisResult.recommendations" :key="rec">{{ rec }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'StudentLearningAnalysis',
  data() {
    return {
      selectedFile: null,
      isDragOver: false,
      isAnalyzing: false,
      analysisResult: null,
      error: '',
    };
  },
  methods: {
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
      if (!this.selectedFile) return;
      this.isAnalyzing = true;
      this.analysisResult = null;
      this.error = '';
      try {
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        // 假设后端API为 /api/student-learning-analysis，返回结构与模拟数据一致
        const response = await axios.post('/api/student-learning-analysis', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.analysisResult = response.data;
      } catch (err) {
        this.error = '分析失败，请稍后重试';
      } finally {
        this.isAnalyzing = false;
      }
    },
    reset() {
      this.selectedFile = null;
      this.analysisResult = null;
      this.isAnalyzing = false;
      this.error = '';
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },
    getScoreColor(score) {
      if (score >= 90) return '#4CAF50'; // Green
      if (score >= 75) return '#8BC34A'; // Light Green
      if (score >= 60) return '#FFC107'; // Amber
      return '#F44336'; // Red
    }
  }
};
</script>

<style scoped>
.analysis-container {
  padding: 2rem;
  background-color: #f9fafb;
  height: 100%;
  overflow-y: auto;
}

.analysis-header {
  text-align: center;
  margin-bottom: 2rem;
}

.analysis-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
}

.analysis-header p {
  font-size: 1rem;
  color: #6b7280;
  margin-top: 0.5rem;
}

.upload-section {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.drop-zone {
  border: 2px dashed #d1d5db;
  border-radius: 0.75rem;
  padding: 2.5rem;
  background-color: #ffffff;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s;
}

.drop-zone.drag-over {
  background-color: #eff6ff;
  border-color: #3b82f6;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.upload-icon {
  width: 4rem;
  height: 4rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.upload-btn {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.upload-btn:hover {
  background-color: #2563eb;
}

.file-preview {
  font-weight: 500;
}

.remove-file-btn {
  margin-left: 1rem;
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
}

.analyze-btn {
  margin-top: 1.5rem;
  padding: 0.75rem 2rem;
  width: 100%;
  background-color: #16a34a;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1.125rem;
  font-weight: 600;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.analyze-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.analyze-btn:hover:not(:disabled) {
  background-color: #15803d;
}

.loading-section {
  text-align: center;
  padding: 4rem 0;
  color: #4b5563;
}

.spinner, .spinner-large {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}
.spinner {
  width: 1.2rem;
  height: 1.2rem;
}
.spinner-large {
  width: 3rem;
  height: 3rem;
  border-color: rgba(59, 130, 246, 0.2);
  border-top-color: #3b82f6;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.results-section {
  margin-top: 2rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.results-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
}

.re-upload-btn {
  padding: 0.5rem 1rem;
  background-color: #6b7280;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.re-upload-btn:hover {
  background-color: #4b5563;
}

.summary-card, .chart-card, .strengths-card, .weaknesses-card, .recommendations-card {
  background-color: #ffffff;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
}

.summary-card {
  margin-bottom: 1.5rem;
}

.summary-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.overall-score {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.125rem;
}

.overall-score span {
  font-weight: 700;
  color: #1d4ed8;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
}

@media (min-width: 1024px) {
  .details-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-template-areas:
      "chart strengths"
      "chart weaknesses"
      "recommendations recommendations";
  }
  .chart-card { grid-area: chart; }
  .strengths-card { grid-area: strengths; }
  .weaknesses-card { grid-area: weaknesses; }
  .recommendations-card { grid-area: recommendations; }
}

.details-grid h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.details-grid ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  color: #4b5563;
}

.details-grid li {
  margin-bottom: 0.5rem;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bar-label {
  width: 5rem;
  text-align: right;
  font-weight: 500;
  color: #374151;
}

.bar-wrapper {
  flex-grow: 1;
  background-color: #e5e7eb;
  border-radius: 0.25rem;
  overflow: hidden;
}

.bar {
  height: 1.5rem;
  border-radius: 0.25rem;
  transition: width 0.5s ease-out;
}

.bar-value {
  font-weight: 600;
  width: 2.5rem;
}
</style>