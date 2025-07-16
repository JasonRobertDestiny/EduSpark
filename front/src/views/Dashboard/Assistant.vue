<!-- src/views/Dashboard/Assistant.vue -->
<template>
  <div class="assistant-page">
    <div class="page-header">
  
      <h2>智能辅助做题</h2>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <div class="search-container">
        <div class="search-input-group">
          <input 
            v-model="searchQuery" 
            @keyup.enter="searchProblems"
            placeholder="搜索LeetCode题目（支持题号、题名、关键词）"
            class="search-input"
          />
          <button @click="searchProblems" class="search-btn" :disabled="isSearching">
            <svg v-if="!isSearching" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <div v-else class="spinner"></div>
            {{ isSearching ? '搜索中...' : '搜索' }}
          </button>
        </div>
        
        <!-- 筛选选项 -->
        <div class="filter-options">
          <select v-model="selectedDifficulty" class="filter-select">
            <option value="">所有难度</option>
            <option value="Easy">简单</option>
            <option value="Medium">中等</option>
            <option value="Hard">困难</option>
          </select>
          
          <select v-model="selectedCategory" class="filter-select">
            <option value="">所有分类</option>
            <option value="Array">数组</option>
            <option value="HashTable">哈希表</option>
            <option value="String">字符串</option>
            <option value="LinkedList">链表</option>
            <option value="Tree">树</option>
            <option value="Graph">图</option>
            <option value="DynamicProgramming">动态规划</option>
            <option value="Greedy">贪心</option>
            <option value="Backtracking">回溯</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 题目列表 -->
      <div class="problems-panel" v-if="!selectedProblem">
        <div class="panel-header">
          <h3>题目列表</h3>
          <span class="problem-count">共 {{ filteredProblems.length }} 道题</span>
        </div>
        
        <div class="problems-list" v-if="filteredProblems.length > 0">
          <div 
            v-for="problem in paginatedProblems" 
            :key="problem.id"
            class="problem-item"
            @click="selectProblem(problem)"
          >
            <div class="problem-info">
              <div class="problem-header">
                <span class="problem-id">#{{ problem.id }}</span>
                <span :class="['difficulty', problem.difficulty.toLowerCase()]">{{ getDifficultyText(problem.difficulty) }}</span>
              </div>
              <h4 class="problem-title">{{ problem.title }}</h4>
              <div class="problem-tags">
                <span v-for="tag in problem.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
            <div class="problem-stats">
              <div class="acceptance-rate">通过率: {{ problem.acceptanceRate }}%</div>
            </div>
          </div>
        </div>
        
        <!-- 分页 -->
        <div class="pagination" v-if="totalPages > 1">
          <button 
            @click="currentPage = Math.max(1, currentPage - 1)"
            :disabled="currentPage === 1"
            class="page-btn"
          >上一页</button>
          
          <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
          
          <button 
            @click="currentPage = Math.min(totalPages, currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="page-btn"
          >下一页</button>
        </div>
        
        <!-- 空状态 -->
        <div class="empty-state" v-if="filteredProblems.length === 0 && !isSearching">
          <div class="empty-icon">🔍</div>
          <h3>暂无题目</h3>
          <p>请尝试搜索或调整筛选条件</p>
        </div>
      </div>

      <!-- 题目详情和编程界面 -->
      <div class="coding-panel" v-if="selectedProblem">
        <!-- 题目详情 -->
        <div class="problem-detail">
          <div class="detail-header">
            <button @click="backToList" class="back-to-list-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
              返回列表
            </button>
            <div class="problem-meta">
              <span class="problem-id">#{{ selectedProblem.id }}</span>
              <h3>{{ selectedProblem.title }}</h3>
              <span :class="['difficulty', selectedProblem.difficulty.toLowerCase()]">{{ getDifficultyText(selectedProblem.difficulty) }}</span>
            </div>
          </div>
          
          <div class="problem-description">
            <div class="description-content" v-html="selectedProblem.description"></div>
            
            <div class="examples" v-if="selectedProblem.examples">
              <h4>示例：</h4>
              <div v-for="(example, index) in selectedProblem.examples" :key="index" class="example">
                <div class="example-title">示例 {{ index + 1 }}：</div>
                <div class="example-content">
                  <div><strong>输入：</strong>{{ example.input }}</div>
                  <div><strong>输出：</strong>{{ example.output }}</div>
                  <div v-if="example.explanation"><strong>解释：</strong>{{ example.explanation }}</div>
                </div>
              </div>
            </div>
            
            <div class="constraints" v-if="selectedProblem.constraints">
              <h4>约束条件：</h4>
              <ul>
                <li v-for="constraint in selectedProblem.constraints" :key="constraint">{{ constraint }}</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 代码编辑区域 -->
        <div class="code-section">
          <div class="code-header">
            <div class="language-selector">
              <select v-model="selectedLanguage" class="language-select">
                <option value="javascript">JavaScript</option>
                <option value="python">Python</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
                <option value="c">C</option>
              </select>
            </div>
            
            <div class="code-actions">
              <button @click="getHint" class="hint-btn" :disabled="isGettingHint">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                  <path d="M12 17h.01"/>
                </svg>
                {{ isGettingHint ? '获取中...' : '获取提示' }}
              </button>
              
              <button @click="runCode" class="run-btn" :disabled="isRunning">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5,3 19,12 5,21"/>
                </svg>
                {{ isRunning ? '运行中...' : '运行代码' }}
              </button>
              
              <button @click="submitCode" class="submit-btn" :disabled="isSubmitting">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22,4 12,14.01 9,11.01"/>
                </svg>
                {{ isSubmitting ? '提交中...' : '提交答案' }}
              </button>
            </div>
          </div>
          
          <div class="code-editor">
            <textarea 
              v-model="userCode" 
              class="code-textarea"
              :placeholder="getCodeTemplate()"
              spellcheck="false"
            ></textarea>
          </div>
          
          <!-- AI提示区域 -->
          <div class="hint-section" v-if="currentHint">
            <div class="hint-header">
              <h4>💡 AI提示</h4>
              <button @click="currentHint = ''" class="close-hint-btn">×</button>
            </div>
            <div class="hint-content">{{ currentHint }}</div>
          </div>
          
          <!-- 运行结果 -->
          <div class="result-section" v-if="runResult">
            <div class="result-header">
              <h4>🔍 运行结果</h4>
              <button @click="runResult = null" class="close-result-btn">×</button>
            </div>
            <div class="result-content">
              <div v-if="runResult.success" class="result-success">
                <div><strong>状态：</strong>通过</div>
                <div><strong>输出：</strong>{{ runResult.output }}</div>
                <div v-if="runResult.runtime"><strong>执行时间：</strong>{{ runResult.runtime }}ms</div>
              </div>
              <div v-else class="result-error">
                <div><strong>状态：</strong>错误</div>
                <div><strong>错误信息：</strong>{{ runResult.error }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Assistant',
  data() {
    return {
      searchQuery: '',
      isSearching: false,
      selectedDifficulty: '',
      selectedCategory: '',
      selectedProblem: null,
      selectedLanguage: 'javascript',
      userCode: '',
      currentHint: '',
      runResult: null,
      isGettingHint: false,
      isRunning: false,
      isSubmitting: false,
      currentPage: 1,
      pageSize: 10,
      
      // 模拟题目数据
      problems: [
        {
          id: 1,
          title: '两数之和',
          difficulty: 'Easy',
          tags: ['数组', '哈希表'],
          acceptanceRate: 52.1,
          description: `
            <p>给定一个整数数组 <code>nums</code> 和一个整数目标值 <code>target</code>，请你在该数组中找出 <strong>和为目标值</strong> <em>target</em> 的那 <strong>两个</strong> 整数，并返回它们的数组下标。</p>
            <p>你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。</p>
            <p>你可以按任意顺序返回答案。</p>
          `,
          examples: [
            {
              input: 'nums = [2,7,11,15], target = 9',
              output: '[0,1]',
              explanation: '因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。'
            }
          ],
          constraints: [
            '2 <= nums.length <= 10^4',
            '-10^9 <= nums[i] <= 10^9',
            '-10^9 <= target <= 10^9',
            '只会存在一个有效答案'
          ]
        },
        {
          id: 2,
          title: '两数相加',
          difficulty: 'Medium',
          tags: ['链表', '数学', '递归'],
          acceptanceRate: 39.7,
          description: `
            <p>给你两个 <strong>非空</strong> 的链表，表示两个非负的整数。它们每位数字都是按照 <strong>逆序</strong> 的方式存储的，并且每个节点只能存储 <strong>一位</strong> 数字。</p>
            <p>请你将两个数相加，并以相同形式返回一个表示和的链表。</p>
            <p>你可以假设除了数字 0 之外，这两个数都不会以 0 开头。</p>
          `,
          examples: [
            {
              input: 'l1 = [2,4,3], l2 = [5,6,4]',
              output: '[7,0,8]',
              explanation: '342 + 465 = 807'
            }
          ],
          constraints: [
            '每个链表中的节点数在范围 [1, 100] 内',
            '0 <= Node.val <= 9',
            '题目数据保证列表表示的数字不含前导零'
          ]
        },
        {
          id: 3,
          title: '无重复字符的最长子串',
          difficulty: 'Medium',
          tags: ['哈希表', '字符串', '滑动窗口'],
          acceptanceRate: 38.9,
          description: `
            <p>给定一个字符串 <code>s</code> ，请你找出其中不含有重复字符的 <strong>最长子串</strong> 的长度。</p>
          `,
          examples: [
            {
              input: 's = "abcabcbb"',
              output: '3',
              explanation: '因为无重复字符的最长子串是 "abc"，所以其长度为 3。'
            }
          ],
          constraints: [
            '0 <= s.length <= 5 * 10^4',
            's 由英文字母、数字、符号和空格组成'
          ]
        }
      ]
    }
  },
  
  computed: {
    filteredProblems() {
      let filtered = this.problems;
      
      // 按搜索关键词过滤
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(problem => 
          problem.title.toLowerCase().includes(query) ||
          problem.id.toString().includes(query) ||
          problem.tags.some(tag => tag.toLowerCase().includes(query))
        );
      }
      
      // 按难度过滤
      if (this.selectedDifficulty) {
        filtered = filtered.filter(problem => problem.difficulty === this.selectedDifficulty);
      }
      
      // 按分类过滤
      if (this.selectedCategory) {
        const categoryMap = {
          'Array': '数组',
          'HashTable': '哈希表',
          'String': '字符串',
          'LinkedList': '链表',
          'Tree': '树',
          'Graph': '图',
          'DynamicProgramming': '动态规划',
          'Greedy': '贪心',
          'Backtracking': '回溯'
        };
        const chineseCategory = categoryMap[this.selectedCategory];
        filtered = filtered.filter(problem => 
          problem.tags.some(tag => tag.includes(chineseCategory))
        );
      }
      
      return filtered;
    },
    
    totalPages() {
      return Math.ceil(this.filteredProblems.length / this.pageSize);
    },
    
    paginatedProblems() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredProblems.slice(start, end);
    }
  },
  
  methods: {
    goBack() {
      this.$router.push('/dashboard?nav=resource');
    },
    
    async searchProblems() {
      if (!this.searchQuery.trim()) return;
      
      this.isSearching = true;
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 这里应该调用后端API搜索LeetCode题目
        console.log('搜索题目:', this.searchQuery);
        
        // 重置分页
        this.currentPage = 1;
      } catch (error) {
        console.error('搜索失败:', error);
        alert('搜索失败，请重试');
      } finally {
        this.isSearching = false;
      }
    },
    
    selectProblem(problem) {
      this.selectedProblem = problem;
      this.userCode = this.getCodeTemplate();
      this.currentHint = '';
      this.runResult = null;
    },
    
    backToList() {
      this.selectedProblem = null;
      this.userCode = '';
      this.currentHint = '';
      this.runResult = null;
    },
    
    getDifficultyText(difficulty) {
      const map = {
        'Easy': '简单',
        'Medium': '中等',
        'Hard': '困难'
      };
      return map[difficulty] || difficulty;
    },
    
    getCodeTemplate() {
      const templates = {
        javascript: `// JavaScript 解决方案
function solution() {
    // 在这里编写你的代码
    
}`,
        python: `# Python 解决方案
def solution():
    # 在这里编写你的代码
    pass`,
        java: `// Java 解决方案
public class Solution {
    public void solution() {
        // 在这里编写你的代码
    }
}`,
        cpp: `// C++ 解决方案
class Solution {
public:
    void solution() {
        // 在这里编写你的代码
    }
};`,
        c: `// C 解决方案
#include <stdio.h>

void solution() {
    // 在这里编写你的代码
}`
      };
      return templates[this.selectedLanguage] || templates.javascript;
    },
    
    async getHint() {
      if (!this.selectedProblem) return;
      
      this.isGettingHint = true;
      try {
        // 模拟调用AI获取提示
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 这里应该调用后端API获取AI提示
        const hints = [
          '考虑使用哈希表来存储已遍历的元素，这样可以在O(1)时间内查找目标值。',
          '尝试使用双指针技术，一个指针从头开始，另一个从尾开始。',
          '这个问题可能需要动态规划的思想，考虑子问题的最优解。',
          '注意边界条件的处理，特别是空数组或单元素数组的情况。'
        ];
        
        this.currentHint = hints[Math.floor(Math.random() * hints.length)];
      } catch (error) {
        console.error('获取提示失败:', error);
        alert('获取提示失败，请重试');
      } finally {
        this.isGettingHint = false;
      }
    },
    
    async runCode() {
      if (!this.userCode.trim()) {
        alert('请先编写代码');
        return;
      }
      
      this.isRunning = true;
      try {
        // 模拟代码运行
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // 这里应该调用后端API运行代码
        const success = Math.random() > 0.3; // 70%成功率
        
        if (success) {
          this.runResult = {
            success: true,
            output: '[0, 1]',
            runtime: Math.floor(Math.random() * 100) + 50
          };
        } else {
          this.runResult = {
            success: false,
            error: 'TypeError: Cannot read property of undefined'
          };
        }
      } catch (error) {
        console.error('运行代码失败:', error);
        alert('运行代码失败，请重试');
      } finally {
        this.isRunning = false;
      }
    },
    
    async submitCode() {
      if (!this.userCode.trim()) {
        alert('请先编写代码');
        return;
      }
      
      this.isSubmitting = true;
      try {
        // 模拟代码提交
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 这里应该调用后端API提交代码
        const success = Math.random() > 0.5; // 50%成功率
        
        if (success) {
          alert('🎉 恭喜！代码提交成功，所有测试用例通过！');
        } else {
          alert('❌ 提交失败，部分测试用例未通过，请检查代码逻辑。');
        }
      } catch (error) {
        console.error('提交代码失败:', error);
        alert('提交代码失败，请重试');
      } finally {
        this.isSubmitting = false;
      }
    }
  },
  
  watch: {
    selectedLanguage() {
      if (this.selectedProblem) {
        this.userCode = this.getCodeTemplate();
      }
    },
    
    selectedDifficulty() {
      this.currentPage = 1;
    },
    
    selectedCategory() {
      this.currentPage = 1;
    }
  }
}
</script>

