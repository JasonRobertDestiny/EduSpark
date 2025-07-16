import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Author/Login.vue';
import Register from '@/views/Author/Register.vue';
import IntCourseManage from '@/views/Dashboard/IntCourseManage.vue';
import TeacherDashboard from '@/views/Dashboard/TeacherDashboard.vue';
import ResourceManage from '@/views/Dashboard/ResourceManage.vue';
import Homework from '@/views/Dashboard/Homework.vue';
import Exam from '@/views/Dashboard/Exam.vue';
import QA from '@/views/Dashboard/QA.vue';
import Assistant from '@/views/Dashboard/Assistant.vue';
import Profile from '@/views/Dashboard/Profile.vue';
import PPT from '@/views/Dashboard/PPT.vue';
import Framework from '@/views/Dashboard/Framework.vue';
import TeachingMaterial from '@/views/CourseManage/TeachingMaterial.vue';
import Syllabus from '@/views/CourseManage/Syllabus.vue';
import IntTrainManage from '@/views/CourseManage/IntTrainManage.vue';
import LearningAnalysis from '@/views/CourseManage/LearningAnalysis.vue';
import StudentDashboard from '@/views/StudentDashboard/StudentDashboard.vue';
import AssistedQuestioning from '@/views/StudentDashboard/AssistedQuestioning.vue';
import StudentLearningAnalysis from '@/views/StudentDashboard/StudentLearningAnalysis.vue';
import CommunitySpace from '@/views/StudentDashboard/CommunitySpace.vue';



const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: TeacherDashboard,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/dashboard/course',
    name: 'IntCourseManage',
    component: IntCourseManage
  },
  {
    path: '/dashboard/resource',
    name: 'ResourceManage',
    component: ResourceManage
  },
  {
    path: '/dashboard/homework',
    name: 'Homework',
    component: Homework
  },
  {
    path: '/dashboard/exam',
    name: 'Exam',
    component: Exam
  },
  {
    path: '/dashboard/qa',
    name: 'QA',
    component: QA
  },
  {
    path: '/dashboard/assistant',
    name: 'Assistant',
    component: Assistant
  },
  {
    path: '/dashboard/profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/dashboard/PPT',
    name: 'PPT',
    component: PPT
  },
  {
    path: '/dashboard/Framework',
    name: 'Framework',
    component: Framework
  },
  {
    path: '/course/material',
    name: 'TeachingMaterial',
    component: TeachingMaterial
  },
  {
    path: '/course/syllabus',
    name: 'Syllabus',
    component: Syllabus
  },
  {
    path: '/course/interactive',
    name: 'IntTrainManage',
    component: IntTrainManage
  },
  {
    path: '/course/analysis',
    name: 'TeacherLearningAnalysis',
    component: LearningAnalysis
  },
  {
    path: '/student-dashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' },
    children: [
      {
        path: '',
        name: 'StudentDashboard',
        redirect: '/student-dashboard/assisted-questioning'
      },
      {
        path: 'assisted-questioning',
        name: 'AssistedQuestioning',
        component: AssistedQuestioning
      },
      {
        path: 'learning-analysis',
        name: 'LearningAnalysis',
        component: StudentLearningAnalysis
      },
      {
        path: 'community-space',
        name: 'CommunitySpace',
        component: CommunitySpace
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;