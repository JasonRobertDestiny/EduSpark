<template>
  <div class="syllabus-container">
    <!-- 新增课程编号输入和搜索区域 -->
    <div class="course-id-input">
      <label for="courseId">课程编号:</label>
      <input
        id="courseId"
        v-model="inputCourseId"
        type="text"
        placeholder="请输入课程编号"

        @keyup.enter="fetchSyllabus"
      />
      <button @click="fetchSyllabus" :disabled="!inputCourseId.trim()">搜索</button>
      <span v-if="courseIdError" class="error-message">{{ courseIdError }}</span>
    </div>

    <div class="syllabus-header">
      <h1>课程教学大纲</h1>
      <div class="syllabus-meta">
        <span>课程编号：{{ courseId }}</span>
        <span>课程名称：{{ courseName }}</span>
      </div>
    </div>

    <!-- 时间线展示区域 -->
    <div v-if="timeline.length && !loading && !error" class="timeline-container">
      <h2>教学时间线</h2>
      <div class="timeline">
        <div v-for="(item, index) in timeline" :key="index" class="timeline-item">
          <div class="timeline-point"></div>
          <div class="timeline-content">
            <h3>{{ item.name }}</h3>
            <p>课时分配: {{ item.hours }} 课时</p>
          </div>
        </div>
      </div>
    </div>

    <div class="syllabus-card">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error">{{ error }}</div>
      <!-- 使用树形结构展示大纲 -->
      <div v-if="syllabusTree.length && !loading && !error" class="tree-container">
        <ul class="tree">
          <li v-for="node in syllabusTree" :key="node.id">
            <div class="tree-node">
              <span @click="selectNode(node)">{{ node.name }}</span>
              <button @click="editNode(node)">编辑</button>
              <button @click="deleteNode(node.id)">删除</button>
            </div>
            <!-- 递归展示子节点 -->
            <ul v-if="node.children && node.children.length">
              <syllabus-tree-node
                :nodes="node.children"
                @edit="editNode"
                @delete="deleteNode"
                @select="selectNode"
              />
            </ul>
          </li>
        </ul>
      </div>
      <div v-else-if="!loading && !error" class="syllabus-empty">暂无教学大纲数据</div>
    </div>
    <!-- 添加新大纲项按钮 -->
    <button @click="showAddModal = true" class="add-button">添加新大纲项</button>

    <!-- 节点详情展示 -->
    <div v-if="selectedNode" class="node-details">
      <h3>节点详情</h3>
      <p>章节名称: {{ selectedNode.name }}</p>
      <p>课时分配: {{ selectedNode.hours }} 课时</p>
      <p>教学目标: {{ selectedNode.objective }}</p>
    </div>

    <!-- 添加/编辑模态框 -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showAddModal = false">&times;</span>
        <h2>{{ isEditing ? '编辑大纲项' : '添加新大纲项' }}</h2>
        <form @submit.prevent="submitSyllabusItem">
          <div>
            <label>章节名称:</label>
            <input v-model="newItem.name" type="text" required />
            <span v-if="newItemErrors.name" class="error-message">{{ newItemErrors.name }}</span>
          </div>
          <div>
            <label>课时分配:</label>
            <input v-model.number="newItem.hours" type="number" required min="1" />
            <span v-if="newItemErrors.hours" class="error-message">{{ newItemErrors.hours }}</span>
          </div>
          <div>
            <label>教学目标:</label>
            <input v-model="newItem.objective" type="text" required />
            <span v-if="newItemErrors.objective" class="error-message">{{ newItemErrors.objective }}</span>
          </div>
          <button type="submit">{{ isEditing ? '更新' : '添加' }}</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getSyllabus, addSyllabus, updateSyllabus, deleteSyllabus } from '@/services/api';