<style scoped>
.assistant-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  background: #f8fafc;
  min-height: 100vh;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #1976d2;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  position: absolute;
  left: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: #1560a8;
  transform: translateY(-1px);
}

.back-btn svg {
  transition: transform 0.2s ease;
}

.back-btn:hover svg {
  transform: translateX(-2px);
}

h2 {
  margin: 0;
  color: #1a202c;
  font-size: 28px;
  font-weight: 600;
}

/* 搜索区域样式 */
.search-section {
  margin-bottom: 30px;
}

.search-container {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.search-input-group {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #1976d2;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.2s ease;
  min-width: 120px;
  justify-content: center;
}

.search-btn:hover:not(:disabled) {
  background: #1560a8;
  transform: translateY(-1px);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.filter-options {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 10px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #1976d2;
}

/* 主要内容区域 */
.main-content {
  display: grid;
  gap: 30px;
}

/* 题目列表样式 */
.problems-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.panel-header h3 {
  margin: 0;
  color: #1a202c;
  font-size: 20px;
  font-weight: 600;
}

.problem-count {
  color: #64748b;
  font-size: 14px;
}

.problems-list {
  max-height: 600px;
  overflow-y: auto;
}

.problem-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.2s ease;
}

.problem-item:hover {
  background: #f8fafc;
  transform: translateX(4px);
}

.problem-item:last-child {
  border-bottom: none;
}

.problem-info {
  flex: 1;
}

.problem-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.problem-id {
  background: #e2e8f0;
  color: #475569;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.difficulty {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.difficulty.easy {
  background: #dcfce7;
  color: #166534;
}

.difficulty.medium {
  background: #fef3c7;
  color: #92400e;
}

.difficulty.hard {
  background: #fecaca;
  color: #991b1b;
}

.problem-title {
  margin: 0 0 8px 0;
  color: #1a202c;
  font-size: 16px;
  font-weight: 500;
}

.problem-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  background: #e0f2fe;
  color: #0277bd;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.problem-stats {
  text-align: right;
}

