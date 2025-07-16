<template>
  <div class="qa-container">
    <!-- 左侧功能区 -->
    <aside class="sidebar">
      <div class="logo">多模态生成</div>
      <nav>
        <ul>
          <li v-for="tool in tools" :key="tool.key" :class="{active: activeTool === tool.key}" @click="selectTool(tool.key)">
            <span>{{ tool.title }}</span>
          </li>
        </ul>
      </nav>
    </aside>
    
    <!-- 右侧对话区 -->
    <div class="chat-content">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <h1 class="chat-title">{{ getCurrentToolTitle() }}</h1>
        <button @click="clearConversation" class="clear-btn">清空对话</button>
      </div>

      <!-- 对话区域 -->
      <div class="chat-area">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-icon">🤖</div>
          <h3>欢迎使用{{ getCurrentToolTitle() }}</h3>
          <p>我是您的AI助手，可以帮您处理文本、图片等多种类型的内容。请开始对话吧！</p>
        </div>
        
        <!-- 对话历史 -->
        <div class="messages-container" ref="messagesContainer">
          <div v-for="(message, index) in messages" :key="index" class="message" :class="message.type">
            <div class="message-content">
              <div v-if="message.type === 'user'" class="user-message">
                <div class="message-text">{{ message.text }}</div>
                <!-- 用户上传的文件 -->
                <div v-if="message.files && message.files.length > 0" class="message-files">
                  <div v-for="file in message.files" :key="file.name" class="file-tag">
                    📄 {{ file.name }}
                  </div>
                </div>
                <!-- 用户上传的图片 -->
                <div v-if="message.images && message.images.length > 0" class="message-images">
                  <img v-for="image in message.images" :key="image.name" :src="image.url" :alt="image.name" class="message-image">
                </div>
              </div>
              <div v-else class="ai-message">
                <div class="ai-avatar">🤖</div>
                <div class="message-text">{{ message.text }}</div>
              </div>
            </div>
          </div>
          
          <!-- 加载中消息 -->
          <div v-if="isLoading" class="message ai">
            <div class="message-content">
              <div class="ai-message">
                <div class="ai-avatar">🤖</div>
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="input-area">
        <!-- 文件预览区域 -->
        <div v-if="uploadedFiles.length > 0 || uploadedImages.length > 0" class="preview-area">
          <!-- 文件预览 -->
          <div v-if="uploadedFiles.length > 0" class="file-previews">
            <div v-for="(file, index) in uploadedFiles" :key="index" class="file-preview">
              <span class="file-icon">📄</span>
              <span class="file-name">{{ file.name }}</span>
              <button @click="removeFile(index)" class="remove-btn">×</button>
            </div>
          </div>
          <!-- 图片预览 -->
          <div v-if="uploadedImages.length > 0" class="image-previews">
            <div v-for="(image, index) in uploadedImages" :key="index" class="image-preview">
              <img :src="image.url" :alt="image.name" class="preview-img">
              <button @click="removeImage(index)" class="remove-btn">×</button>
            </div>
          </div>
        </div>
        
        <!-- 输入框和按钮 -->
        <div class="input-container">
          <div class="input-wrapper">
            <!-- 上传按钮 -->
            <div class="upload-buttons">
              <button @click="triggerFileUpload" class="upload-btn" title="上传文件">
                📎
              </button>
              <button @click="triggerImageUpload" class="upload-btn" title="上传图片">
                🖼️
              </button>
            </div>
            
            <!-- 文本输入 -->
            <textarea 
              v-model="questionText" 
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.enter.shift.exact="questionText += '\n'"
              placeholder="输入消息... (Enter发送，Shift+Enter换行)"
              class="message-input"
              rows="1"
              ref="messageInput"
            ></textarea>
            
            <!-- 发送按钮 -->
            <button 
              @click="sendMessage" 
              :disabled="isLoading || !questionText.trim()"
              class="send-btn"
            >
              <span v-if="isLoading">⏳</span>
              <span v-else>🚀</span>
            </button>
          </div>
        </div>
        
        <!-- 隐藏的文件输入 -->
        <input 
          ref="fileInput" 
          type="file" 
          multiple 
          accept=".pdf,.doc,.docx,.txt,.xlsx,.xls"
          @change="handleFileSelect"
          style="display: none;"
        >
        <input 
          ref="imageInput" 
          type="file" 
          multiple 
          accept="image/*"
          @change="handleImageSelect"
          style="display: none;"
        >
      </div>
    </div>
  </div>
