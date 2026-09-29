<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const logout = () => {
  localStorage.clear()
  router.push('/')
}
</script>

<template>
<nav class="navbar navbar-expand-lg navbar-dark pp-navbar shadow-sm">
  <div class="container">
    <a class="navbar-brand fw-bold text-white" href="#">
      <span class="text-primary">Your</span> Portal
    </a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#studentNav">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="studentNav">
      <div class="navbar-nav me-auto ms-lg-3">
        <button class="btn btn-link nav-link px-3 text-start" @click="router.push('/student/dashboard')">Dashboard</button>
        <button class="btn btn-link nav-link px-3 text-start" @click="router.push('/student/jobs')">Jobs</button>
        <button class="btn btn-link nav-link px-3 text-start" @click="router.push('/student/applications')">Applications</button>
        <button class="btn btn-link nav-link px-3 text-start" @click="router.push('/student/profile')">Profile</button>
      </div>
      <button class="btn btn-sm btn-outline-light px-3 mt-2 mt-lg-0" @click="logout">Logout</button>
    </div>
  </div>
</nav>
</template>

<style scoped>
.pp-navbar {
  background-color: #1e293b;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.nav-link {
  color: #94a3b8 !important;
  text-decoration: none;
  font-size: 0.95rem;
}
.nav-link:hover {
  color: #ffffff !important;
}
</style>