.acceptance-rate {
  color: #64748b;
  font-size: 14px;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-top: 1px solid #e2e8f0;
}

.page-btn {
  background: #1976d2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background: #1560a8;
}

.page-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.page-info {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  color: #475569;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* 编程界面样式 */
.coding-panel {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  align-items: start;
}

.problem-detail {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.detail-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.back-to-list-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #64748b;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 16px;
  transition: all 0.2s ease;
}

.back-to-list-btn:hover {
  background: #475569;
}

.problem-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.problem-meta h3 {
  margin: 0;
  color: #1a202c;
  font-size: 18px;
  font-weight: 600;
}

.problem-description {
  padding: 24px;
  max-height: 500px;
  overflow-y: auto;
}

.description-content {
  margin-bottom: 24px;
  line-height: 1.6;
  color: #374151;
}

.description-content p {
  margin-bottom: 12px;
}

.description-content code {
  background: #f1f5f9;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
}

.examples h4,
.constraints h4 {
  color: #1a202c;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.example {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
}

.example-title {
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 8px;
}

.example-content div {
  margin-bottom: 4px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
}

.constraints {
  margin-top: 24px;
}

.constraints ul {
  margin: 0;
  padding-left: 20px;
}

.constraints li {
  margin-bottom: 4px;
  color: #374151;
  font-size: 14px;
}

/* 代码编辑区域样式 */
.code-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.language-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.language-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  cursor: pointer;
}

