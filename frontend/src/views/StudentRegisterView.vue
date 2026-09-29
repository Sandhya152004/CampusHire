<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import api from '../api'

const router = useRouter()

const full_name = ref('')
const email = ref('')
const password = ref('')
const degree = ref('')
const branch = ref('')
const cgpa = ref('')
const graduation_year = ref('')
const successMessage = ref('')

const registerStudent = async () => {
  try {
    await api.post(
      '/register/student',
      {
        full_name: full_name.value,
        email: email.value,
        password: password.value,
        degree: degree.value,
        branch: branch.value,
        cgpa: parseFloat(cgpa.value),
        graduation_year: parseInt(graduation_year.value)
      }
    )
    successMessage.value = 'Registration Successful. Redirecting to Login...'
    setTimeout(() => { router.push('/') }, 1500)
  } catch (error) {
    console.log(error.response.data)
    alert(error.response.data.message)
  }
}
</script>

<template>
  <div class="pp-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-7">
          <div class="card pp-form-card shadow p-4 p-md-5">

            <h3 class="fw-bold mb-1 text-dark-blue">Student Registration</h3>
            <p class="text-muted small mb-4">Create your credential profile to apply for placement drives.</p>

            <div v-if="successMessage" class="alert alert-success py-2 small">
              {{ successMessage }}
            </div>

            <div class="mb-3">
              <label class="form-label small fw-medium text-secondary">Full Name</label>
              <input v-model="full_name" class="form-control pp-input" placeholder="Enter full name">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-medium text-secondary">Email Address</label>
              <input v-model="email" type="email" class="form-control pp-input" placeholder="name@domain.com">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-medium text-secondary">Password</label>
              <input v-model="password" type="password" class="form-control pp-input" placeholder="Choose a safe password">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-medium text-secondary">Degree Track</label>
              <select v-model="degree" class="form-select pp-input">
                <option disabled value="">Select Degree</option>
                <option>B.Tech</option>
                <option>B.Sc</option>
                <option>B.Com</option>
                <option>B.A</option>
                <option>M.Tech</option>
                <option>M.Sc</option>
                <option>MBA</option>
                <option>Other</option>
              </select>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label small fw-medium text-secondary">Branch / Specialization</label>
                <input v-model="branch" class="form-control pp-input" placeholder="e.g. Computer Science">
              </div>
              <div class="col-md-3 mb-3">
                <label class="form-label small fw-medium text-secondary">CGPA</label>
                <input v-model="cgpa" class="form-control pp-input" placeholder="0.00">
              </div>
              <div class="col-md-3 mb-3">
                <label class="form-label small fw-medium text-secondary">Grad Year</label>
                <input v-model="graduation_year" class="form-control pp-input" placeholder="YYYY">
              </div>
            </div>

            <button class="btn btn-primary w-100 py-2 mt-3 fw-semibold pp-btn" @click="registerStudent">
              Complete Registration
            </button>

            <p class="text-center text-muted small mt-4 mb-0">
              Already verified? <router-link to="/" class="text-decoration-none text-primary fw-medium">Login here</router-link>
            </p>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pp-page {
  min-height: 100vh;
  background-color: #0f172a;
  background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 100%);
}
.pp-form-card {
  background: #ffffff;
  border-radius: 12px;
  border: none;
}
.text-dark-blue {
  color: #0f172a;
}
.pp-input {
  border-radius: 6px;
  border: 1px solid #cbd5e1;
}
.pp-btn {
  background-color: #2563eb;
  border: none;
}
</style>