</template>

<script>
import { askMultimodalQA } from '@/services/api';
export default {
  name: 'QA',
  data() {
    return {
      questionText: '',
      uploadedFiles: [],
      uploadedImages: [],
      isLoading: false,
      messages: [],
      activeTool: 'qa',
      tools: [
        { key: 'qa', title: '多模态问答' },
        { key: 'text', title: '文本生成' },
        { key: 'image', title: '图像生成' },
        { key: 'video', title: '视频生成' },
        { key: 'audio', title: '音频生成' }
      ]
    }
  },
  methods: {
    selectTool(toolKey) {
      this.activeTool = toolKey;
    },
    
    getCurrentToolTitle() {
      const tool = this.tools.find(t => t.key === this.activeTool);
      return tool ? tool.title : '多模态问答';
    },
    
    clearConversation() {
      this.questionText = '';
      this.uploadedFiles = [];
      this.uploadedImages = [];
      this.messages = [];
    },
    
    sendMessage() {
      if (!this.questionText.trim() && this.uploadedFiles.length === 0 && this.uploadedImages.length === 0) {
        return;
      }
      const userMessage = {
        type: 'user',
        text: this.questionText,
        files: [...this.uploadedFiles],
        images: [...this.uploadedImages],
        timestamp: new Date()
      };
      this.messages.push(userMessage);
      const currentText = this.questionText;
      this.questionText = '';
      this.uploadedFiles = [];
      this.uploadedImages = [];
      this.isLoading = true;
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      askMultimodalQA({
        question: currentText,
        files: userMessage.files,
        images: userMessage.images
      })
        .then(res => {
          this.messages.push({
            type: 'ai',
            text: res.answer || 'AI未返回有效内容',
            timestamp: new Date()
          });
        })
        .catch(err => {
          this.messages.push({
            type: 'ai',
            text: 'AI服务异常，请稍后重试',
            timestamp: new Date()
          });
        })
        .finally(() => {
          this.isLoading = false;
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        });
    },
    
    generateAIResponse(text, files, images) {
      const responses = [
        `我理解您的问题："${text}"。让我为您分析一下...`,
        `根据您提供的信息，我认为这是一个很有趣的问题。`,
        `感谢您的提问！基于${this.getCurrentToolTitle()}的功能，我可以帮您处理这个请求。`,
        `这是一个很好的问题。让我从多个角度来分析...`,
        `我已经理解了您的需求，现在为您提供详细的回答...`
      ];
      
      let response = responses[Math.floor(Math.random() * responses.length)];
      
      if (files.length > 0) {
        response += `\n\n我注意到您上传了 ${files.length} 个文件，我会仔细分析其中的内容。`;
      }
      
      if (images.length > 0) {
        response += `\n\n您上传的 ${images.length} 张图片我也会进行详细的视觉分析。`;
      }
      
      return response;
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    
    // 文件上传相关方法
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    
    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      this.addFiles(files);
    },
    
    handleFileDrop(event) {
      event.preventDefault();
      const files = Array.from(event.dataTransfer.files);
      this.addFiles(files);
    },
    
    addFiles(files) {
      files.forEach(file => {
        if (this.isValidFile(file)) {
          this.uploadedFiles.push({
            name: file.name,
            file: file,
            size: this.formatFileSize(file.size)
          });
        }
      });
    },
    
    isValidFile(file) {
      const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
      return validTypes.includes(file.type);
    },
    
    removeFile(index) {
      this.uploadedFiles.splice(index, 1);
    },
    
    // 图片上传相关方法
    triggerImageUpload() {
      this.$refs.imageInput.click();
    },
    
    handleImageSelect(event) {
      const files = Array.from(event.target.files);
      this.addImages(files);
    },
    
    handleImageDrop(event) {
      event.preventDefault();
      const files = Array.from(event.dataTransfer.files);
      this.addImages(files);
    },
    
    addImages(files) {
      files.forEach(file => {
        if (file.type.startsWith('image/')) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.uploadedImages.push({
              name: file.name,
              file: file,
              url: e.target.result
            });
          };
          reader.readAsDataURL(file);
        }
      });
    },
    
    removeImage(index) {
      this.uploadedImages.splice(index, 1);
    },
    

    
    // 工具方法
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  }
}
</script>

