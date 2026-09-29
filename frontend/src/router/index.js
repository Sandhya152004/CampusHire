import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'

import StudentRegisterView from '../views/StudentRegisterView.vue'
import CompanyRegisterView from '../views/CompanyRegisterView.vue'

import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminCompanies from '../views/admin/AdminCompanies.vue'
import AdminStudents from '../views/admin/AdminStudents.vue'
import AdminDrives from '../views/admin/AdminDrives.vue'
import AdminReports from '../views/admin/AdminReports.vue'
import AdminCompanyProfile from '../views/admin/AdminCompanyProfile.vue'
import AdminApplications
from '../views/admin/AdminApplications.vue'
import AdminStudentProfile from '../views/admin/AdminStudentProfile.vue'

import CompanyDashboard from '../views/company/CompanyDashboard.vue'
import CompanyDrives from '../views/company/CompanyDrives.vue'
import CompanyApplicants from '../views/company/CompanyApplicants.vue'
import CompanyProfile from '../views/company/CompanyProfile.vue'
import CompanyStudentProfile from '../views/company/CompanyStudentProfile.vue'

import StudentDashboard from '../views/student/StudentDashboard.vue'
import StudentJobs from '../views/student/StudentJobs.vue'
import StudentApplications from '../views/student/StudentApplications.vue'
import StudentProfile from '../views/student/StudentProfile.vue'

const routes = [

  {
    path: '/',
    component: LoginView
  },
  {
    path: '/admin/dashboard',
    component: AdminDashboard
  },
  {
    path: '/register/student',
    component: StudentRegisterView
  },
  
  {
    path: '/register/company',
    component: CompanyRegisterView
  },
  {
    path: '/admin/companies',
  
    component: AdminCompanies
  },
  
  {
    path: '/admin/students',
  
    component: AdminStudents
  },
  
  {
    path: '/admin/drives',
  
    component: AdminDrives
  },
  
  {
    path: '/admin/reports',
  
    component: AdminReports
  },
  {
    path: '/admin/company/:id',
    component: AdminCompanyProfile
  },
  {
    path: '/admin/student/:id',
    component: AdminStudentProfile
  },
  {
    path:'/admin/applications',

    component:AdminApplications
  },
  {
      path: '/company/dashboard',
      component: CompanyDashboard
  },
  {
      path: '/company/drives',
      component: CompanyDrives
  },
  {
      path: '/company/applicants',
      component: CompanyApplicants
  },
  {
      path: '/company/profile',
      component: CompanyProfile
  },
  {
      path: '/company/student/:id',
      component: CompanyStudentProfile
  },
  {
    path: '/student/dashboard',
    component: StudentDashboard
  },
  {
    path: '/student/jobs',
    component: StudentJobs
  },
  {
    path: '/student/applications',
    component: StudentApplications
  },
  {
    path: '/student/profile',
    component: StudentProfile
  }
  ]

const router = createRouter({
  history: createWebHistory(),
  routes
})
router.beforeEach((to, from, next) => {

  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  // Public pages
  if (
    to.path === '/' ||
    to.path === '/register/student' ||
    to.path === '/register/company'
  ) {
    return next()
  }

  // Not logged in
  if (!token) {
    return next('/')
  }

  if (
    to.path.startsWith('/student') &&
    role !== 'student'
  ) {
    return next('/')
  }
  
  if (
    to.path.startsWith('/company') &&
    role !== 'company'
  ) {
    return next('/')
  }
  
  if (
    to.path.startsWith('/admin') &&
    role !== 'admin'
  ) {
    return next('/')
  }

  next()
})

export default router