// 递归树形组件
const SyllabusTreeNode = {
  name: 'SyllabusTreeNode',
  props: ['nodes'],
  emits: ['edit', 'delete', 'select'],
  template: `
    <li v-for="node in nodes" :key="node.id">
      <div class="tree-node">
        <span @click="$emit('select', node)">{{ node.name }}</span>
        <button @click="$emit('edit', node)">编辑</button>
        <button @click="$emit('delete', node.id)">删除</button>
      </div>
      <ul v-if="node.children && node.children.length">
        <syllabus-tree-node
          :nodes="node.children"
          @edit="$emit('edit', $event)"
          @delete="$emit('delete', $event)"
          @select="$emit('select', $event)"
        />
      </ul>
    </li>
  `
};

export default {
  name: 'Syllabus',
  components: {
    SyllabusTreeNode
  },
  props: {
    courseId: {
      type: String,
      default: 'CS101'
    },
    courseName: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      syllabusTree: [],
      loading: false,
      error: '',
      showAddModal: false,
      isEditing: false,
      newItem: {
        name: '',
        hours: null,
        objective: ''
      },
      selectedNode: null,
      inputCourseId: '',
      timeline: [], // 新增时间线数据
      courseIdError: '',
      newItemErrors: {
        name: '',
        hours: '',
        objective: ''
      }
    };
  },
  created() {
    this.inputCourseId = this.courseId;
    this.fetchSyllabus();
  },
  methods: {
    validateCourseId() {
      if (!this.inputCourseId.trim()) {
        this.courseIdError = '请输入课程编号';
        return false;
      }
      this.courseIdError = '';
      return true;
    },
    validateNewItem() {
      this.newItemErrors = {
        name: '',
        hours: '',
        objective: ''
      };
      let isValid = true;
      if (!this.newItem.name.trim()) {
        this.newItemErrors.name = '请输入章节名称';
        isValid = false;
      }
      if (!this.newItem.hours || this.newItem.hours < 1) {
        this.newItemErrors.hours = '课时分配必须大于 0';
        isValid = false;
      }
      if (!this.newItem.objective.trim()) {
        this.newItemErrors.objective = '请输入教学目标';
        isValid = false;
      }
      return isValid;
    },
    async fetchSyllabus() {
      if (!this.validateCourseId()) return;
      this.loading = true;
      this.error = '';
      try {
        // 使用输入的课程编号获取数据
        const data = await getSyllabus(this.inputCourseId); 
        this.syllabusTree = this.transformToTree(data);
        this.generateTimeline(data); // 生成时间线数据
      } catch (error) {
        console.error('获取教学大纲失败:', error);
        this.error = error.message || '获取教学大纲失败，请稍后重试';
        this.syllabusTree = [];
        this.timeline = [];
      } finally {
        this.loading = false;
      }
    },
    transformToTree(data) {
      // 假设数据中有 parentId 字段，根节点的 parentId 为 null 或 0
      const tree = [];
      const map = {};

      data.forEach(item => {
        map[item.id] = { ...item, children: [] };
      });

      data.forEach(item => {
        if (item.parentId === null || item.parentId === 0) {
          tree.push(map[item.id]);
        } else {
          if (map[item.parentId]) {
            map[item.parentId].children.push(map[item.id]);
          }
        }
      });

      return tree;
    },
    generateTimeline(data) {
      // 简单实现：将数据平铺作为时间线节点
      // 实际可能需要根据数据结构调整
      this.timeline = data.map(item => ({
        name: item.name,
        hours: item.hours
      }));
    },
    async addSyllabusItem() {
      if (!this.validateNewItem()) return;
      try {
        await addSyllabus(this.inputCourseId, this.newItem);
        this.showAddModal = false;
        this.fetchSyllabus();
        this.resetNewItem();
      } catch (error) {
        console.error('添加教学大纲项失败:', error);
        this.error = error.message || '添加教学大纲项失败，请稍后重试';
      }
    },
    async updateSyllabusItem() {
      if (!this.validateNewItem()) return;
      try {
        await updateSyllabus(this.inputCourseId, this.newItem);
        this.showAddModal = false;
        this.fetchSyllabus();
        this.resetNewItem();
        this.isEditing = false;
      } catch (error) {
        console.error('更新教学大纲项失败:', error);
        this.error = error.message || '更新教学大纲项失败，请稍后重试';
      }
    },
    async deleteSyllabusItem(week) {
      try {
        await deleteSyllabus(this.inputCourseId, week);
        this.fetchSyllabus();
      } catch (error) {
        console.error('删除教学大纲项失败:', error);
        this.error = error.message || '删除教学大纲项失败，请稍后重试';
      }
    },
    editNode(node) {
      this.isEditing = true;
      this.newItem = { ...node };
      this.showAddModal = true;
    },
    async deleteNode(id) {
      try {
        if (!confirm('确定要删除该大纲节点吗？')) return;
        await deleteSyllabus(this.inputCourseId, id);
        this.fetchSyllabus();
      } catch (error) {
        console.error('删除大纲节点失败:', error);
        this.error = error.message || '删除大纲节点失败，请稍后重试';
      }
    },
    selectNode(node) {
      this.selectedNode = node;
    },
    submitSyllabusItem() {
      if (this.isEditing) {
        this.updateSyllabusItem();
      } else {
        this.addSyllabusItem();
      }
    },
    resetNewItem() {
      this.newItem = {
        name: '',
        hours: null,
        objective: ''
      };
      this.newItemErrors = {
        name: '',
        hours: '',
        objective: ''
      };
    }
  }
};
</script>