<style scoped>
.qa-container {
  display: flex;
  height: 100vh;
  background: #f7f7f8;
  margin: 0;
  padding: 0;
}

.sidebar {
  width: 280px;
  background: #2c3e50;
  color: white;
  padding: 0;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  padding: 30px 20px;
  text-align: center;
  color: #3498db;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar nav {
  flex: 1;
  padding: 20px 0;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar nav li {
  padding: 15px 20px;
  margin: 0 10px 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.sidebar nav li:hover {
  background: rgba(52, 152, 219, 0.1);
  border-left-color: #3498db;
}

.sidebar nav li.active {
  background: rgba(52, 152, 219, 0.2);
  border-left-color: #3498db;
  color: #3498db;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  margin: 0;
  padding: 0;
}

.chat-header {
  padding: 20px 30px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  z-index: 10;
}

.chat-title {
  margin: 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.clear-btn {
  padding: 8px 16px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
  font-size: 14px;
}

.clear-btn:hover {
  background: #c0392b;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.welcome-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.welcome-message h3 {
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.welcome-message p {
  margin: 0;
  font-size: 16px;
  line-height: 1.5;
  max-width: 500px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

.message {
  margin-bottom: 20px;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.ai {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
}

.user-message {
  background: #3498db;
  color: white;
  padding: 12px 16px;
  border-radius: 18px 18px 4px 18px;
  word-wrap: break-word;
}

.ai-message {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.ai-avatar {
  width: 32px;
  height: 32px;
  background: #f0f0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.ai-message .message-text {
  background: #f1f3f4;
  color: #2c3e50;
  padding: 12px 16px;
  border-radius: 18px 18px 18px 4px;
  word-wrap: break-word;
  line-height: 1.5;
}

.message-files {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.file-tag {
  background: rgba(255,255,255,0.2);
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.message-images {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.message-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  object-fit: cover;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 16px;
  background: #f1f3f4;
  border-radius: 18px 18px 18px 4px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #bdc3c7;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.input-area {
  border-top: 1px solid #e0e0e0;
  background: white;
  padding: 0;
}

.preview-area {
  padding: 15px 20px 0 20px;
  border-bottom: 1px solid #f0f0f0;
}

.file-previews, .image-previews {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f9fa;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.file-icon {
  font-size: 16px;
}

.file-name {
  color: #2c3e50;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-preview {
  position: relative;
  display: inline-block;
}

.preview-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

.remove-btn {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: -5px;
  right: -5px;
}

.file-preview .remove-btn {
  position: static;
  margin-left: 5px;
}

.remove-btn:hover {
  background: #c0392b;
}

.input-container {
  padding: 20px;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: #f8f9fa;
  border-radius: 24px;
  padding: 8px;
  border: 1px solid #e0e0e0;
  transition: border-color 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: #3498db;
}

.upload-buttons {
  display: flex;
  gap: 5px;
  padding-left: 8px;
}

.upload-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}

.upload-btn:hover {
  background: rgba(52, 152, 219, 0.1);
}

.message-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  resize: none;
  font-size: 16px;
  line-height: 1.5;
  padding: 8px 12px;
  max-height: 120px;
  min-height: 20px;
  font-family: inherit;
}

.message-input::placeholder {
  color: #95a5a6;
}

.send-btn {
  background: #3498db;
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: background 0.3s ease;
  margin-right: 4px;
}

.send-btn:hover:not(:disabled) {
  background: #2980b9;
}

.send-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

/* 滚动条样式 */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .qa-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    flex-direction: row;
    overflow-x: auto;
  }
  
  .sidebar nav {
    display: flex;
    padding: 10px;
  }
  
  .sidebar nav ul {
    display: flex;
    gap: 10px;
  }
  
  .sidebar nav li {
    white-space: nowrap;
    margin: 0;
  }
  
  .message-content {
    max-width: 85%;
  }
}
</style>