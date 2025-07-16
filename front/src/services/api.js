import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // 连接到我们的FastAPI后端
  headers: {
    'Content-Type': 'application/json',
  }
});


//社区空间部分
// 帖子相关API
export const getPosts = () => apiClient.get('/posts');
export const createPost = (postData) => apiClient.post('/posts', postData);
export const likePost = (postId) => apiClient.post(`/posts/${postId}/like`);

// 用户信息相关API
export const getUserProfile = (userId) => apiClient.get(`/users/${userId}`);

// 热门话题API
export const getTrends = () => apiClient.get('/trends');

// 文件管理相关API
export const getFiles = (userId, searchTerm = '') => {
  const params = { userId };
  if (searchTerm) {
    params.search = searchTerm;
  }
  return apiClient.get('/files', { params }).then(response => response.data);
};


export const uploadFile = (userId, fileData) => {
  const formData = new FormData();
  formData.append('file', fileData);
  formData.append('userId', userId);
  return apiClient.post('/files/upload', formData)
    .then(response => response.data)
    .catch(error => {
      console.error('文件上传失败:', error);
      throw error;
    });
};

export const deleteFile = (fileId) => {
  return apiClient.delete(`/files/${fileId}`).then(response => response.data);
};

// 智能培养方案相关API
/**
 * 生成智能培养方案
 * @param {string} subject - 教学科目
 * @returns {Promise<any>} 返回包含培养方案数据的 Promise
 */
export const generateTrainingProgram = async (subject) => {
  // 参数校验
  if (typeof subject !== 'string' || !subject.trim()) {
    throw new Error('教学科目必须是非空字符串');
  }

  try {
    const response = await apiClient.post('/training-programs/generate', { subject });
    // 检查响应状态，确保数据有效
    if (response.status >= 200 && response.status < 300) {
      return response.data;
    } else {
      throw new Error(`请求失败，状态码: ${response.status}`);
    }
  } catch (error) {
    // 记录错误日志
    console.error('生成智能培养方案失败:', error);
    // 将错误抛出，方便调用处处理
    throw error;
  }
};

// 教学大纲相关API
/**
 * 获取课程教学大纲数据
 * @param {string} courseId - 课程编号
 * @returns {Promise<any>} 返回包含教学大纲数据的 Promise
 */
export const getSyllabus = async (courseId) => {
  try {
    // 使用 apiClient 发起请求
    const response = await apiClient.get(`/syllabus/${courseId}`); 
    return response.data;
  } catch (error) {
    console.error('API 请求出错:', error);
    throw error;
  }
};

/**
 * 添加新的教学大纲项
 * @param {string} courseId - 课程编号
 * @param {Object} newItem - 新的大纲项数据
 * @returns {Promise<any>} 返回包含添加结果的 Promise
 */
export const addSyllabus = async (courseId, newItem) => {
  try {
    // 使用 apiClient 发起请求
    const response = await apiClient.post(`/syllabus/${courseId}`, newItem);
    return response.data;
  } catch (error) {
    console.error('添加教学大纲项失败:', error);
    throw error;
  }
};

/**
 * 更新教学大纲项
 * @param {string} courseId - 课程编号
 * @param {Object} updatedItem - 更新后的大纲项数据
 * @returns {Promise<any>} 返回包含更新结果的 Promise
 */
export const updateSyllabus = async (courseId, updatedItem) => {
  try {
    // 使用 apiClient 发起请求
    const response = await apiClient.put(`/syllabus/${courseId}`, updatedItem);
    return response.data;
  } catch (error) {
    console.error('更新教学大纲项失败:', error);
    throw error;
  }
};

/**
 * 删除教学大纲项
 * @param {string} courseId - 课程编号
 * @param {string|number} itemId - 要删除的大纲项 ID
 * @returns {Promise<any>} 返回包含删除结果的 Promise
 */
export const deleteSyllabus = async (courseId, itemId) => {
  try {
    // 使用 apiClient 发起请求
    const response = await apiClient.delete(`/syllabus/${courseId}/${itemId}`);
    return response.data;
  } catch (error) {
    console.error('删除教学大纲项失败:', error);
    throw error;
  }
};
// PPT生成相关API
export const generatePPT = (pptConfig) => {
  return apiClient.post('/ppt/generate', pptConfig).then(response => response.data);
};

// 智能试卷生成
export async function generateExam(examConfig) {
  try {
    const response = await fetch('/api/exam/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(examConfig)
    });
    if (!response.ok) {
      throw new Error('试卷生成接口请求失败');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}

// 多模态问答API
export const askMultimodalQA = (payload) => {
  const formData = new FormData();
  formData.append('question', payload.question);
  (payload.files || []).forEach((file, idx) => {
    formData.append('files', file.file || file);
  });
  (payload.images || []).forEach((image, idx) => {
    formData.append('images', image.file || image);
  });
  return apiClient.post('/qa/multimodal', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    }
  }).then(res => res.data);
};


// 智能作业生成API
export const generateHomework = async (homeworkConfig) => {
  try {
    const response = await apiClient.post('/homework/generate', homeworkConfig);
    return response.data;
  } catch (error) {
    throw error;
  }
};


// 学情分析相关API
export const getLearningAnalysis = async (params) => {
  try {
    const response = await apiClient.get('/learning-analysis', { params });
    return response.data;
  } catch (error) {
    throw error;
  }
};


// 力扣MCP相关API
// 题目检索
export const searchLeetCodeProblems = (params) => {
  return apiClient.get('/leetcode/problems', { params }).then(res => res.data);
};
// 获取题目详情
export const getLeetCodeProblemDetail = (problemId) => {
  return apiClient.get(`/leetcode/problems/${problemId}`).then(res => res.data);
};
// 获取AI提示
export const getLeetCodeHint = (problemId, language, code) => {
  return apiClient.post(`/leetcode/hint`, { problemId, language, code }).then(res => res.data);
};
// 运行代码
export const runLeetCodeCode = (problemId, language, code) => {
  return apiClient.post(`/leetcode/run`, { problemId, language, code }).then(res => res.data);
};
// 提交代码
export const submitLeetCodeCode = (problemId, language, code) => {
  return apiClient.post(`/leetcode/submit`, { problemId, language, code }).then(res => res.data);
};




