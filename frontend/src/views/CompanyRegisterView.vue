<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import api from '../api'

const router = useRouter()

const company_name = ref('')
const email = ref('')
const password = ref('')
const website = ref('')
const industry = ref('')
const location = ref('')
const description = ref('')
const hr_name = ref('')
const hr_email = ref('')
const hr_contact = ref('')
const successMessage = ref('')

const registerCompany = async () => {
  try {
    await api.post(
    '/register/company',
      {
        company_name: company_name.value,
        email: email.value,
        password: password.value,
        website: website.value,
        industry: industry.value,
        location: location.value,
        description: description.value,
        hr_name: hr_name.value,
        hr_email: hr_email.value,
        hr_contact: hr_contact.value
      }
    )
    successMessage.value = 'Registration Successful. Redirecting to Login...'
    setTimeout(() => { router.push('/') }, 3000)
  } catch (error) {
    alert(error.response.data.message)
  }
}
</script>

<template>
<div class="pp-page">
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card pp-form-card shadow p-4 p-md-5">

          <h3 class="fw-bold mb-1 text-dark-blue">Corporate Registration</h3>
          <p class="text-muted small mb-4">Onboard your enterprise to schedule campus drives and look over applicants.</p>

          <div v-if="successMessage" class="alert alert-success py-2 small">
            {{ successMessage }}
          </div>

          <div class="mb-3">
            <label class="form-label small fw-medium text-secondary">Company Legal Name</label>
            <input v-model="company_name" class="form-control pp-input" placeholder="Company Name">
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-medium text-secondary">Corporate Email ID</label>
              <input v-model="email" type="email" class="form-control pp-input" placeholder="hr@company.com">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-medium text-secondary">Access Password</label>
              <input v-model="password" type="password" class="form-control pp-input" placeholder="Password">
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-medium text-secondary">Official Website</label>
              <input v-model="website" class="form-control pp-input" placeholder="https://...">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-medium text-secondary">Industry Sector</label>
              <input v-model="industry" class="form-control pp-input" placeholder="e.g. Technology, Finance">
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label small fw-medium text-secondary">Headquarters Location</label>
            <input v-model="location" class="form-control pp-input" placeholder="City, Country">
          </div>

          <div class="mb-4">
            <label class="form-label small fw-medium text-secondary">Brief Description</label>
            <textarea v-model="description" class="form-control pp-input" placeholder="Describe company profile..." rows="3"></textarea>
          </div>

          <div class="position-relative my-4">
            <hr class="text-muted opacity-25">
            <span class="position-absolute top-50 start-0 translate-middle-y bg-white pe-2 small text-muted fw-bold text-uppercase tracking-wider text-primary">
              Point of Contact Details
            </span>
          </div>

          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label small fw-medium text-secondary">HR Lead Name</label>
              <input v-model="hr_name" class="form-control pp-input" placeholder="Full Name">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label small fw-medium text-secondary">HR Email Address</label>
              <input v-model="hr_email" type="email" class="form-control pp-input" placeholder="contact@company.com">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label small fw-medium text-secondary">HR Phone Number</label>
              <input v-model="hr_contact" class="form-control pp-input" placeholder="Phone Number">
            </div>
          </div>

          <button class="btn btn-primary w-100 py-2 mt-3 fw-semibold pp-btn" @click="registerCompany">
            Submit Onboarding Request
          </button>

          <p class="text-center text-muted small mt-4 mb-0">
            Already registered? <router-link to="/" class="text-decoration-none text-primary fw-medium">Login here</router-link>
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