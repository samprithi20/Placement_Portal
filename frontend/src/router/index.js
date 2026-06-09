import { createRouter, createWebHistory } from "vue-router"

import Login from "../components/login.vue"

import AdminDashboard from "../components/admin_dashboard.vue"

import StudentDashboard from "../components/student_dashboard.vue"

import CompanyDashboard from "../components/company_dashboard.vue"

import RegisterStudent from "../components/register_student.vue"

import RegisterCompany from "../components/register_company.vue"

import StudentJobs from "../components/student_jobs.vue"

import AllStudents from "../components/all_students.vue"

import AllCompanies from "../components/all_companies.vue"

import AllJobs from "../components/all_jobs.vue"

import PostJob from "../components/create_job.vue"

import CompanyJobs from "../components/company_jobs.vue"

import CompanyApplications from "../components/company_application.vue"

import MyApplications from "../components/my_applications.vue"

import EditProfile from "../components/student_edit_profile.vue"

import JobApplications from "../components/job_applications.vue"

import CompanyEditProfile from "../components/company_edit_profile.vue"

import Report from "../components/reports.vue"


const routes = [

  {
    path: "/",
    component: Login
  },

  {
    path: "/admin",
    component: AdminDashboard
  },

  {
    path: "/student",
    component: StudentDashboard
  },

  {
    path: "/company",
    component: CompanyDashboard
  },

  {
    path: "/register-student",
    component: RegisterStudent
  },

  {
    path: "/register-company",
    component: RegisterCompany
  },

  {
  path: "/student-jobs",
  component: StudentJobs
  },

  {
  path: "/my-applications",
  component: MyApplications
  },

  {
  path: "/all-students",
  component: AllStudents
  },

  {
    path: "/all-companies",
    component: AllCompanies
  },

  {
    path: "/all-jobs",
    component: AllJobs
  },

  {
  path: "/create-job",
  component: PostJob
  },

  {
    path: "/company-jobs",
    component: CompanyJobs
  },

  {
   path: "/company-applications",
    component: CompanyApplications
  },
  {
  path: "/student-edit-profile",
  component: EditProfile
  },
  {
  path: "/job-applications/:jobId",
  component: JobApplications
  },

  {
  path: "/company-edit-profile",
  component: CompanyEditProfile
  },
  {
    path: "/reports",
    component: Report
}


]

const router = createRouter({

  history: createWebHistory(),

  routes

})

export default router
