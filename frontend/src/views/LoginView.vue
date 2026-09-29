<script setup>
import { ref } from 'vue'
import api from '../api';
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')

const router = useRouter()

const login = async () => {
  try {
    const response = await api.post(
      '/login',
      {
        email: email.value,
        password: password.value
      }
    )

    localStorage.setItem('token', response.data.token)
    localStorage.setItem('role', response.data.role)

    if (response.data.role === 'student') {
      router.push('/student/dashboard')
    }
    else if (response.data.role === 'company') {
      router.push('/company/dashboard')
    }
    else if (response.data.role === 'admin') {
      router.push('/admin/dashboard')
    }

  } catch (error) {
    alert(error.response.data.message)
  }
}
</script>

<template>
  <nav class="navbar navbar-expand navbar-dark pp-top-bar py-1">
    <div class="container text-white-50 small d-flex justify-content-between w-100">
      <div>
        <i class="bi bi-envelope-fill me-1"></i> support@yourcareerportal.edu
      </div>
      <div>
        <i class="bi bi-telephone-fill me-1"></i> +1 (555) 019-2834
      </div>
    </div>
  </nav>

  <div class="pp-login-wrapper d-flex align-items-center justify-content-center">
    <div class="container">
      <div class="row justify-content-center align-items-center">
        <div class="col-md-5">
          <div class="card pp-card shadow p-4 p-md-5">
            
            <div class="text-center mb-4">
              <div class="pp-login-badge mx-auto mb-3">
                AP
              </div>
              <h2 class="pp-brand-heading mb-1">
                Your Career Portal
              </h2>
              <p class="text-muted small">
                Sign in to manage your placements
              </p>
            </div>

            <div v-if="errorMessage" class="alert alert-danger py-2 small">
              {{ errorMessage }}
            </div>

            <div class="mb-3">
              <label class="form-label small fw-medium text-secondary">Email Address</label>
              <input
                v-model="email"
                type="email"
                class="form-control pp-input"
                placeholder="you@example.com"
              >
            </div>

            <div class="mb-4">
              <label class="form-label small fw-medium text-secondary">Password</label>
              <input
                v-model="password"
                type="password"
                class="form-control pp-input"
                placeholder="Enter your password"
              >
            </div>

            <button
              class="btn btn-primary w-100 py-2 fw-semibold pp-btn-primary"
              @click="login"
            >
              Login
            </button>

            <div class="position-relative my-4">
              <hr class="text-muted opacity-25">
              <span class="position-absolute top-50 start-50 translate-middle bg-white px-2 small text-muted">
                New Account
              </span>
            </div>

            <div class="d-flex justify-content-center gap-2 flex-wrap">
              <router-link
                to="/register/student"
                class="btn btn-outline-primary btn-sm px-3"
              >
                Student Registration
              </router-link>
              <router-link
                to="/register/company"
                class="btn btn-outline-secondary btn-sm px-3"
              >
                Company Registration
              </router-link>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:deep(:root), th, td, div, input, select, textarea {
  --pp-dark-bg: #0f172a;     /* Deep slate blue background */
  --pp-card-bg: #1e293b;     /* Dark blue for elements */
  --pp-primary: #3b82f6;     /* Electric blue accent */
}

.pp-top-bar {
  background-color: #0b0f19;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.pp-login-wrapper {
  min-height: calc(100vh - 34px);
  background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 100%);
  padding: 2rem 0;
}

.pp-card {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
}

.pp-login-badge {
  width: 52px;
  height: 52px;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}

.pp-brand-heading {
  color: #0f172a;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.pp-input {
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  padding: 0.6rem 0.75rem;
}

.pp-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.pp-btn-primary {
  background-color: #2563eb;
  border: none;
}
.pp-btn-primary:hover {
  background-color: #1d4ed8;
}
</style>