.code-actions {
  display: flex;
  gap: 8px;
}

.hint-btn,
.run-btn,
.submit-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.hint-btn {
  background: #f59e0b;
  color: white;
}

.hint-btn:hover:not(:disabled) {
  background: #d97706;
}

.run-btn {
  background: #10b981;
  color: white;
}

.run-btn:hover:not(:disabled) {
  background: #059669;
}

.submit-btn {
  background: #dc2626;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #b91c1c;
}

.hint-btn:disabled,
.run-btn:disabled,
.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.code-editor {
  position: relative;
}

.code-textarea {
  width: 100%;
  height: 400px;
  padding: 20px;
  border: none;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  outline: none;
  background: #1e293b;
  color: #e2e8f0;
}

.code-textarea::placeholder {
  color: #64748b;
}

/* AI提示区域样式 */
.hint-section {
  border-top: 1px solid #e2e8f0;
  background: #fffbeb;
}

.hint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid #fde68a;
}

.hint-header h4 {
  margin: 0;
  color: #92400e;
  font-size: 14px;
  font-weight: 600;
}

.close-hint-btn {
  background: none;
  border: none;
  color: #92400e;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.close-hint-btn:hover {
  background: #fde68a;
}

.hint-content {
  padding: 16px 20px;
  color: #92400e;
  font-size: 14px;
  line-height: 1.5;
}

/* 运行结果样式 */
.result-section {
  border-top: 1px solid #e2e8f0;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #f0f9ff;
  border-bottom: 1px solid #bae6fd;
}

.result-header h4 {
  margin: 0;
  color: #0369a1;
  font-size: 14px;
  font-weight: 600;
}

.close-result-btn {
  background: none;
  border: none;
  color: #0369a1;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.close-result-btn:hover {
  background: #bae6fd;
}

.result-content {
  padding: 16px 20px;
}

.result-success {
  color: #065f46;
}

.result-success div {
  margin-bottom: 4px;
  font-size: 14px;
}

.result-error {
  color: #991b1b;
}

.result-error div {
  margin-bottom: 4px;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .coding-panel {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .assistant-page {
    padding: 10px;
  }
  
  .page-header {
    padding: 15px;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .back-btn {
    margin-right: 0;
  }
  
  h2 {
    font-size: 24px;
  }
  
  .search-container {
    padding: 16px;
  }
  
  .search-input-group {
    flex-direction: column;
  }
  
  .filter-options {
    flex-direction: column;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .problem-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .code-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .code-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .hint-btn,
  .run-btn,
  .submit-btn {
    flex: 1;
    justify-content: center;
  }
}
</style>