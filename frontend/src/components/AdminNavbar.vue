<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const role = localStorage.getItem('role')

const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    router.push('/')
}
</script>

<template>
<nav class="navbar navbar-expand-lg navbar-dark pp-navbar shadow-sm">
    <div class="container">
        <router-link class="navbar-brand fw-bold text-white tracking-tight" to="/">
            <span class="text-primary">Your</span> Portal
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#adminNav">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="adminNav">
            <div class="navbar-nav me-auto ms-lg-3">
                <template v-if="role === 'admin'">
                    <router-link class="nav-link px-3" to="/admin/dashboard">Dashboard</router-link>
                    <router-link class="nav-link px-3" to="/admin/companies">Companies</router-link>
                    <router-link class="nav-link px-3" to="/admin/students">Students</router-link>
                    <router-link class="nav-link px-3" to="/admin/drives">Drives</router-link>
                    <router-link class="nav-link px-3" to="/admin/applications">Applications</router-link>
                    <router-link class="nav-link px-3" to="/admin/reports">Reports</router-link>
                </template>
            </div>
            <button class="btn btn-sm btn-outline-light px-3 mt-2 mt-lg-0" @click="logout">
                Logout
            </button>
        </div>
    </div>
</nav>
</template>

<style scoped>
.pp-navbar {
  background-color: #1e293b; /* Unified Dark Blue element theme */
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.nav-link {
  color: #94a3b8 !important;
  font-size: 0.95rem;
}
.nav-link:hover, .router-link-active {
  color: #ffffff !important;
}
</style>