<style scoped>
.syllabus-container {
  max-width: 900px;
  margin: 40px auto 0 auto;
  padding: 32px 24px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
}
.syllabus-header {
  text-align: center;
  margin-bottom: 32px;
}
.syllabus-header h1 {
  font-size: 2.6rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #222;
  letter-spacing: 2px;
}
.syllabus-meta {
  font-size: 1.1rem;
  color: #666;
  display: flex;
  justify-content: center;
  gap: 32px;
}
.syllabus-card {
  background: #f8fafc;
  border-radius: 14px;
  padding: 28px 18px 18px 18px;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.04);
}
.syllabus-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1.05rem;
  background: transparent;
}
.syllabus-table th, .syllabus-table td {
  border-bottom: 1px solid #e5e7eb;
  padding: 12px 8px;
  text-align: center;
}
.syllabus-table th {
  background: #f1f5f9;
  font-weight: 600;
  color: #333;
}
.syllabus-table tr:last-child td {
  border-bottom: none;
}
.syllabus-empty {
  text-align: center;
  color: #aaa;
  font-size: 1.2rem;
  padding: 32px 0;
}
.loading, .error {
  text-align: center;
  padding: 20px;
}
.error {
  color: red;
}
.add-button {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.4);
}
.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 500px;
  border-radius: 8px;
}
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}
.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.modal-content form div {
  margin-bottom: 15px;
}
.modal-content form label {
  display: inline-block;
  width: 80px;
}
.modal-content form input {
  padding: 5px;
}
.modal-content form button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 新增时间线样式 */
.timeline-container {
  margin-bottom: 32px;
}

.timeline {
  position: relative;
  padding-left: 20px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #e5e7eb;
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
  display: flex;
}

.timeline-point {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #4CAF50;
  margin-right: 16px;
}

.timeline-content {
  flex: 1;
}

.timeline-content h3 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
}

.timeline-content p {
  margin: 0;
  color: #666;
}

/* 新增搜索区域样式 */
.course-id-input {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.course-id-input input {
  padding: 5px;
}

.course-id-input button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  font-size: 0.8rem;
  margin-left: 5px;
}

/* 新增树形结构样式 */
.tree-container {
  overflow-x: auto;
}

.tree {
  list-style: none;
  padding-left: 20px;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.tree-node button {
  padding: 2px 8px;
  font-size: 0.8rem;
}
</style>