/**
 * 模拟生成专业培养方案的 API
 * @param {string} subject - 教学科目
 * @returns {Promise<Object>} 返回包含培养方案数据的 Promise 对象
 */
export const generateTrainingProgram = (subject) => {
  return new Promise((resolve) => {
    // 模拟网络请求延迟
    setTimeout(() => {
      // 模拟数据
      const mockData = {
        '计算机科学与技术': {
          subject: '计算机科学与技术',
          introduction: '计算机科学与技术专业是一个综合性的学科，涵盖了计算机硬件、软件、网络、算法等多个方面。本专业培养具有良好的科学素养，系统地掌握计算机科学与技术的基本理论、基本知识和基本技能的高级专门人才。',
          directions: [
            '软件开发工程师',
            '系统架构师',
            '数据库管理员',
            '网络安全工程师',
            '人工智能工程师',
            '大数据分析师'
          ],
          objectives: '培养德、智、体、美全面发展，具有良好的科学素养和人文素养，系统地掌握计算机科学与技术的基本理论、基本知识和基本技能，具有较强的实践能力和创新精神，能在科研部门、教育单位、企业、事业、技术和行政管理部门等单位从事计算机教学、科学研究和应用的计算机科学与技术学科的高级专门人才。',
          requirements: [
            {
              category: '知识要求',
              items: [
                '掌握数学、自然科学基础知识',
                '掌握计算机科学与技术的基本理论和方法',
                '掌握计算机系统分析和设计的基本方法',
                '了解计算机科学与技术的发展现状和趋势'
              ]
            },
            {
              category: '能力要求',
              items: [
                '具有运用所学知识分析和解决问题的能力',
                '具有计算机软硬件系统的设计和开发能力',
                '具有较强的实践能力和创新意识',
                '具有良好的团队合作和沟通能力'
              ]
            },
            {
              category: '素质要求',
              items: [
                '具有良好的思想道德品质和职业道德',
                '具有较强的学习能力和适应能力',
                '具有国际视野和跨文化交流能力',
                '具有健康的身心素质'
              ]
            }
          ],
          courses: [
            '高等数学', '线性代数', '概率论与数理统计', 'C语言程序设计',
            '数据结构', '计算机组成原理', '操作系统', '计算机网络',
            '数据库原理', '软件工程', '算法设计与分析', '编译原理',
            'Java程序设计', 'Web开发技术', '人工智能', '机器学习'
          ]
        }
      };

      // 如果有匹配的专业数据就返回，否则返回通用模板
      const result = mockData[subject] || {
        subject: subject,
        introduction: `${subject}是一个重要的学科领域，致力于培养具备扎实理论基础和实践能力的专业人才。本专业注重理论与实践相结合，培养学生的创新思维和解决实际问题的能力。`,
        directions: [
          '专业技术岗位',
          '管理岗位',
          '研发岗位',
          '教育岗位',
          '咨询岗位'
        ],
        objectives: `培养德、智、体、美全面发展，具备${subject}领域的基本理论、基本知识和基本技能，具有较强实践能力和创新精神的高级专门人才。`,
        requirements: [
          {
            category: '知识要求',
            items: [
              '掌握本专业的基础理论知识',
              '了解专业发展前沿和趋势',
              '具备跨学科知识结构',
              '掌握科学研究方法'
            ]
          },
          {
            category: '能力要求',
            items: [
              '具有分析和解决专业问题的能力',
              '具有实践操作和应用能力',
              '具有创新思维和创新能力',
              '具有团队协作和沟通能力'
            ]
          }
        ],
        courses: [
          '专业基础课程', '专业核心课程', '专业选修课程', '实践课程'
        ]
      };

      resolve(result);
    }, 1000);
  });
};