<template>
  <div class="page-container">
    <header class="page-header">
      <h1>教材资源管理</h1>
      <p>智能生成和管理您的教学材料</p>
    </header>

    <div class="actions-bar">
      <button class="upload-btn" @click="triggerFileUpload">上传文件</button>
      <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none">
      <input type="text" v-model="searchTerm" @input="handleSearch" placeholder="搜索您的文件..." class="search-input">
    </div>

    <div v-if="isLoading" class="loading-indicator">正在加载...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

        <div v-if="!isLoading && !error" class="file-list">
      <!-- ... file list ... -->
    </div>

    <!-- 预览模态框 -->
    <div v-if="showPreview" class="preview-modal">
      <div class="preview-content">
        <span class="close-btn" @click="closePreview">&times;</span>
        <h3>{{ selectedFile.name }}</h3>
        <div v-if="selectedFile.type === 'image'">
          <img :src="selectedFile.url" alt="图片预览" class="preview-image" />
        </div>
        <div v-else-if="selectedFile.type === 'pdf'">
          <vue-pdf-embed :source="selectedFile.url" />
        </div>
        <div v-else-if="selectedFile.type === 'docx'">
          <div ref="docxContainer"></div>
        </div>
        <div v-else>
          <p>{{ selectedFile.content }}</p>
        </div>
      </div>
    </div>

    <div v-if="!isLoading && !error" class="file-list">
      <div v-if="files.length === 0" class="empty-state">没有找到文件。</div>
      <div class="file-item" v-for="file in files" :key="file.id">
        <div class="file-info">
          <span class="file-icon">📄</span>
          <span class="file-name">{{ file.name }}</span>
        </div>
        <div class="file-actions">
          <button class="action-btn" @click="previewFile(file)">预览</button>
          <button class="action-btn delete-btn" @click="handleDelete(file)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getFiles } from '../../services/api';
import VuePdfEmbed from 'vue-pdf-embed';
import { renderAsync } from 'docx-preview';

export default {
  name: 'TeachingMaterial',
  components: {
    VuePdfEmbed,
  },
  data() {
    return {
      files: [],
      searchTerm: '',
      isLoading: false,
      error: null,
      currentUserId: 'teacher1',
      showPreview: false,
      selectedFile: null,
    };
  },
  created() {
    this.fetchFiles();
  },
  methods: {
    fetchFiles() {
      this.isLoading = true;
      this.error = null;
      getFiles(this.currentUserId, this.searchTerm)
        .then(files => {
          this.files = files;
        })
        .catch(error => {
          this.error = '加载文件失败，请稍后重试。';
          console.error(error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    handleSearch() {
      this.fetchFiles();
    },
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      // 模拟文件上传
      const newFile = {
        id: Date.now(), // 使用时间戳作为唯一 ID
        name: file.name,
      };

      this.files.unshift(newFile); // 将新文件添加到列表顶部
      alert(`文件 "${file.name}" 已上传成功！`);
    },
    handleDelete(fileToDelete) {
      if (confirm(`确定要删除文件 "${fileToDelete.name}" 吗？`)) {
        this.files = this.files.filter(file => file.id !== fileToDelete.id);
        alert(`文件 "${fileToDelete.name}" 已被删除。`);
      }
    },
    handleDownload(file) {
      alert(`正在开始下载文件 "${file.name}" ...`);
    },
    handleShare(file) {
      alert(`文件 "${file.name}" 的分享链接已复制到剪贴板。`);
    },
        previewFile(file) {
      console.log('Attempting to preview file:', file);
      this.selectedFile = file;
      this.showPreview = true;

      if (file.type === 'docx') {
        this.$nextTick(() => {
          const docxContainer = this.$refs.docxContainer;
          if (docxContainer) {
            console.log(`Fetching DOCX from: ${file.url}`);
            fetch(file.url)
              .then(response => {
                if (!response.ok) {
                  throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.blob();
              })
              .then(blob => {
                console.log('DOCX blob received, rendering...');
                renderAsync(blob, docxContainer);
              })
              .catch(error => {
                console.error('Error fetching or rendering DOCX:', error);
                docxContainer.innerText = '预览加载失败，请检查文件是否存在于public文件夹，或查看控制台获取更多信息。';
              });
          }
        });
      } else if (file.type === 'pdf') {
        console.log(`Loading PDF from: ${file.url}`);
      }
    },
    closePreview() {
      this.showPreview = false;
      this.selectedFile = null;
    }
  },
};
</script>

<style scoped>
.page-container {
  padding: 40px;
  background-color: #f9f9f9;
  min-height: 100vh;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5em;
  color: #333;
}

.page-header p {
  color: #666;
}

.actions-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.upload-btn {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-input {
  padding: 10px;
  width: 300px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.file-list {
  background-color: white;
  border-radius: 5px;
  padding: 20px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.file-item:last-child {
  border-bottom: none;
}

.file-info {
  display: flex;
  align-items: center;
}

.file-icon {
  font-size: 1.5em;
  margin-right: 15px;
}

.action-btn {
  background: none;
  border: 1px solid #ccc;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.delete-btn {
  color: #f44336;
  border-color: #f44336;
}

.loading-indicator, .error-message, .empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error-message {
  color: #f44336;
}

/* 预览模态框样式 */
.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 600px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5em;
  cursor: pointer;
}

.preview-image {
  max-width: 100%;
  max-height: 70vh;
  display: block;
  margin: 0 auto;
}
</style>